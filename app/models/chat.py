from pydantic import BaseModel

class ReassuranceMultiResponse(BaseModel):
    bot_message_1: str
    bot_message_2: str
    bot_message_3: str
    bot_message_4: str
    bot_message_5: str


class SearchResponseRate(BaseModel):
    message: str
    rating: int


class ReassuranceSearchResponse(BaseModel):
    stored_message_1: SearchResponseRate
    stored_message_2: SearchResponseRate
    stored_message_3: SearchResponseRate
    stored_message_4: SearchResponseRate
    stored_message_5: SearchResponseRate
    stored_message_6: SearchResponseRate
    stored_message_7: SearchResponseRate
    stored_message_8: SearchResponseRate
    stored_message_9: SearchResponseRate
    stored_message_10: SearchResponseRate