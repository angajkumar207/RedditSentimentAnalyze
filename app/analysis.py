import os
import nltk
nltk.data.path.append(os.path.join(os.getcwd(),'nltk_data'))
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(posts):
    results = []
    for post in posts:
        # get sentiment scores
        sentiment_score = sia.polarity_scores(post['content'])['compound']
        # classific sentiment based on the compounds score
        sentiment = 'POSITIVE' if sentiment_score >= 0 else 'NEGATIVE'

        # append results:
        results.append({
            'title': post['title'],
            'content':post['content'],
            'sentiment': sentiment,
            'score': sentiment_score,
        })

    return results