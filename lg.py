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
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        print("API Response:", response)  # Debug print
        return response
    except Exception as e:
        print("API Error:", str(e))  # Debug print
        return f"Error: {str(e)}"
    
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
            "Your personal AI tool for all things CV. It helps recruiters sort through resumes, rank them based on quality, "
            "and provides personal advice with specific tips to improve your resume. It can also identify your strengths and weaknesses."
            ).classes("text-lg text-gray-800")
            
        # About the Makers Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            ui.label("About the Makers").classes("text-3xl font-extrabold text-blue-700 mb-4")
            ui.label("Avinash Karthik - Co-Founder and AI Specialist").classes("text-lg text-gray-700 font-semibold mb-2")
            ui.label(
                "Avinash is a passionate AI enthusiast and developer. He specializes in AI-driven applications and has a deep interest in machine learning. "
                "He is responsible for leading the development of HireSite's AI algorithms and ensuring the platform's powerful and accurate performance."
            ).classes("text-md text-gray-700")
            ui.label("Pranav Kaushik - Co-Founder and Backend Engineer").classes("text-lg text-gray-700 font-semibold mb-2")
            ui.label(
                "Pranav is a backend engineer with a knack for building scalable systems. He oversees the development of HireSite's backend architecture, " 
                "ensuring that all features run smoothly and efficiently. He is committed to delivering a seamless user experience with an emphasis on performance."
            ).classes("text-md text-gray-700 mb-4")


    with ui.tab_panel(two):
        # Expanded Features Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            ui.label("✨ Features").classes("text-3xl font-extrabold text-blue-700 mb-2")
            
            # Introduction to features
            ui.label(
                "HireSite offers a comprehensive suite of AI-powered tools designed to optimize and improve the resume "
                "review process for recruiters and job seekers alike. From ranking resumes based on quality to providing "
                "personalized advice, our platform takes your CV to the next level."
            ).classes("text-lg text-gray-700 mb-4")

            features = [
                ("AI-powered resume ranking", 
                 "Utilize advanced machine learning algorithms to rank resumes based on quality. The AI takes into account "
                 "key factors such as experience, skills, keywords, and formatting, ensuring that recruiters see the most "
                 "relevant and impactful resumes first."),
                 
                ("Personalized feedback on strengths & weaknesses", 
                 "Get actionable insights on your resume's strengths and areas for improvement. The AI identifies critical "
                 "elements that can make a resume stand out and suggests practical changes to increase the chances of landing "
                 "the perfect job."),
                 
                ("Resume quality analysis (keywords, experience, readability)", 
                 "Evaluate your resume's quality based on specific criteria such as keyword optimization, readability, and "
                 "overall experience alignment with the target job role. Our system highlights key sections that need refinement "
                 "and ensures your resume is polished and professional."),
                 
                ("Chat section for specific resume-related queries", 
                 "Have a specific question about your resume or need advice on a particular section? Use the AI-powered chat to "
                 "ask questions about your resume’s structure, content, or layout. The assistant provides tailored responses, "
                 "helping you improve your CV quickly."),
                 
                ("User-friendly UI for easy interaction", 
                 "Our platform is designed with ease of use in mind. With an intuitive interface and easy navigation, you can "
                 "upload resumes, interact with the AI assistant, and get instant feedback, making it perfect for users with "
                 "varying levels of tech proficiency."),
                 
                ("Automated formatting suggestions", 
                 "The AI not only reviews your resume’s content but also suggests improvements in formatting and presentation. "
                 "Ensure your resume looks professional with a clean, modern layout that recruiters will love."),
                 
                ("Keyword optimization for Applicant Tracking Systems (ATS)", 
                 "Our AI ensures your resume passes through ATS systems by analyzing it for relevant keywords that match the job "
                 "description. By optimizing your resume for ATS, you increase your chances of getting noticed by recruiters."),
                 
                ("Professional tips and industry-specific recommendations", 
                 "Receive specific resume improvement tips tailored to your industry. Whether you're in tech, healthcare, or finance, "
                 "our AI suggests the best ways to highlight your experience and skills, ensuring your resume aligns with industry standards."),
                 
                ("Interactive report generation", 
                 "Generate a detailed report that highlights all feedback, suggestions, and areas of improvement on your resume. "
                 "This report can be used to track your progress and ensure that you’re constantly enhancing your resume for future opportunities.")
            ]
            
            for feature, description in features:
                with ui.card().classes("p-4 bg-blue-50 rounded-lg shadow-md mb-4"):
                    ui.label(feature).classes("text-xl font-semibold text-blue-600 mb-2")
                    ui.label(description).classes("text-md text-gray-700")


    with ui.tab_panel(three):
        # Upload Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            with ui.dialog().props('full-width') as dialog:
                with ui.card():
                    content = ui.markdown()

            def handle_upload(e: events.UploadEventArguments):
                global uploaded_resume_text
                file_data = e.content.read()
                with fitz.open(stream=file_data, filetype="pdf") as doc:
                    uploaded_resume_text = "\n".join([page.get_text() for page in doc])
                print("Extracted Text:", uploaded_resume_text)  # Debug print
                content.set_content(uploaded_resume_text)
                dialog.open()

            ui.upload(on_upload=handle_upload).props('accept=.pdf').classes('max-w-full p-6 border-2 border-dashed border-gray-400 rounded-lg')

        # AI Review Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            ui.label("AI review").classes("text-3xl font-extrabold text-blue-700 mb-2")
            chat_output = ui.label("Here is our AI's review of your resume").classes("mt-4 text-lg text-gray-800")

            def process_question():
                global uploaded_resume_text
                if uploaded_resume_text:
                    question = '''rate this resume on a scale of 1-10, identify strengths and weaknesses,
                                tell me what to improve on and what is really good, 
                                give a rough estimate of the quality of companies I could get in to with this resume, 
                                be honest, dont try and sugarcoat and make sure to give credit where credit is due
                                also dont forget to use bullet points to give a clean readable output
                                also format it after each point, then press enter
                                there should be an empty line between each new point'''
                    response = query(f"{question}\n\nResume Content:\n{uploaded_resume_text}")
                    print("Response to set:", response)  # Debug print
                    ui.button(f"AI Response: {response}")
                else:
                    ui.button("Please upload a resume first!")

            ui.button("Give thoughts", on_click=process_question).classes("bg-blue-500 hover:bg-blue-600 transition-all text-white px-6 py-3 rounded-lg shadow-md mt-2")




    with ui.tab_panel(four):
        # Upload Section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            with ui.dialog().props('full-width') as dialog:
                with ui.card():
                    content = ui.markdown()

            def handle_upload(e: events.UploadEventArguments):
                global uploaded_resume_text
                file_data = e.content.read()
                with fitz.open(stream=file_data, filetype="pdf") as doc:
                    uploaded_resume_text += "\n".join([page.get_text() for page in doc])
                print("Extracted Text:", uploaded_resume_text)  # Debug print
                content.set_content(uploaded_resume_text)
                dialog.open()

            ui.upload(on_upload=handle_upload, multiple=True).props('accept=.pdf').classes('max-w-full p-6 border-2 border-dashed border-gray-400 rounded-lg')

        # Ranking section
        with ui.card().classes("m-4 p-6 rounded-xl bg-white shadow-md border border-gray-300"):
            ui.label("Rankings").classes("text-3xl font-extrabold text-blue-700 mb-2")
            chat_output = ui.label("Here are your uploaded resumes with a rating and in order").classes("mt-4 text-lg text-gray-800")

            def process_question():
                global uploaded_resume_text
                if uploaded_resume_text:
                    question = '''rank each of these resumes on a scale of 1-10 and return them in order form best to worst'''
                    response = query(f"{question}\n\nResume Content:\n{uploaded_resume_text}")
                    print("Response to set:", response)  # Debug print
                    ui.button(f"AI Response: {response}")
                else:
                    ui.button("Please upload a resume first!")

            ui.button("Rank Them", on_click=process_question).classes("bg-blue-500 hover:bg-blue-600 transition-all text-white px-6 py-3 rounded-lg shadow-md mt-2")











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
