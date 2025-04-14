from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configure upload folder with absolute path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload directory exists
try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception as e:
    print(f"Error creating upload directory: {e}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_pdf(input_pdf):
    # Create a PDF reader object
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Process each page
    for page in reader.pages:
        # Add the page to the writer
        writer.add_page(page)

    # Set compression parameters
    writer._compress = True

    # Create a bytes buffer for the output
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    return output_buffer

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if not all(allowed_file(file.filename) for file in files):
            flash('Invalid file type. Only PDF files are allowed.', 'error')
            return redirect(request.url)

        try:
            if request.form.get('action') == 'compress':
                # Handle compression
                if len(files) == 1:
                    # Single file compression
                    file = files[0]
                    compressed_pdf = compress_pdf(file)
                    return send_file(
                        compressed_pdf,
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name='compressed.pdf'
                    )
                else:
                    # Multiple files - merge first, then compress
                    merger = PdfMerger()
                    for file in files:
                        merger.append(file)
                    
                    # Create a buffer for the merged PDF
                    merged_buffer = io.BytesIO()
                    merger.write(merged_buffer)
                    merger.close()
                    merged_buffer.seek(0)
                    
                    # Compress the merged PDF
                    compressed_pdf = compress_pdf(merged_buffer)
                    return send_file(
                        compressed_pdf,
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name='compressed.pdf'
                    )
            else:
                # Handle merging
                merger = PdfMerger()
                for file in files:
                    merger.append(file)
                
                # Create a buffer for the merged PDF
                output_buffer = io.BytesIO()
                merger.write(output_buffer)
                merger.close()
                output_buffer.seek(0)
                
                return send_file(
                    output_buffer,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name='merged.pdf'
                )

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 