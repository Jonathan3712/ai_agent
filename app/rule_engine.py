import os
import json

BASE_DIR = os.path.dirname(__file__)
rules_path = os.path.join(BASE_DIR, "rules.json")
print("Looking for rules.json at:", rules_path)
print("Exists:", os.path.exists(rules_path))

with open(rules_path) as f:
    RULES = json.load(f)['rules']

def evaluate_rules(p_churn: float, sentiment: str):
    """
    Example usage:
    p_churn = 0.25
    sentiment = 'negative'
    action = evaluate_rules(p_churn, sentiment)
    """
    for rule in RULES:
        cond = rule.get('conditions') or rule.get('condition')  # handle both names
        churn_check = eval(f"{p_churn} {cond.get('p_churn', '< 1')}")  # safe default
        sentiment_check = (sentiment == cond.get('sentiment'))
        if churn_check and sentiment_check:
            return rule.get('action') or rule.get('proactive_message')
    return None
