"""Test Vertex AI connection"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_vertex_ai():
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project:
        print("❌ GOOGLE_CLOUD_PROJECT not set in .env file")
        print("\nPlease add to backend/.env:")
        print("GOOGLE_CLOUD_PROJECT=My Project 27432")
        print("GOOGLE_CLOUD_LOCATION=us-central1")
        return False

    print(f"✓ Project: {project}")
    print(f"✓ Location: {location}")
    print("\nTesting Vertex AI connection...")

    try:
        from langchain_google_vertexai import ChatVertexAI

        llm = ChatVertexAI(
            model="gemini-2.5-flash",
            project=project,
            location=location,
            temperature=0.7
        )

        response = llm.invoke("Say hello in one sentence.")
        print(f"\n✓ Success! Vertex AI Response: {response.content}")
        print("\n✅ Vertex AI is working correctly!")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Vertex AI API is enabled:")
        print("   https://console.cloud.google.com/apis/library/aiplatform.googleapis.com")
        print("\n2. Authenticate with gcloud:")
        print("   gcloud auth application-default login")
        print("\n3. Set your project:")
        print(f"   gcloud config set project \"{project}\"")
        print("\n4. Verify credentials:")
        print("   gcloud auth application-default print-access-token")
        return False

if __name__ == "__main__":
    test_vertex_ai()
