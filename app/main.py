from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import logging

from app.ml_model import predict_churn
from app.sentiment import get_sentiment
from app.openai_client import get_gpt_reply, send_message_to_user
from app.rule_engine import evaluate_rules

app = FastAPI()

# ✅ Correct CORS middleware
origins = [
    "http://localhost:3000",  # React local dev
    # "https://proactive-ai-agent.onrender.com"  # add here if you deploy frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # use list, not "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load rules
BASE_DIR = os.path.dirname(__file__)
rules_path = os.path.join(BASE_DIR, "rules.json")
with open(rules_path) as f:
    rules = json.load(f)["rules"]

@app.post("/api/events")
async def process_event(request: Request):
    try:
        data = await request.json()
        user_message = data.get("last_user_message", "")
        inactivity_seconds = data.get("inactivity_seconds", 0)

        sentiment = get_sentiment(user_message)
        proactive_message = None

        for rule in rules:
            cond = rule["condition"]
            if sentiment == cond["sentiment"] and inactivity_seconds > cond["inactivity_greater_than"]:
                proactive_message = rule["proactive_message"]
                break

        bot_reply = get_gpt_reply(user_message)

        return {
            "bot_reply": bot_reply,
            "sentiment": sentiment,
            "proactive_message": proactive_message
        }
    except Exception as e:
        logging.error(f"Error processing event: {e}")
        return {"error": str(e)}

