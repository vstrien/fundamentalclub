from typing import Any, Dict
from openai import OpenAI
import requests
import dotenv
import os

client = OpenAI()


dotenv.load_dotenv()
DATABASE_INTERFACE_BEAR_TOKEN = os.getenv("DATABASE_INTERFACE_BEAR_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatGPT():
    def __init__(self, api_key, role):
        self.api_key = api_key
        self.role = role

    def call_chatgpt_api(self, user_question: str) -> str:
        # Send a request to the GPT API
        messages = [{
            "role": "system",
            "content": self.role,
        },
        {
            "role": "user",
            "content": user_question
        }]
        response = client.chat.completions.create(model="gpt-4-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.7)
        return response.choices[0].message.content
    
class Pinecone():
    def __init__(self, bearer_token, url = "http://0.0.0.0:8000/query"):
        self.bearer_token = bearer_token
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {self.bearer_token}",
        }

    def query_database(self, query_prompt: str) -> Dict[str, Any]:
        """
        Query vector database to retrieve chunk with user's input questions.
        """

        data = {"queries": [{"query": query_prompt, "top_k": 5}]}

        response = requests.post(self.url, json=data, headers=self.headers)

        if response.status_code == 200:
            result = response.json()
            # process the result
            return result
        else:
            raise ValueError(f"Error: {response.status_code} : {response.content}")
