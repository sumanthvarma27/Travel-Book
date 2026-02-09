from langchain_core.prompts import ChatPromptTemplate
from app.graph.state import TripState
from app.core.prompts import RESEARCHER_SYSTEM_PROMPT
from app.tools.search_utils import run_searches, build_search_context
from app.core.llm import get_llm

async def research_node(state: TripState):
    """
    Research Agent: Gathers comprehensive destination information using web search.
    Focuses on attractions, restaurants, local culture, and hidden gems.
    """
    spec = state['spec']

    # Perform web searches for real-time data
    search_queries = [
        f"best things to do in {spec.destination} {' '.join(spec.interests) if spec.interests else ''}",
        f"top restaurants {spec.destination} {spec.budget_tier} budget",
        f"hidden gems {spec.destination} local recommendations",
        f"{spec.destination} travel guide 2026"
    ]

    search_results = run_searches(search_queries, max_results_per_query=4, max_total=15)
    search_context = build_search_context(search_results, max_items=15)

    llm = get_llm(temperature=0.7, max_tokens=8000)
    if not llm:
        return {
            "research_notes": f"""
=== DESTINATION RESEARCH: {spec.destination} ===

Budget Tier: {spec.budget_tier}
Interests: {', '.join(spec.interests) if spec.interests else 'general sightseeing'}

Note: Using fallback mode - configure GEMINI_API_KEY for enhanced research.

General recommendations for {spec.destination}:
• Explore major landmarks and attractions
• Try local cuisine and traditional restaurants
• Visit museums and cultural sites
• Experience local markets and neighborhoods
• Check travel forums for recent tips

Web search context: {search_context[:500]}...
"""
        }

    prompt = ChatPromptTemplate.from_template(
        RESEARCHER_SYSTEM_PROMPT + "\n\nWeb Search Results:\n{search_context}"
    )
    chain = prompt | llm

    response = await chain.ainvoke({
        "destination": spec.destination,
        "interests": ", ".join(spec.interests) if spec.interests else "general sightseeing",
        "budget_tier": spec.budget_tier,
        "search_context": search_context
    })

    return {"research_notes": response.content}