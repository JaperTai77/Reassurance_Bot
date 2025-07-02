from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import json

class ReassuranceResponse(BaseModel):
    message_1: str
    message_2: str
    message_3: str
    message_4: str
    message_5: str
    message_6: str
    message_7: str
    message_8: str

def get_model():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    client = openai.OpenAI()
    return client

def get_completion(client, prompt):
    completion = client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": "你會安撫你對象的情緒，並提供支持和鼓勵，並幽默且風趣的回應,回應盡量有押韻或諧音。"},
            {"role": "user", "content": f"當別人對你說{prompt}，身為情人要如何幽默回應？8條幽默回應"},
        ],
        temperature=0.8,
        response_format=ReassuranceResponse
    )
    return completion

if __name__ == "__main__":
    load_dotenv()
    client = get_model()
    prompt = "我今天感覺很沮喪"
    response = get_completion(client, prompt)

    message = response.choices[0].message
    print(json.loads(message.content))
        