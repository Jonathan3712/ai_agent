from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.ml_model import predict_churn
from app.sentiment import analyze_sentiment
from app.rule_engine import evaluate_rules
from app.openai_client import send_message_to_user

app = FastAPI()

class Event(BaseModel):
    inactivity_seconds: int
    last_user_message: str

@app.post("/api/events")
async def handle_event(event: Event):
    p_churn = predict_churn(event.inactivity_seconds)
    sentiment = analyze_sentiment(event.last_user_message)
    action = evaluate_rules(p_churn, sentiment)

    if action == "send_proactive_message":
        proactive_text = "Hey! Noticed you might need help. Can I assist?"
        ai_response = send_message_to_user(proactive_text)
        return {"proactive_message": ai_response}

    return {"message": "No proactive action needed"}
