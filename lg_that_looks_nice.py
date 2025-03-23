import os
import json
from groq import Groq
from nicegui import ui, events
import base64
from io import StringIO 
import fitz 

client = Groq(
    api_key="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"
)

test = "showering"
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

with ui.tabs().classes("w-full text-lg font-semibold text-gray-700 border-b") as tabs:
    one = ui.tab('Introduction')
    two = ui.tab('features')
    three = ui.tab('Ask about your resume')
    four = ui.tab('rank resumes')
    five = ui.tab('Chat with our helper')
with ui.tab_panels(tabs, value=two).classes('w-full'):

    with ui.tab_panel(one):
    # Introduction Section
    with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
        ui.label("Set your sights HIGHER with HireSite!").classes("text-4xl font-extrabold text-blue-700")

        ui.label(
            "HireSite is an AI-powered platform designed to streamline the recruitment process. It helps hiring teams "
            "efficiently evaluate resumes, rank candidates based on experience, skills, and overall quality, and provides "
            "personalized feedback to improve resumes. Our platform offers tailored suggestions to help job seekers enhance "
            "their applications, ensuring that each resume stands out in a competitive job market."
        ).classes("text-lg text-gray-800 mt-4")

    
        with ui.row().classes("space-x-4 mt-6"):
 
            with ui.card().classes("p-6 rounded-xl bg-white shadow-md border border-gray-300 w-full"):
                ui.label("Meet the Makers").classes("text-2xl font-semibold text-blue-700 mb-2")
                ui.image("https://via.placeholder.com/150", alt="Image of Makers").classes("w-full rounded-lg")
                ui.label(
                    "We are a passionate team of AI enthusiasts and tech innovators. With backgrounds in machine learning, "
                    "data science, and software engineering, we are committed to creating tools that empower individuals and "
                    "businesses alike. Our mission is to make the hiring process smarter, faster, and more efficient."
                ).classes("text-md text-gray-700 mt-4")

            # Meet the Makers Box 2
            with ui.card().classes("p-6 rounded-xl bg-white shadow-md border border-gray-300 w-full"):
                ui.label("Meet the Makers").classes("text-2xl font-semibold text-blue-700 mb-2")
                ui.image("https://via.placeholder.com/150", alt="Image of Makers").classes("w-full rounded-lg")
                ui.label(
                    "Our journey began with a shared vision to transform recruitment with the power of AI. By combining cutting-edge "
                    "technology with our deep understanding of hiring trends, we built HireSite to simplify and revolutionize the way "
                    "companies connect with top talent."
                ).classes("text-md text-gray-700 mt-4")




    with ui.tab_panel(two):
    with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
        ui.label("✨ Features").classes("text-4xl font-extrabold text-blue-700 mb-4")
        features = [
            {"title": "AI-powered resume ranking", "icon": "📊"},
            {"title": "Personalized feedback on strengths & weaknesses", "icon": "📝"},
            {"title": "Resume quality analysis (keywords, experience, readability)", "icon": "🔍"},
            {"title": "Chat section for specific resume-related queries", "icon": "💬"},
            {"title": "User-friendly UI for easy interaction", "icon": "💡"}
        ]
        with ui.column().classes("space-y-4"):
            for feature in features:
                with ui.card().classes("p-4 rounded-xl bg-gray-50 shadow-md border border-gray-300 hover:bg-blue-50"):
                    ui.label(feature["icon"] + " " + feature["title"]).classes("text-lg text-gray-800 font-medium")



    with ui.tab_panel(three):
        # Upload Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            with ui.dialog().props('full-width') as dialog:
                with ui.card():
                    content = ui.markdown()

            def handle_upload(e: events.UploadEventArguments):
                file_data = e.content.read()  # Read file as bytes

                with fitz.open(stream=file_data, filetype="pdf") as doc:
                    text = "\n".join([page.get_text() for page in doc])  # Extract text

                content.set_content(text)  # Display extracted text
                dialog.open()
            ui.upload(on_upload=handle_upload).props('accept=.pdf').classes('max-w-full p-6 border-2 border-dashed border-gray-400 rounded-lg')



        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            ui.label("AI review").classes("text-3xl font-extrabold text-blue-700 mb-2")
            chat_input = ui.input("Here is our AI's review of your resume").classes("w-full p-4 border-2 border-gray-300 rounded-lg text-gray-800")
            chat_output = ui.label("").classes("mt-4 text-lg text-gray-800")

            def process_question():
                question = chat_input.value
                if question:
                    chat_output.set_text(f"Identify the strengths and weaknesses in this resume" + ui.upload(on_upload=handle_upload).props('accept=.pdf').classes('max-w-full'))

            ui.button("Submit", on_click=process_question).classes("bg-blue-500 hover:bg-blue-600 transition-all text-white px-6 py-3 rounded-lg shadow-md mt-2")



    with ui.tab_panel(five):
        # Upload Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            with ui.dialog().props('full-width') as dialog:
                with ui.card():
                    content = ui.markdown()

            def handle_upload(e: events.UploadEventArguments):
                file_data = e.content.read()  # Read file as bytes

                with fitz.open(stream=file_data, filetype="pdf") as doc:
                    text = "\n".join([page.get_text() for page in doc])  # Extract text

                content.set_content(text)  # Display extracted text
                dialog.open()

            ui.upload(on_upload=handle_upload).props('accept=.pdf').classes('max-w-full p-6 border-2 border-dashed border-gray-400 rounded-lg')

        # Chat Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            ui.label("Ask AI About Your Resume").classes("text-3xl font-extrabold text-blue-700 mb-2")
            chat_input = ui.input("Ask something...").classes("w-full p-4 border-2 border-gray-300 rounded-lg text-gray-800")
            chat_output = ui.label("").classes("mt-4 text-lg text-gray-800")

            def process_question():
                question = chat_input.value
                if question:
                    chat_output.set_text(f"AI Response: {query(question)}")

            ui.button("Submit", on_click=process_question).classes("bg-blue-500 hover:bg-blue-600 transition-all text-white px-6 py-3 rounded-lg shadow-md mt-2")




# App Header
with ui.header().classes("bg-blue-700 text-white p-8 text-center"):
    ui.label("HireSite - AI Resume Assistant").classes("text-5xl font-extrabold")




# Run App
ui.run(title="HireSite - AI Resume Tool", dark=False)
