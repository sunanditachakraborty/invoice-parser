# Invoice Parser

## Overview

Invoice Parser is an AI-powered document processing application that automates invoice data extraction and Excel entry. The application combines a FastAPI backend, a React frontend, and the GLM-OCR Vision Language Model to extract structured information from invoice images and append the extracted data into an existing Excel workbook.

The system is capable of reading both printed and handwritten text, making it suitable for invoices that contain manually entered inward numbers, inward dates, quantities, and other handwritten annotations.

---

## Features

- AI-powered invoice data extraction
- Supports both printed and handwritten text
- Upload existing Excel workbooks
- Automatically appends extracted invoice data
- Preserves existing workbook structure
- REST API built with FastAPI
- Simple React-based user interface
- Download updated Excel workbook after processing

---

## Extracted Fields

The application extracts the following information from invoices:

- Supplier
- Invoice Number
- Invoice Date
- Purchase Order Number
- SAP Number
- Quantity
- Inward Number
- Inward Date

---

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- FastAPI
- Python
- Hugging Face Transformers
- GLM-OCR
- PyTorch
- OpenPyXL
- Pillow
- Pandas

---

## Project Structure

```
invoice-parser/
│
├── backend/
│   ├── app.py
│   ├── inference.py
│   ├── excel_utils.py
│   ├── requirements.txt
│   ├── uploads/
│   └── workbooks/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/sunanditachakraborty/invoice-parser.git

cd invoice-parser
```

---

## Backend Setup

Create a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Run the backend

```bash
cd backend

uvicorn app:app --reload
```

The backend runs on:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

Navigate to the frontend folder.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

The frontend runs on:

```
http://localhost:5173
```

---

## API Endpoints

### GET /

Checks whether the API is running.

---

### POST /upload-excel

Uploads an Excel workbook that will receive extracted invoice data.

---

### POST /upload-invoice

Uploads an invoice image, extracts structured information using the AI model, and appends the extracted data to the uploaded workbook.

---

### GET /download-excel

Downloads the updated Excel workbook.

---

## AI Model

The application uses the **GLM-OCR Vision Language Model** through the Hugging Face Transformers library to extract structured information from invoice images.

The model processes both printed and handwritten text and returns structured JSON, which is then written into the uploaded Excel workbook.

---

## Future Improvements

- PDF invoice support
- Batch invoice processing
- Database integration
- User authentication
- Cloud deployment
- Docker support
- Multi-sheet workbook support
- OCR confidence scoring

---

## License

This project is provided for educational and demonstration purposes.
