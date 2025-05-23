import praw
import requests
import datetime
from sqlalchemy import create_engine, text
import psycopg2
from datetime import datetime, timezone

reddit = praw.Reddit(
    client_id = '9MenyGXWR4nZa8dkqnRM8g',
    client_secret = 'jhSv0Tdcn9eOXPaTO_HtrlHZE7rVFw',
    user_agent = "stocksentiment by u/FennelComfortable",
    username = "FennelComfortable497",
    password = 'Calliope@2019!'
)

engine = create_engine("postgresql://postgres:WjValpnjgoYyLCVqoPrZhiSbVwdbgbUh@roundhouse.proxy.rlwy.net:44826/railway")
platform = 'Reddit'

reddit.read_only = True

# Define your date range
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 7, 29)

# Convert dates to Unix timestamps
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# Define your search parameters
subreddit_name = 'wingstop'
topic = 'wingstop'

# Fetch submissions from the subreddit
subreddit = reddit.subreddit(subreddit_name)
posts = []

# Use Reddit API to get submissions and filter by date
for submission in subreddit.top(limit=None):  # Adjust the limit as needed
    if start_timestamp <= submission.created_utc <= end_timestamp:
        posts.append(submission)

print(len(posts))

# Print the filtered posts
for post in posts:
    sub_title = post.title
    post_date = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
    format_date = post_date.strftime('%Y-%m-%d')
    likes = post.score
    sub_id = post.id
    sub_text = post.selftext
    content = sub_title + ' - ' + sub_text
    print(format_date)

    with engine.begin() as trans:
        print('Inserting into database')
        trans.execute(text("""
                            INSERT INTO posts (platform, topic, post, likes, date_posted, sub_id, subreddit) 
                            VALUES (:platform, :topic, :post, :likes, :date_posted, :sub_id, :subreddit)
                        """),
                        {'platform':platform,
                        'topic':topic,
                        'post':content,
                        'likes':likes,
                        'date_posted':format_date,
                        'sub_id':sub_id,
                        'subreddit':subreddit_name})
    
    #print(f"Content:{content}")
    #print(f"Post Score: {post.score}, Post Comments: {post.num_comments}")