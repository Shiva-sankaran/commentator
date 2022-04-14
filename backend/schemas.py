import pymongo
# conn_str = "mongodb://localhost:27017"
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/annotation_tool?retryWrites=true&w=majority"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']

database.create_collection('users')
database.create_collection('sentences')
print('Schemas Created')
