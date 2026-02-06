from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph.state import TripState
from app.core.prompts import RESEARCHER_SYSTEM_PROMPT
import os

async def research_node(state: TripState):
    spec = state['spec']
    
    # Check for API key to decide execution mode
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"research_notes": "Simulation: The user likes museums and spicy food. Recommended: Grand Museum, Spicy Noodle House."}

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    
    prompt = ChatPromptTemplate.from_template(RESEARCHER_SYSTEM_PROMPT)
    chain = prompt | llm
    
    response = await chain.ainvoke({
        "destination": spec.destination,
        "interests": ", ".join(spec.interests),
        "budget_tier": spec.budget_tier
    })
    
    return {"research_notes": response.content}
