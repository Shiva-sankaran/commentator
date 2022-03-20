import csv
# import pymysql.cursors

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='root',
#                              database='annotation_sql',
#                              cursorclass=pymysql.cursors.DictCursor)

# cur = connection.cursor()
# result = cur.execute("SELECT * FROM UserTagList WHERE uid = 1")
# data = cur.fetchall()
# print(data)
# cur.close()


# index = 0
# with open('./csv/data.csv', 'w', encoding='utf-8', newline="") as f:
#     writer = csv.writer(f)

#     writer.writerow(['utid', 'uid', 'sid', 'stag'])
#     for i in data:
#         data_row = i
#         row = [data_row['utid'], data_row['uid'],
#                data_row['sid'], data_row['stag']]
#         print(row)
#         writer.writerow(row)


from tokenize import group
import pandas as pd
import pymongo
import os

# conn_str = os.environ.get('DATABASE_URL')
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/annotation_tool?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']

print(database.list_collection_names())

users_collection = database.get_collection('users')

user = users_collection.find({'username': 'test'})
# user = users_collection.find()
user = list(user)
sentTag = user[0]['sentTag']

with open('./csv/data.csv', 'w', encoding='utf-8', newline="") as f:
    writer = csv.writer(f)

    writer.writerow(['grammar', 'time', 'tag', 'link'])

    for sentence in sentTag:
    # print(sentence)
        grammar = sentence[0]
        time = sentence[1]
        tag = sentence[2]
        link = sentence[3]
        row = [grammar, time, tag, link]
        # break
    # for i in data:
    #     data_row = i
    #     row = [data_row['utid'], data_row['uid'],
    #            data_row['sid'], data_row['stag']]
    #     print(row)
        writer.writerow(row)
        break