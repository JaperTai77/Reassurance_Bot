from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo.operations import SearchIndexModel
from langchain_openai import OpenAIEmbeddings
import os
import argparse

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

def create_index(client):
    __, collection = get_connection(client)
    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1536,
                    "similarity": "cosine",
                    "quantization": "scalar"
                }
            ]
        },
        name=os.getenv("MONGO_ATLAS_SEARCH_INDEX"),
        type="vectorSearch"
    )
    result = collection.create_search_index(model=search_index_model)
    return None


def add_documents(client, texts, metadatas):
    __, collection = get_connection(client)
    vector_store = MongoDBAtlasVectorSearch(
        embedding=OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL")),
        collection=collection,
        index_name=os.getenv("MONGO_ATLAS_SEARCH_INDEX"),
        relevance_score_fn="cosine"
    )
    _ = vector_store.add_texts(
        texts=texts, metadatas=metadatas
    )
    return None
    
    
def main():
    parser = argparse.ArgumentParser(description='Your script description')
    parser.add_argument('-i', '--index', default=False, help='Whether the vector index is created or not', type=bool)
    parser.add_argument('-t', '--text', help='Input text to add to the vector store', type=str, required=True)
    texts = [
        parser.parse_args().text
    ]
    metadatas = [
        {"source": "web"}
    ]
    
    load_dotenv()
    client = MongoClient(os.getenv("MONGODB_URI", ""), tlsCAFile=certifi.where())
    add_documents(client, texts, metadatas)
    if parser.parse_args().index:
        create_index(client)
    client.close()

if __name__ == "__main__":
    main()