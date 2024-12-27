from src import app
import os
import fitz
import docx

# Upload folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}

# Check if the file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Extract text from .docx
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text.strip()

# Extract text from .pdf
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ''
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text.strip()

if __name__ == '__main__':
    app.run(debug=True)