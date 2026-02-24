import sys
import google.generativeai as genai
import langchain_google_genai
from pydantic import BaseModel

print("--- Environment Check ---")
print(f"Python Version: {sys.version}")
print(f"Google GenerativeAI installed: {genai.__version__}")
print("Pydantic is working correctly.")
print("LangChain Google GenAI is accessible.")
print("--------------------------")
print("✅ Setup is valid and ready for coding!")