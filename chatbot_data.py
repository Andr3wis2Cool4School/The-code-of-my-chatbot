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
connection = sqlite3.connect('./data/{}.db'.format(timeframe))
cursor = connection.cursor()

def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS parent_reply
    (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, 
    parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)""")

'''
WHY NEED 
Subreddit:
Different Subreddit may have different types of talking style
'''

def format_data(data):
    data = data.replace('\n', ' newlinechar ').replace('\r', ' newlinechar ').replace('"', "'") 
    # hope no one use newlinechar hahahha
    return data

def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            return result[0] # it return a list
        else: return False
    except Exception as e:
        print('find_parent', e)
        return False

if __name__ == '__main__':
    create_table()
    row_counter = 0 
    paired_rows = 0 
    dataPath = './data/RC_2015-01'

    '''
    row_counter: How many rows we have gone through
    paired_rows: How many parent and child pairs we come up with

    Because lots of times that the parent never been reply
    '''
    # Only Buffer 100
    with open (dataPath, buffering=100) as f:
        for row in f:
            print(row)
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            create_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']

            parent_data = find_parent(parent_id)


