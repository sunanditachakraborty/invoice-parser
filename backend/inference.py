import gc
import json
import os

import torch
from PIL import Image

from transformers import (
    AutoProcessor,
    GlmOcrForConditionalGeneration
)

# --------------------------------------------------
# CUDA Memory
# --------------------------------------------------

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# --------------------------------------------------
# Model
# --------------------------------------------------

MODEL = "zai-org/GLM-OCR"

processor = AutoProcessor.from_pretrained(
    MODEL,
    trust_remote_code=True
)

model = GlmOcrForConditionalGeneration.from_pretrained(
    MODEL,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True,
)

model.eval()

# --------------------------------------------------
# Prompt
# --------------------------------------------------

PROMPT = """
Extract information from this invoice.

Read BOTH printed and handwritten text.

Return ONLY valid JSON.

{
    "invoice_number": "",
    "invoice_date": "",
    "supplier": "",
    "purchase_order": "",
    "sap_number": "",
    "quantity": "",
    "inward_number": "",
    "inward_date": ""
}

Rules:
- Use handwritten text if present for inward_number and inward_date.
- Use printed text for invoice_number, invoice_date, supplier and purchase_order.
- Give date only in DD_MM_YYYY format, only numbers no words
- If quantity or sap_number are handwritten, extract the handwritten values.
- If any field is not found, return an empty string.
- Return ONLY raw JSON.
- Do not explain anything.
- Do not use markdown.
"""

# --------------------------------------------------
# Inference
# --------------------------------------------------

def extract_invoice(image_path):

    image = Image.open(image_path).convert("RGB")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image
                },
                {
                    "type": "text",
                    "text": PROMPT
                }
            ]
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():

        generated_ids = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            temperature=0.0,
        )

    generated = generated_ids[:, inputs["input_ids"].shape[1]:]

    response = processor.decode(
        generated[0],
        skip_special_tokens=True
    )

    response = (
        response.replace("```json", "")
                .replace("```", "")
                .strip()
    )

    try:
        result = json.loads(response)

    except Exception:

        result = {
            "invoice_number": "",
            "invoice_date": "",
            "supplier": "",
            "purchase_order": "",
            "sap_number": "", 
            "quantity": "",
            "inward_number": "",
            "inward_date": "",
            "raw_output": response
        }

    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return result