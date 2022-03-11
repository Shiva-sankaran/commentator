from tokenize import group
import pandas as pd
import pymongo
# # conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/test"
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/annotation_tool?retryWrites=true&w=majority"

# # set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']

sentences_collection = database.get_collection('sentences')
# user_collection = database.get_collection('users')

# user = user_collection.find()
# user = list(user)

# for s in user:
#     print(s['username'])


df = pd.read_csv('data.csv')
df = df['Sentence']

# rows = sentences_collection.find().sort('sid', pymongo.DESCENDING).limit(1)
# rows = list(rows)
# rows = rows[0]
# last_row_id = rows['sid']
last_row_id = 0
print(last_row_id)

# for sent in df:
#     print(sent)

for sent in range(len(df)):
    last_row_id += 1

    print(df[sent])
    sentences_collection.insert_one({
        'sentence': df[sent],
        'sid': last_row_id
    })

print('Task Finished')