import praw

reddit = praw.Reddit(client_id = '8LZ79zkDa_nbaQ',
                     client_secret = 'EcvHMHYRo038G92UIhe1tPE5bUGT0Q',
                     username = 'Little-Yam7288',
                     password = 'yepandrewluo123',
                     user_agent = 'china')

subreddit = reddit.subreddit('python')

hot_python = subreddit.hot(limit=5)

for submission in hot_python:
    print(submission.title)