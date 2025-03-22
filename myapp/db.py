from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.krishnan
col2 = db.col2  # Ensure col2 is correctly defined
