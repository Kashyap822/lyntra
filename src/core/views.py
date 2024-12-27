from flask import Flask, render_template, request, Blueprint, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import docx
import fitz

# This line doesn't work for some reason, so I commented it out for testing purposes
# from src.portfolio_generator.crew import WebsiteGenerator

# Added for testing purposes
app = Flask(__name__)

# CrewAI Flows Functionality
from crewai.flow.flow import Flow, listen, start, and_, or_, router

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

core = Blueprint('core', __name__)
# Route for the home page
@core.route('/')
def index():
    return render_template('index.html')

# Route for the web app
@core.route('/generate-portfolio')
def generate_portfolio():
    return render_template('generate_portfolio.html')

# Route for the contact page
@core.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the admin pages (Privacy Policy)
# In the future, I am planning to move this into an "admin" directory for easier organization
@core.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@core.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html')

# Route to display the generated website
@core.route('/website')
def display_website():
    # Get the generated HTML from the session
    html_output = session.get('generated_html')
    return render_template('website/website.html', html_content=html_output)

# API Endpoints

@core.route('/api/submitQuiz', methods=['POST'])
def submit_quiz():
    # Default portfolio builder
    layout = "one pager"
    purpose = "Build a portfolio based on the resume provided."

    theme = request.form.get('theme', "Simple, modern, and elegant. Use a unique font but not over-the-top")
    color = request.form.get('color', "Use a combination of warm light colors that compliment well with each other")
    content = request.form.get('content', "A portfolio with 5 sections: HERO section (with image), about me, my work, education, and contact information")
    resume = request.files.get('resume')

    # Default resume text if no file is uploaded
    if not resume:
        resume = "I do not have a resume. Assume I am a college student with basic work experience"
    else:
        # Check if the file is allowed
        if resume and allowed_file(resume.filename):
            # Secure the file name and save it to the uploads folder
            filename = secure_filename(resume.filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(file_path)

            # Extract text based on the file type
            if filename.endswith('.docx'):
                resume_text = extract_text_from_docx(file_path)
            elif filename.endswith('.pdf'):
                resume_text = extract_text_from_pdf(file_path)
            else:
                resume_text = "Unsupported file format"  # If not DOCX or PDF

            resume = resume_text
        else:
            resume = "Invalid resume format"  # If the file format is not allowed

    # Default values if none are provided.
    inputs = {
        'purpose': purpose,
        'theme': theme,
        'color': color,
        'layout': layout,
        'content': content,
        'resume': resume
    }
    
    # Test to make sure that resume contents are read
    print(resume)

    # Run the CrewAI model with the inputs
    # Relies on 'from src.portfolio_generator.crew import WebsiteGenerator' to work
    # For testing purposes we can ignore this temporarily
    """
    website_generator = WebsiteGenerator()
    result = website_generator.crew().kickoff(inputs=inputs)

    # Extract the HTML string from the result (assuming result.result holds the HTML)
    html_output = result.result if hasattr(result, 'result') else str(result)

    # Remove unwanted Markdown-style markers
    html_output = html_output.strip('```html').strip('```').strip()

    print(f"HTML OUTPUT: {html_output}")

    # Store the generated HTML in the session
    session['generated_html'] = html_output
    """

    # Redirect to a new route to display the HTML
    return redirect(url_for('core.display_website'))