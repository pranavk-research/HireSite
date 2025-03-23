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

# Resume Data
resume_data = {
    "name": "Avinash Karthik",
    "title": "Software Engineer | AI Enthusiast",
    "contact": {
        "Email": "avinash@example.com",
        "Phone": "+1 234 567 890",
        "LinkedIn": "linkedin.com/in/avinashkarthik",
        "GitHub": "github.com/avinashkarthik"
    },
    "experience": [
        {"role": "Software Developer", "company": "TechCorp", "years": "2022 - Present",
         "description": "Developed AI-powered resume ranking system."},
        {"role": "Intern", "company": "Startup Inc.", "years": "2021 - 2022",
         "description": "Worked on backend APIs and AI models."}
    ],
    "education": "B.Sc. Computer Science, XYZ University (2018 - 2022)",
    "skills": ["Python", "Machine Learning", "NiceGUI", "API Development", "Resume Ranking"],
    "projects": [
        {"name": "HireSite", "description": "AI-powered resume ranking and feedback tool."},
        {"name": "Connect 4 AI", "description": "Built an AI to play Connect 4 using Minimax."}
    ]
}

# App Header
with ui.header().classes("bg-blue-700 text-white p-4 text-center"):
    ui.label("HireSite - AI Resume Assistant").classes("text-3xl font-bold")

# Introduction Section
with ui.card().classes("m-4 p-6 shadow-lg bg-gray-100"):
    ui.label("Set your sights HIGHER with HireSite!").classes("text-2xl font-bold text-blue-700")
    ui.label(
        "Your personal AI tool for all things CV. It helps recruiters sort through resumes, rank them based on quality, "
        "and provides personal advice with specific tips to improve your resume. It can also identify your strengths and weaknesses."
    ).classes("text-md")

# Features Section
with ui.card().classes("m-4 p-6 shadow-lg bg-gray-100"):
    ui.label("✨ Features").classes("text-xl font-bold text-blue-700 mb-2")
    features = [
        "AI-powered resume ranking",
        "Personalized feedback on strengths & weaknesses",
        "Resume quality analysis (keywords, experience, readability)",
        "Chat section for specific resume-related queries",
        "User-friendly UI for easy interaction"
    ]
    for feature in features:
        ui.label(feature).classes("text-md")

# Chat Section
with ui.card().classes("m-4 p-6 shadow-lg bg-gray-100"):
    ui.label("Ask AI About Your Resume").classes("text-xl font-bold text-blue-700 mb-2")
    chat_input = ui.input("Ask something...").classes("w-full p-2 border rounded")
    chat_output = ui.label("").classes("mt-4 text-md text-gray-800")

    def process_question():
        question = chat_input.value
        if question:
            chat_output.set_text(f"AI Response: {query(question)}")

    ui.button("Submit", on_click=process_question).classes("bg-blue-600 text-white px-4 py-2 rounded mt-2")

# Run App
ui.run(title="HireSite - AI Resume Tool", dark=False)
