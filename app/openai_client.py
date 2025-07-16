import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_reply(user_message: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly support AI."},
            {"role": "user", "content": user_message}
        ]
    )
    return completion.choices[0].message.content

def send_message_to_user(message):
    print("Simulated sending message to user:", message)
    # Later: real send logic (websocket, email, etc.)
