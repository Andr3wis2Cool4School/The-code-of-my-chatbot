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

def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        print('find_existing_score', e)
        return False

def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]':
        return False
    elif data == '[removed]':
        return False
    else: return True

def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        cursor.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                cursor.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []


def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s-replace-comment insertion',str(e))

def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s-has-parent-insertion',str(e))

def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s insertion no parent',str(e))

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
            #print(row)
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            create_utc = row['created_utc']
            score = row['score']
            comment_id = row['name']
            subreddit = row['subreddit']
            parent_data = find_parent(parent_id)

            '''
            The comment at least have one upvote
            If the parent has already have one comment 
            get the comment has more score
            '''
            if score >= 2:
                if acceptable(body):
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, create_utc, score)
                    
                    else:
                        if parent_data:
                            sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, create_utc, score)
                            paired_rows += 1
                
                        else:
                            sql_insert_no_parent(comment_id, parent_id, body, subreddit, create_utc, score)

            if row_counter % 10000 == 0:
                print('Total rows head: {}, paired row: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now)))





