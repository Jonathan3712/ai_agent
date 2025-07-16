from textblob import TextBlob

def get_sentiment(user_message: str) -> str:
    """
    Uses TextBlob to get sentiment polarity.
    Returns: 'positive', 'neutral', or 'negative'
    """
    blob = TextBlob(user_message)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"
