# PDF Merger

A modern web application built with Flask that allows users to merge multiple PDF files into a single PDF document.

## Features

- Drag and drop interface for file upload
- Multiple PDF file selection
- Modern and responsive UI
- Real-time file selection feedback
- Error handling and validation
- Automatic cleanup of temporary files

## Requirements

- Python 3.7 or higher
- Flask
- PyPDF2
- Werkzeug

## Installation

1. Clone this repository or download the files
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`
3. Drag and drop PDF files or click to select files
4. Click the "Merge PDFs" button
5. The merged PDF will be automatically downloaded

## Notes

- Only PDF files are accepted
- The application creates an `uploads` directory to temporarily store files during the merging process
- All temporary files are automatically cleaned up after the merge is complete 