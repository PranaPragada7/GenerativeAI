from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage 

# Use gemini-2.5-flash as it is the current standard
# This avoids the "NotFound" error on the v1beta endpoint
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

try:
    res = model.invoke([HumanMessage(content="What is the capital of Spain?")])
    print(res.content)
except Exception as e:
    print(f"Error: {e}")