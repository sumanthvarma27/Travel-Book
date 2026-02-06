"""Simple test to verify Gemini API connection"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_google_genai import ChatGoogleGenerativeAI

    print("Testing with gemini-2.5-flash...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    response = llm.invoke("Say hello in one sentence.")
    print(f"✓ Success! Response: {response.content}")

except Exception as e:
    print(f"✗ Error: {e}")
