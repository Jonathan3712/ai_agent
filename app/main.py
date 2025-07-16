from fastapi import FastAPI, Request
import json
import os
import logging

from app.ml_model import predict_churn
from app.sentiment import get_sentiment
from app.openai_client import get_gpt_reply, send_message_to_user
from app.rule_engine import evaluate_rules
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Allow React frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace "*" with actual React app URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

# Load rules at startup
BASE_DIR = os.path.dirname(__file__)
rules_path = os.path.join(BASE_DIR, "rules.json")
with open(rules_path) as f:
    rules = json.load(f)['rules']  # <-- load the list directly

print("Loaded rules:", rules)


@app.post("/api/events")
async def process_event(request: Request):
    try:
        data = await request.json()
        user_message = data.get("last_user_message", "")
        inactivity_seconds = data.get("inactivity_seconds", 0)

        logging.info(f"Received message: '{user_message}', inactivity: {inactivity_seconds}")

        sentiment = get_sentiment(user_message)
        p_churn = predict_churn(user_message)
        logging.info(f"Predicted churn: {p_churn}, sentiment: {sentiment}")

        proactive_message = None

        # Use inactivity + sentiment rules
        for rule in rules:
            cond = rule["condition"]
            if sentiment == cond["sentiment"] and inactivity_seconds > cond["inactivity_greater_than"]:
                proactive_message = rule["proactive_message"]
                break

        # Use churn-based rules too
        churn_action = evaluate_rules(p_churn, sentiment)
        if churn_action:
            proactive_message = churn_action

        bot_reply = get_gpt_reply(user_message)

        return {
            "bot_reply": bot_reply,
            "sentiment": sentiment,
            "predicted_churn": p_churn,
            "proactive_message": proactive_message
        }
    except Exception as e:
        logging.error(f"Error processing event: {e}")
        return {"error": str(e)}