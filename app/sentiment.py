# from transformers import pipeline
#
# sentiment_pipeline = pipeline("sentiment-analysis")
#
# def analyze_sentiment(text: str) -> str:
#     result = sentiment_pipeline(text)[0]
#     label = result['label'].lower()  # e.g., POSITIVE, NEGATIVE
#     return label
from textblob import TextBlob

def get_sentiment(text: str):
    """
    Analyze sentiment using TextBlob.
    Returns: 'positive', 'negative', or 'neutral'
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"
