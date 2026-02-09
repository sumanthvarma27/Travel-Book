import os
import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_llm(*, temperature: float = 0.7, max_tokens: int = 8000, timeout: int = 120):
    """
    Return a configured LLM instance.
    Priority: Kimi K2 -> Gemini (fallback)
    """
    
    # --- Primary: Kimi K2 (Moonshot AI) ---
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            from pydantic import SecretStr

            
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=SecretStr(groq_key),  # wrap in SecretStr
                temperature=temperature,
                max_tokens=max_tokens,
                )
            logger.info("✅ Using Groq (Llama 3.3 70B)")
            return llm
        except Exception as e:
            logger.warning(f"Groq failed: {str(e)[:80]}")

    # --- Fallback: Gemini ---
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            logger.info("✅ Using Gemini 2.0 Flash (fallback)")
            return DirectGeminiWrapper(model, temperature, max_tokens)
        except Exception as e:
            logger.warning(f"Gemini failed: {str(e)[:80]}")

    raise ValueError(
        "No LLM available. Set MOONSHOT_API_KEY or GEMINI_API_KEY in your .env file.\n"
        "Get Kimi key: https://platform.moonshot.ai\n"
        "Get Gemini key: https://ai.google.dev/"
    )


class DirectGeminiWrapper:
    """Wrapper for Google's generativeai SDK with LangChain-compatible interface."""
    
    def __init__(self, model: Any, temperature: float, max_tokens: int = 8000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def invoke(self, prompt: str) -> Any:
        response = self.model.generate_content(
            prompt, generation_config={'temperature': self.temperature}
        )
        class Response:
            def __init__(self, text):
                self.content = text
        return Response(response.text)
    
    async def ainvoke(self, prompt: str) -> Any:
        return self.invoke(prompt)


def test_llm_connection():
    """Test LLM connection with a simple prompt."""
    try:
        llm = get_llm(temperature=0.1, max_tokens=100)
        response = llm.invoke("Say 'Hello, I am working!' if you can read this.")
        
        # Handle both LangChain and wrapper response formats
        content = response.content if hasattr(response, 'content') else str(response)
        logger.info(f"✅ LLM test successful: {content}")
        print(f"✅ LLM test successful: {content}")
        return True
    except Exception as e:
        logger.error(f"❌ LLM test failed: {e}")
        print(f"❌ LLM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Testing LLM connection...")
    success = test_llm_connection()
    
    if success:
        print("\n✅ Everything working! You can use this in your app.")
    else:
        print("\n❌ Fix the errors above before using.")