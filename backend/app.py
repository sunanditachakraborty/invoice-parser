from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from inference import extract_invoice
from excel_utils import append_to_excel

import shutil
import os

app = FastAPI()

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Change this later when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Folders
# -----------------------------------

UPLOAD_DIR = "uploads"
WORKBOOK_DIR = "workbooks"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(WORKBOOK_DIR, exist_ok=True)

current_excel = None

# -----------------------------------
# Home
# -----------------------------------

@app.get("/")
def home():
    return {"message": "Invoice Parser API Running"}

# -----------------------------------
# Upload Excel Workbook
# -----------------------------------

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):

    global current_excel

    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an Excel workbook (.xlsx)"
        )

    excel_path = os.path.join(WORKBOOK_DIR, file.filename)

    with open(excel_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_excel = excel_path

    return {
        "message": "Excel uploaded successfully",
        "file": file.filename
    }

# -----------------------------------
# Upload Invoice
# -----------------------------------

@app.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):

    global current_excel

    if current_excel is None:
        raise HTTPException(
            status_code=400,
            detail="Please upload an Excel workbook first."
        )

    invoice_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(invoice_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    invoice = extract_invoice(invoice_path)

    append_to_excel(current_excel, invoice)

    return {
        "message": "Invoice added successfully",
        "invoice": invoice
    }

# -----------------------------------
# Download Updated Excel
# -----------------------------------

@app.get("/download-excel")
def download_excel():

    global current_excel

    if current_excel is None:
        raise HTTPException(
            status_code=400,
            detail="No workbook uploaded."
        )

    return FileResponse(
        current_excel,
        filename=os.path.basename(current_excel),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )