from pymongo import MongoClient
import certifi
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo.operations import SearchIndexModel
from langchain_openai import OpenAIEmbeddings

from app.core.config import Variable

class MongoDBOperations:
    def __init__(self):
        self.mongo_uri = Variable.MONGODB_URI
        self.db_name = Variable.MONGODB_DB_NAME
        self.collection_name = Variable.MONGODB_COLLECTION_NAME
        self.index_name = Variable.MONGO_ATLAS_SEARCH_INDEX
        self.embedding_model = Variable.OPENAI_EMBEDDING_MODEL
        self.client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def close(self):
        self.client.close()

    def create_index(self) -> str:
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
            name=self.index_name,
            type="vectorSearch"
        )
        self.collection.create_search_index(model=search_index_model)
        return "Search index created!"

    def add_documents(self, text: str, metadata: str) -> str:
        vector_store = MongoDBAtlasVectorSearch(
            embedding=OpenAIEmbeddings(model=self.embedding_model),
            collection=self.collection,
            index_name=self.index_name,
            relevance_score_fn="cosine"
        )
        if text != "" or metadata != "":
            vector_store.add_texts(texts=[text], metadatas=[{"source":metadata}])
            return f"'{text}' added to the vector store successfully!"
        return "No data!"

    def get_all_texts(self) -> list:
        all_texts = []
        collection_name = self.collection_name
        collection = self.db[collection_name]
        documents = collection.find()
        for doc in documents:
            text = doc.get("text", "")
            if text:
                all_texts.append(str(text))
        return all_texts

    def search_documents(self, text:str, k:int=5) -> list:
        vector_store = MongoDBAtlasVectorSearch(
            embedding=OpenAIEmbeddings(model=self.embedding_model),
            collection=self.collection,
            index_name=self.index_name,
            relevance_score_fn="cosine"
        )
        return vector_store.similarity_search(text, k=k)