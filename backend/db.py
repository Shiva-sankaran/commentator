import pymongo
# conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/test"
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/annotation_tool?retryWrites=true&w=majority"

# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']

# sentences_collection = database.get_collection('sentences')
user_collection = database.get_collection('users')

user = user_collection.find()
user = list(user)

for s in user:
    print(s['username'])
