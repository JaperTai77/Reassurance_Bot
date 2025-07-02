from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.v1.repositories.vectorstore_operation import MongoDBOperations

router = APIRouter(tags=["vectorstoreoperation"])

@router.post("/createindex")
async def create_index():
    client = MongoDBOperations()
    response = client.create_index()
    client.close()
    response_json = jsonable_encoder({"messages": response})
    return JSONResponse(content=response_json, status_code=200)

@router.post("/adddocuments")
async def add_documents(text: str, metadata: str):
    client = MongoDBOperations()
    response = client.add_documents(text=text, metadata=metadata)
    client.close()
    response_json = jsonable_encoder({"messages": response})
    return JSONResponse(content=response_json, status_code=200)

@router.get("/getalltexts")
async def get_all_texts():
    client = MongoDBOperations()
    response = client.get_all_texts()
    client.close()
    response_json = jsonable_encoder({"messages": response})
    return JSONResponse(content=response_json, status_code=200)

@router.get("/getsearchtexts")
async def get_search_texts(text: str, k: int = 5):
    client = MongoDBOperations()
    response = client.search_documents(text=text, k=k)
    client.close()
    response_list = [res.page_content for res in response]
    response_json = jsonable_encoder({"messages": response_list})
    return JSONResponse(content=response_json, status_code=200)