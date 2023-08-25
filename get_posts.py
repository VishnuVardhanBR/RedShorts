import praw
import json
import datetime
import random
from praw.exceptions import RedditAPIException
import os
from dotenv import load_dotenv

load_dotenv()
# JSON file to store fetched post details
json_file = "fetched_posts.json"

def load_fetched_posts():
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_fetched_posts(posts):
    with open(json_file, "w") as f:
        json.dump(posts, f, indent=4)

def get_random_subreddit_from_file(file_path):
    with open(file_path, "r") as f:
        subreddits = f.read().splitlines()
    return random.choice(subreddits)

def get_top_video_post(subreddit_name):
    fetched_posts = load_fetched_posts()

    reddit = praw.Reddit(
        user_agent=os.environ.get("REDDIT_USER_AGENT"),
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        read_only=os.environ.get("REDDIT_READ_ONLY") == "True"
    )

    try:
        if subreddit_name == "0":
            subreddit_name = get_random_subreddit_from_file("subreddits.txt")

        # Get the specified subreddit
        subreddit = reddit.subreddit(subreddit_name)

        # Fetch the top posts of the past 7 days
        top_posts = subreddit.top(time_filter="week")

        for post in top_posts:
            post_id = post.id

            # Check if the post ID has already been fetched
            if not any(post_details["post_id"] == post_id for post_details in fetched_posts):
                if post.is_video and not post.over_18 and post.score >= 1000:
                    post_details = {
                        "post_id": post.id,
                        "title": post.title,
                        "subreddit": post.subreddit.display_name,
                        "url": post.url,
                        "date": str(datetime.datetime.now()),
                        "upvotes": post.score
                    }

                    fetched_posts.append(post_details)
                    save_fetched_posts(fetched_posts)
                    return post_details
                else:
                    print("Skipping non-video or NSFW post. Fetching the next top post.")
            else:
                print("Duplicate post found. Fetching the next top post.")
    except RedditAPIException as e:
        print("An error occurred:", e)
        return None
