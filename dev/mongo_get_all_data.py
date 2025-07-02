from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

def get_all_texts_from_mongodb():
    # Connect to MongoDB
    client = MongoClient(os.getenv("MONGODB_URI", ""), tlsCAFile=certifi.where())
    db = client[os.getenv("MONGODB_DB_NAME", "")]

    all_texts = []

    # List all collections
    collections = db.list_collection_names()

    for collection_name in collections:
        collection = db[collection_name]
        # Fetch all documents in the collection
        documents = collection.find()
        for doc in documents:
            # Extract "text" field and convert to string if exists
            text = doc.get("text", "")
            if text:
                all_texts.append(str(text))

    return all_texts

if __name__ == "__main__":
    texts = get_all_texts_from_mongodb()
    for t in texts:
        print(t)
