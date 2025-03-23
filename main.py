import pytesseract
import pdfplumber
import docx
from PIL import Image, ImageFilter
import os
import re
from nicegui import ui


# File Handling - Text Extraction Functions

def read_pdf(file_path):
    """Extract text from a PDF and structure it into a string format."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    structured_data = extract_resume_sections(text)
    return structured_data  # Return as string instead of JSON

def read_docx(file_path):
    """Extract text from a DOCX file and return as a structured string."""
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])

    structured_data = extract_resume_sections(text)
    return structured_data  # Return as string instead of JSON

def read_image(file_path):
    """Extract text from an image file using OCR and return structured string."""
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
    return structured_data  # Return as string instead of JSON


# Resume Analysis - Section Identification

def extract_resume_sections(text):
    """Identify and split resume text into sections using regex."""
    sections = {
        "Experience": "",
        "Education": "",
        "Skills": "",
        "Projects": "",
    }

    # Define section patterns (using regular expressions for flexibility)
    section_patterns = {
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

    # Convert sections dictionary to a formatted string
    result = ""
    for section, content in sections.items():
        result += f"{section}:\n{content}\n\n"
    
    return result


# NiceGUI UI Setup
upload_folder = "uploads"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

def upload_file(file):
    """Handle file upload and extract text."""
    if not file:
        return "No file selected"

    file_path = os.path.join(upload_folder, file.name)
    file.save(file_path)  # Save the file to the server

    # Check if the file size is correct
    if os.path.getsize(file_path) == 0:
        return "Failed to save the file properly"

    file_extension = file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        result = read_pdf(file_path)
    elif file_extension == 'docx':
        result = read_docx(file_path)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        result = read_image(file_path)
    else:
        result = "Unsupported file format"
    
    result_output.set_text(result)

    # Add download link
    ui.link(f"Download {file.name}", file_path).classes("text-link")


# NiceGUI UI

with ui.column():
    ui.label('Upload a file (PDF, DOCX, or Image):')
    upload_button = ui.upload(on_upload=upload_file)

    result_label = ui.label('Extracted Resume Data:').classes('text-h6')
    result_output = ui.label("").classes('text-body1')


# Start the NiceGUI app
ui.run()
