from pymongo import MongoClient
import certifi
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
import argparse
from dotenv import load_dotenv

def get_connection(client: MongoClient) -> tuple:
    """
    Establishes and returns MongoDB connection and returns a tuple containing the database and collection
    Arguments:
        client: MongoClient - The MongoClient instance used to connect to the Mongo
    Returns:
        Tuple containing the database and collection
    """
    dbname = os.getenv("MONGODB_DB_NAME")
    collectionname = os.getenv("MONGODB_COLLECTION_NAME")
    db = client[dbname]
    collection = db[collectionname]
    return db, collection

def search_documents(client, text, k):
    __, collection = get_connection(client)
    vector_store = MongoDBAtlasVectorSearch(
        embedding=OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL")),
        collection=collection,
        index_name=os.getenv("MONGO_ATLAS_SEARCH_INDEX"),
        relevance_score_fn="cosine"
    )
    return vector_store.similarity_search(text, k=k) 

def main():
    parser = argparse.ArgumentParser(description='Your script description')
    parser.add_argument('-q', '--query', default=True, help='Query string to search for in the vector store', type=str)
    
    load_dotenv()
    client = MongoClient(os.getenv("MONGODB_URI", ""), tlsCAFile=certifi.where())
    results = search_documents(client, parser.parse_args().query, 5)
    for doc in results:
        print(f"Text: {doc.page_content}")
    client.close()

if __name__ == "__main__":
    main()