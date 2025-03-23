import pytesseract
import pdfplumber
from PIL import Image, ImageFilter
import os
import re
from nicegui import ui


# File Handling - Text Extraction Functions

def extract_text_from_pdf(file_path):
    """Extract text from a PDF and return as a structured string."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_image(file_path):
    """Extract text from an image using OCR and return as a structured string."""
    image = Image.open(file_path)
    image = image.convert("L")  # Convert to grayscale
    image = image.point(lambda p: p > 200 and 255)  # Thresholding
    image = image.filter(ImageFilter.MedianFilter())  # Noise reduction
    text = pytesseract.image_to_string(image)
    return text


# Resume Analysis - Section Identification

def identify_resume_sections(text):
    """Identify and split resume text into sections (Experience, Education, Skills, Projects)."""
    sections = {
        "Experience": "",
        "Education": "",
        "Skills": "",
        "Projects": "",
    }

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

    # Format the extracted sections
    result = ""
    for section, content in sections.items():
        if content.strip():  # Only include sections with content
            result += f"{section}:\n{content}\n\n"

    return result.strip()


# NiceGUI UI Setup

upload_folder = "uploads"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)


def handle_file_upload(event):
    """Handle the file upload, extract text, and display structured result."""
    file = event.files[0]  # Get the uploaded file
    if not file:
        return "No file selected"

    file_path = os.path.join(upload_folder, file.name)
    file.save(file_path)  # Save the file

    # Ensure the file has been saved correctly
    if os.path.getsize(file_path) == 0:
        return "Failed to save the file properly"

    file_extension = file.name.split('.')[-1].lower()

    # Process based on file type
    if file_extension == 'pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif file_extension == 'docx':
        extracted_text = extract_text_from_docx(file_path)
    elif file_extension in ['jpg', 'jpeg', 'png']:
        extracted_text = extract_text_from_image(file_path)
    else:
        return "Unsupported file format"

    # Identify resume sections in the extracted text
    structured_data = identify_resume_sections(extracted_text)

    # Display the result
    result_output.set_text(structured_data)

    # Provide a download link for the uploaded file
    ui.link(f"Download {file.name}", file_path).classes("text-link")


# NiceGUI UI

with ui.column():
    ui.label('Upload a file (PDF, DOCX, or Image):')
    upload_button = ui.upload(on_upload=handle_file_upload)

    result_label = ui.label('Extracted Resume Data:').classes('text-h6')
    result_output = ui.label("").classes('text-body1')

# Start the NiceGUI app
ui.run()
