import sqlite3
import json
from datetime import datetime

timeframe = '2015-01'
'''
When you know you are going to working with millions of rows
You don't want to insert row one by one
Instead you want to build up a big transaction
just do it all at once
'''
sql_transaction = []
connection = sqlite3.connect('{}.db'.format(timeframe))
cursor = connection.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply
    (parent_id TEXT PRIMARY, comment_id TEXT UNIQUE, 
    parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)""")

'''
Subreddit:
Different Subreddit may have different types of talking style
'''

if __name__ == '__main__':
    create_table()





