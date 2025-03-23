import pytesseract
import pdfplumber
import docx
from PIL import Image, ImageFilter
import json
import os
from flask import Flask, request

# Flask App Setup
app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload via web form."""
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    # If no file is selected
    if file.filename == "":
        return "No selected file", 400

    # Save the file to a specific folder
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)  # Save the file to the server

    # Process the file and extract text
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return read_pdf(file_path)
    elif file_extension == 'docx':
        return read_docx(file_path)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        return read_image(file_path)
    else:
        return "Unsupported file format", 400


# File Handling - Text Extraction Functions

def read_pdf(file_path):
    """Extract text from a PDF and structure it into JSON format."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    structured_data = extract_resume_sections(text)
    return json.dumps(structured_data, indent=4)

def read_docx(file_path):
    """Extract text from a DOCX file and return structured JSON."""
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])

    structured_data = extract_resume_sections(text)
    return json.dumps(structured_data, indent=4)


def read_image(file_path):
    """Extract text from an image file using OCR and return structured JSON."""
    image = Image.open(file_path)

    # Preprocessing: Convert image to grayscale
    image = image.convert("L")

    # Apply thresholding for better contrast (binary image)
    image = image.point(lambda p: p > 200 and 255)

    # Optional: Apply image filtering for noise removal
    image = image.filter(ImageFilter.MedianFilter())

    # OCR: Extract text from the preprocessed image
    text = pytesseract.image_to_string(image)

    structured_data = extract_resume_sections(text)
    return json.dumps(structured_data, indent=4)


# Resume Analysis - Section Identification

def extract_resume_sections(text):
    """Identify and split resume text into sections using regex."""
    sections = {
        "Contact Information": "",
        "Experience": "",
        "Education": "",
        "Skills": "",
        "Projects": "",
    }

    # Define section patterns (using regular expressions for flexibility)
    section_patterns = {
        "Contact Information": r"(?:email|phone|address|contact)",
        "Experience": r"(?:experience|professional\s*experience|work\s*history)",
        "Education": r"(?:education|academic\s*history|degrees)",
        "Skills": r"(?:skills|technical\s*skills|competencies)",
        "Projects": r"(?:projects|research|portfolio)"
    }

    lines = text.split("\n")
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match section patterns using regex
        for section, pattern in section_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                current_section = section
                break

        # Add the line to the identified section
        if current_section:
            sections[current_section] += line + "\n"

    return sections


# AI Chat - Placeholder functions for future implementation

def generate_response(query, resume_text):
    """Answer user queries based on resume content."""
    pass

def score_resume(text):
    """Rank the resume based on predefined criteria."""
    pass

def identify_strengths_weaknesses(text):
    """Identify areas of improvement based on the resume."""
    pass


# UI & API - Flask Web App Setup (Already handled above)
def build_ui():
    """Create UI interface for the user to interact with."""
    pass

def setup_api():
    """Setup API integration."""
    pass


# Main entry point for running the app
if __name__ == "__main__":
    app.run(debug=True)
