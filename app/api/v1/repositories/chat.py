import openai
import json
import random

from app.models.chat import ReassuranceMultiResponse, ReassuranceSearchResponse
from app.core.config import Variable
from app.api.v1.repositories.vectorstore_operation import MongoDBOperations

class Chat():
    def __init__(self):
        openai.api_key = Variable.OPENAI_API_KEY
        self.chat_model = Variable.OPENAI_CHAT_MODEL
        self.client = openai.OpenAI()
        self.simple_assurance_sys_prompt = """
        你會收到一段文字，設想自己為他的女朋友、情人、老婆，會用溫柔又貼心的話來回應。
        使用幽默風趣的口吻，對方喜歡有灰心一笑的感覺，回應盡量有押韻或諧音。
        你是一個開心果，到哪裡都讓人開心。
        """
        self.simple_assurance_usr_prompt = """
        收到了下面這段話:{text}，分享5條幽默的回應給我參考。
        """
        self.rated_assurance_sys_prompt = """
        設想自己為他的女朋友、情人、老婆，對這些回應進行評分，根據幽默跟體貼程度評分，如果有押韻或諧音也會提高評分
        評分分數為1到10分，10分表示最好
        """
        self.rated_assurance_usr_prompt = """
        你收到這段文字{text}，下面是一些回應，請幫我評分並挑最高分的5個就好。
        以下是根據上面那段文字的回應，回應是用\n分隔:

        {response}

        """
        self.final_assurance_sys_prompt = """
        設想自己為他的女朋友、情人、老婆，溫柔又風趣。
        """
        self.final_assurance_usr_prompt = """
        你會收到一段<文字>跟<回應>，<文字>是對方表達的問題或心情，根據<回應>的內容，重新加工出一段稍微長一點，且風趣的回應。
        <文字>:{text}
        <回應>:{response}
        """

    def _get_simple_reassurance_response(self, text:str)->list:
        completion = self.client.chat.completions.parse(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": self.simple_assurance_sys_prompt},
                {"role": "user", "content": self.simple_assurance_usr_prompt.format(text=text)},
            ],
            temperature=1.0,
            response_format=ReassuranceMultiResponse
        )
        response = completion.choices[0].message.content
        response_json = json.loads(response)
        return list(response_json.values())
    
    def _get_vector_search(self, text:str, k:int=5)->list:
        client = MongoDBOperations()
        vector_search_responses = client.search_documents(text=text, k=k)
        client.close()
        return [res.page_content for res in vector_search_responses]
    
    def get_rated_reassurance_response(self, text:str)->dict:
        bot_response = self._get_simple_reassurance_response(text)
        search_response = self._get_vector_search(text)
        combine_response = "\n".join(bot_response+search_response)
        completion = self.client.chat.completions.parse(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": self.rated_assurance_sys_prompt},
                {"role": "user", "content": self.rated_assurance_usr_prompt.format(text=text, response=combine_response)},
            ],
            temperature=0.8,
            response_format=ReassuranceSearchResponse
        )
        rated_response = completion.choices[0].message.content
        return json.loads(rated_response)
    
    def _rank_messages_by_rating(self, messages:dict)->list:
        sorted_messages = sorted(
            [(msg_data["rating"], msg_data["message"]) for msg_data in messages.values()],
            key=lambda x: x[0],
            reverse=True
        )
        return [message for _, message in sorted_messages]

    def get_random_message_and_revised(self, text:str) -> dict:
        rated_response = self.get_rated_reassurance_response(text)
        ranked_messages = self._rank_messages_by_rating(rated_response)
        def weighted_random_choice(items: list) -> str:
            # Assign weights: higher for earlier items (e.g., linear decay)
            weights = [len(items) - i for i in range(len(items))]
            return random.choices(items, weights=weights, k=1)[0]
        random_response = weighted_random_choice(ranked_messages)

        final_response = self.client.responses.create(
            model=self.chat_model,
            instructions = self.final_assurance_sys_prompt,
            input = self.final_assurance_usr_prompt.format(text=text, response=random_response),
            temperature=0.8
        )
        return {"Original Response": random_response, "Revised Response": final_response.output_text}

