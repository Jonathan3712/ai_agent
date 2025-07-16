import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def send_message_to_user(message: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly support agent."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content
