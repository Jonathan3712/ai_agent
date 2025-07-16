def predict_churn(user_message: str) -> float:
    """
    Dummy churn predictor based on message length.
    Replace later with real ML model.
    """
    if len(user_message) < 20:
        return 0.8  # high churn risk
    return 0.2  # low churn risk
