from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from app.graph.state import TripState
from app.core.prompts import RESEARCHER_SYSTEM_PROMPT
from app.tools.web_search import web_search_tool
import os

async def research_node(state: TripState):
    spec = state['spec']

    # Check for Vertex AI configuration
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project:
        return {"research_notes": "Simulation: The user likes museums and spicy food. Recommended: Grand Museum, Spicy Noodle House."}

    # Perform web searches for real-time data
    search_queries = [
        f"best things to do in {spec.destination} {' '.join(spec.interests)}",
        f"top restaurants {spec.destination} {spec.budget_tier} budget",
        f"hidden gems {spec.destination} local recommendations",
        f"{spec.destination} travel guide 2026"
    ]

    search_results = []
    for query in search_queries:
        try:
            results = web_search_tool.invoke({"query": query, "max_results": 4})
            search_results.extend(results)
        except Exception as e:
            print(f"Search error for '{query}': {e}")

    # Format search results for LLM
    search_context = "\n\n".join([
        f"**{r['title']}**\n{r['snippet']}\nSource: {r['url']}"
        for r in search_results[:15]  # Limit to top 15 results
    ])

    llm = ChatVertexAI(
        model="gemini-2.5-flash",
        project=project,
        location=location,
        temperature=0.7,
        max_tokens=8000
    )

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
