from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph.state import TripState
from app.core.prompts import BUDGET_SYSTEM_PROMPT
import os

async def budget_node(state: TripState):
    """
    Budget Agent: Analyzes trip requirements and provides detailed cost breakdown
    for flights, accommodation, food, activities, and local transport.
    """
    spec = state['spec']
    research_notes = state.get('research_notes', '')
    hotel_recommendations = state.get('hotel_recommendations', '')
    logistics_info = state.get('logistics_info', '')

    # Calculate trip duration
    try:
        start, end = spec.dates.split(' to ')
        from datetime import datetime
        start_date = datetime.strptime(start.strip(), "%Y-%m-%d")
        end_date = datetime.strptime(end.strip(), "%Y-%m-%d")
        num_days = (end_date - start_date).days + 1
    except:
        num_days = 3  # Default fallback

    # Check for API key to decide execution mode
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Provide mock budget breakdown
        budget_multiplier = {
            "low": 75,
            "medium": 150,
            "high": 300,
            "luxury": 600
        }.get(spec.budget_tier, 150)

        daily_budget = budget_multiplier * spec.travelers
        total = daily_budget * num_days

        budget_context = f"""
=== BUDGET BREAKDOWN ===
Trip Duration: {num_days} days
Budget Tier: {spec.budget_tier}
Travelers: {spec.travelers}

Estimated Costs (USD):
• Flights: ${300 * spec.travelers:.2f}
• Accommodation: ${(budget_multiplier * 0.4) * num_days:.2f}
• Food & Dining: ${(budget_multiplier * 0.3) * num_days:.2f}
• Activities: ${(budget_multiplier * 0.2) * num_days:.2f}
• Local Transport: ${(budget_multiplier * 0.1) * num_days:.2f}

TOTAL ESTIMATED: ${total + (300 * spec.travelers):.2f} USD

Daily Budget Per Person: ${budget_multiplier:.2f}/day
"""
        return {"budget_breakdown": budget_context}

    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.2)

    prompt = ChatPromptTemplate.from_template(BUDGET_SYSTEM_PROMPT)
    chain = prompt | llm

    response = await chain.ainvoke({
        "origin": spec.origin,
        "destination": spec.destination,
        "dates": spec.dates,
        "num_days": num_days,
        "travelers": spec.travelers,
        "budget_tier": spec.budget_tier,
        "travel_style": spec.travel_style,
        "research_notes": research_notes,
        "hotel_recommendations": hotel_recommendations,
        "logistics_info": logistics_info
    })

    return {"budget_breakdown": response.content}
