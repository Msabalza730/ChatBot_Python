import os

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    AIMessagePromptTemplate,
    ChatMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

messages = [
    SystemMessage(content="You are a helpful assistant")
]

while True:
    user_input = input("You: ")
    messages.append(HumanMessage(content=user_input))
    ai_response = chat(messages=messages).content
    print("IA", ai_response)
    messages.append(AIMessage(content=ai_response))
