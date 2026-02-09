"""
Script to check your langchain-google-genai version and supported parameters.
"""

import inspect

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    import langchain_google_genai
    
    print("=" * 60)
    print("LANGCHAIN-GOOGLE-GENAI VERSION CHECK")
    print("=" * 60)
    
    # Get version
    version = getattr(langchain_google_genai, '__version__', 'unknown')
    print(f"\n📦 Package version: {version}")
    
    # Get __init__ signature
    sig = inspect.signature(ChatGoogleGenerativeAI.__init__)
    params = list(sig.parameters.keys())
    
    print(f"\n📋 Available parameters:")
    for param in params:
        if param != 'self':
            print(f"   ✓ {param}")
    
    # Check which API key parameter exists
    print(f"\n🔑 API Key parameter:")
    if 'api_key' in params:
        print("   ✅ Use: api_key")
    elif 'google_api_key' in params:
        print("   ✅ Use: google_api_key")
    else:
        print("   ⚠️  Neither found!")
    
    # Check max tokens parameter
    print(f"\n📊 Max tokens parameter:")
    if 'max_tokens' in params:
        print("   ✅ Use: max_tokens")
    elif 'max_output_tokens' in params:
        print("   ✅ Use: max_output_tokens")
    else:
        print("   ⚠️  Neither found!")
    
    # Check timeout parameter
    print(f"\n⏱️  Timeout parameter:")
    if 'timeout' in params:
        print("   ✅ Use: timeout")
    elif 'request_timeout' in params:
        print("   ✅ Use: request_timeout")
    else:
        print("   ⚠️  Not supported")
    
    print("\n" + "=" * 60)
    print("RECOMMENDED CODE:")
    print("=" * 60)
    
    # Generate recommended code
    api_key_param = 'api_key' if 'api_key' in params else 'google_api_key'
    max_tokens_param = 'max_tokens' if 'max_tokens' in params else 'max_output_tokens'
    
    print(f"""
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    {api_key_param}=api_key,
    temperature=temperature,
    {max_tokens_param}=max_tokens,
)
""")
    
except ImportError:
    print("❌ langchain-google-genai not installed")
    print("Run: pip install langchain-google-genai")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()