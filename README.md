# Excel Financial Processor

A full-stack web application that processes Excel files and generates professional estimates and financial statements in both PDF and Excel formats.

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/YOUR_USERNAME/excel-financial-processor)

## 🚀 Live Demo

[View Live Demo](https://your-site-name.netlify.app) (Replace with your actual Netlify URL)

## Features

- **Smart Excel Processing**: Automatically detects and processes estimates and financial statements
- **Professional Formatting**: Generates clean, client-ready documents with proper styling
- **Multiple Output Formats**: Download as both PDF and Excel files
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS
- **Secure Processing**: Files are processed securely on the server

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pandas**: Data manipulation and analysis
- **OpenPyXL**: Excel file handling
- **ReportLab**: PDF generation
- **Uvicorn**: ASGI server

### Frontend
- **React**: User interface library
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Dropzone**: File upload component
- **Lucide React**: Icon library

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Click "Upload Your Excel File" or drag and drop an Excel file
3. Wait for the processing to complete
4. Download your generated PDF and Excel files

## API Endpoints

### POST /upload
Upload and process an Excel file.

**Request**: Multipart form data with Excel file
**Response**: 
```json
{
  "file_id": "uuid",
  "original_filename": "example.xlsx",
  "pdf_download": "/download/uuid_processed.pdf",
  "excel_download": "/download/uuid_processed.xlsx",
  "status": "success"
}
```

### GET /download/{filename}
Download a generated file.

**Response**: File download

### GET /health
Health check endpoint.

**Response**: 
```json
{
  "status": "healthy"
}
```

## File Processing

The application automatically:

1. **Analyzes** Excel file structure and content
2. **Detects** estimates and financial statements using keyword matching
3. **Formats** data with professional styling:
   - Bold headers and clean borders
   - Currency formatting
   - Proper alignment
   - Summary totals
4. **Generates** both PDF and Excel outputs

## Supported File Types

- `.xlsx` (Excel 2007+)
- `.xls` (Excel 97-2003)

## File Size Limits

- Maximum file size: 10MB
- Processing timeout: 60 seconds

## Development

### Backend Development
```bash
cd backend
python main.py
```

### Frontend Development
```bash
cd frontend
npm start
```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Project Structure

```
excel/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── excel_processor.py      # Excel processing logic
│   ├── pdf_generator.py        # PDF generation
│   ├── excel_generator.py      # Excel generation
│   ├── requirements.txt        # Python dependencies
│   ├── uploads/                # Temporary upload directory
│   └── outputs/                # Generated files directory
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── App.js             # Main application
│   │   ├── index.js           # Entry point
│   │   └── index.css          # Global styles
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   └── tailwind.config.js     # Tailwind configuration
└── README.md                  # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the repository.
