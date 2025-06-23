import os
import praw
from dotenv import load_dotenv

load_dotenv()
def fetch_reddit_data(topic, limit=10):
    try:
        reddit = praw.Reddit(client_id = os.getenv("REDDIT_CLIENT_ID"),client_secret = os.getenv("REDDIT_CLIENT_SECRET"), user_agent = os.getenv("REDDIT_USER_AGENT"))
        reddit.read_only = True
        # fetch put and reddit read node
        posts = []
        subreddit = reddit.subreddit('all')
        for submission in subreddit.search(topic, sort= 'new', time_filter='all', limit=limit):
            posts.append({
                'title': submission.title,
                'content': submission.selftext or 'no content available',
                "url": submission.url()
            })
        return posts
    except Exception as e:
        print(f"Error fetching data from Reddit:{e}")
        return {}
    