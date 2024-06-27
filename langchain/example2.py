import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from langchain.chat_models import ChatOpenAI

load_dotenv()

llm_claude3 = ChatAnthropic(model='claude-3-opus-20240229')

llm_claude3.invoke("What is langchain?").content
# api_key = os.getenv("ANTHROPIC_API_KEY")

# chat_model = ChatAnthropic(anthropic_api_key=api_key)

# result = chat_model.predict("Hello!!")

# print(result)