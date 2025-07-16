import json

with open("app/rules.json") as f:
    RULES = json.load(f)['rules']

def evaluate_rules(p_churn: float, sentiment: str):
    for rule in RULES:
        cond = rule['conditions']
        churn_check = eval(f"{p_churn} {cond['p_churn']}")
        sentiment_check = (sentiment == cond['sentiment'])
        if churn_check and sentiment_check:
            return rule['action']
    return None
