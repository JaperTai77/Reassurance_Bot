from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.v1.repositories.chat import Chat

router = APIRouter(tags=["chat"])

@router.get("/getratedresponse")
async def get_rated_response(text: str):
    chat_client = Chat()
    response = chat_client.get_rated_reassurance_response(text)
    response_json = jsonable_encoder({"messages": response})
    return JSONResponse(content=response_json, status_code=200)

@router.get("/gettopresponse")
async def get_top_response(text: str):
    chat_client = Chat()
    response = chat_client.get_random_message_and_revised(text)
    response_json = jsonable_encoder({"messages": response})
    return JSONResponse(content=response_json, status_code=200)