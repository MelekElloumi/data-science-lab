from pymongo import MongoClient

def send_to_mongo(data):
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    db = client["Smart_Conseil"]
    col = db["Facebook_Connector"]
    col.insert_one(data)
