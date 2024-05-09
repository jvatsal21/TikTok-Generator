import praw
import os

reddit = praw.Reddit(
    client_secret=os.environ["REDDIT_API_KEY"],
    client_id=os.environ["REDDIT_CLIENT_ID"],
    user_agent=os.environ["REDDIT_USER_AGENT"]
)

def find_aita():
    subreddit_aita = reddit.subreddit("AmItheAsshole")

    top_daily_posts = subreddit_aita.top('day', limit=1)

    text = ""

    for post in top_daily_posts:
        # print("Title:", post.title)
        # print("Score:", post.score)
        # print("URL:", post.url)
        text += post.selftext
        text += "\n---\n"

    return text

print(find_aita())