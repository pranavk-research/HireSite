import os
import json
from groq import Groq
from nicegui import ui, events
import base64
from io import BytesIO
import fitz
import docx

client = Groq(
    api_key="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"
)

def query(query):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()

def extract_text_from_docx(file_data):
    """Extracts text from a DOCX file."""
    doc = docx.Document(BytesIO(file_data))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def handle_upload(e: events.UploadEventArguments):
    file_data = e.content.read()  # Read file as bytes
    filename = e.name.lower()

    if filename.endswith(".pdf"):
        with fitz.open(stream=file_data, filetype="pdf") as doc:
            text = "\n".join([page.get_text() for page in doc])  # Extract text
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_data)
    else:
        text = "Unsupported file type."

    content.set_content(text)  # Display extracted text
    dialog.open()

ui.upload(on_upload=handle_upload).props('accept=.pdf,.docx').classes('max-w-full')

# Run App
ui.run(title="HireSite - AI Resume Tool", dark=False)
