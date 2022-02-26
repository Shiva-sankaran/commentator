import pymongo
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/test"

# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']

sentences_collection = database.get_collection('sentences')

sentences_collection.insert_many([
    {'sid': 1, 'sentence': 'Hi, this is the first sentence'},
    {'sid': 2, 'sentence': '2nd Sentence in the database'},
    {'sid': 3, 'sentence': 'नमस्ते, यह शुभ है। यह एक एनोटेशन टूल है।'}
])
