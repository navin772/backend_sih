import pymongo

# Initialize MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["minhash_db"]
collection = db["minhash_collection"]

# Use the find() method to retrieve all documents in the collection
cursor = collection.find()

# Iterate through the cursor and print each document
for document in cursor:
    print(document)
