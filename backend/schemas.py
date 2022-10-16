import pymongo
# conn_str = "mongodb://localhost:27017"
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/annotation_tool?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']

try:
    database.create_collection('users')
except:
    print("Users Already exists")

try:
    database.create_collection('sentences')
except:
    print("Sentences Already exists")

try:
    database.create_collection('lid')
except:
    print("LID Already exists")

try:
    database.create_collection('sentiment')
except:
    print("Sentiment Already exists")

print('Schemas Created')
