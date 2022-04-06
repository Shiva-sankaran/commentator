import pymongo
conn_str = "mongodb://localhost:27017"

client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']

database.create_collection('users')
database.create_collection('sentences')
