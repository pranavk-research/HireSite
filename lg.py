import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("groq_api_key"),
)

test = "showering"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of" + test,
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)