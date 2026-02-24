from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

llm = init_chat_model("gemini-2b",model_provider="google",temperature=0.8,max_tokens=500)

response = llm.invoke([HumanMessage(content="Generate a haiku about the ocean")])

print(response.content)
