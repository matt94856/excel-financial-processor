from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import os
import uuid
from pathlib import Path
from typing import List
import logging
from excel_processor import ExcelProcessor
from pdf_generator import PDFGenerator
from excel_generator import ExcelGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Excel Financial Processor", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads and outputs directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Excel Financial Processor API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process Excel file"""
    try:
        # Validate file type
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are allowed")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        upload_filename = f"{file_id}{file_extension}"
        upload_path = UPLOAD_DIR / upload_filename
        
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"File uploaded: {upload_filename}")
        
        # Process the Excel file
        processor = ExcelProcessor()
        processed_data = processor.process_file(upload_path)
        
        # Generate outputs
        pdf_generator = PDFGenerator()
        excel_generator = ExcelGenerator()
        
        # Generate PDF
        pdf_filename = f"{file_id}_processed.pdf"
        pdf_path = OUTPUT_DIR / pdf_filename
        pdf_generator.generate_pdf(processed_data, pdf_path)
        
        # Generate Excel
        excel_filename = f"{file_id}_processed.xlsx"
        excel_path = OUTPUT_DIR / excel_filename
        excel_generator.generate_excel(processed_data, excel_path)
        
        # Clean up uploaded file
        os.remove(upload_path)
        
        return {
            "file_id": file_id,
            "original_filename": file.filename,
            "pdf_download": f"/download/{pdf_filename}",
            "excel_download": f"/download/{excel_filename}",
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        # Clean up uploaded file if it exists
        if 'upload_path' in locals() and upload_path.exists():
            os.remove(upload_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated file"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type
    if filename.endswith('.pdf'):
        media_type = "application/pdf"
    elif filename.endswith('.xlsx'):
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        media_type = "application/octet-stream"
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
