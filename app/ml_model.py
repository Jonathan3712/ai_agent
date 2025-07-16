def predict_churn(inactivity_seconds: int) -> float:
    # Simple logic: longer inactivity → higher churn
    return min(1.0, inactivity_seconds / 300)  # e.g., >5min = 1.0
