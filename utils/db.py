from pymongo import MongoClient

def initialize_db(uri, db_name, collection_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]
