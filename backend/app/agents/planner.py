from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
from langchain_core.output_parsers import JsonOutputParser
from app.graph.state import TripState
from app.schemas.itinerary import TripPlan
from app.core.prompts import PLANNER_SYSTEM_PROMPT
import os
import json

async def planner_node(state: TripState):
    spec = state['spec']
    research = state.get('research_notes', '')
    weather = state.get('weather_info', 'Not checked')
    hotels = state.get('hotel_recommendations', '')
    budget = state.get('budget_breakdown', '')
    logistics = state.get('logistics_info', '')
    activities = state.get('activities_recommendations', '')

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    parser = JsonOutputParser(pydantic_object=TripPlan)

    if not project:
        # Mock Response for testing without LLM
        from datetime import datetime, timedelta
        from app.schemas.itinerary import (
            DailyPlan, Activity, AccommodationOption,
            TransportOption, BudgetBreakdown, PackingItem, WeatherData
        )

        # Parse dates
        try:
            start_date_str, end_date_str = spec.dates.split(' to ')
            start_date = datetime.strptime(start_date_str.strip(), "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str.strip(), "%Y-%m-%d")
            num_days = (end_date - start_date).days + 1
        except:
            start_date = datetime.now()
            num_days = 3

        # Generate mock itinerary
        itinerary = []
        for i in range(min(num_days, 7)):  # Max 7 days for mock
            day_date = start_date + timedelta(days=i)
            itinerary.append(DailyPlan(
                day_number=i + 1,
                date=day_date.strftime("%Y-%m-%d"),
                city=spec.destination,
                weather=WeatherData(
                    date=day_date.strftime("%Y-%m-%d"),
                    temperature_c=20.0,
                    condition="Partly cloudy",
                    precip_prob=30
                ),
                morning_activities=[
                    Activity(
                        name=f"Morning exploration of {spec.destination}",
                        description="Discover the city's highlights",
                        location="City Center",
                        estimated_cost=0,
                        time_slot="morning"
                    )
                ],
                afternoon_activities=[
                    Activity(
                        name=f"Afternoon activity in {spec.destination}",
                        description="Experience local culture",
                        location="Downtown",
                        estimated_cost=25,
                        time_slot="afternoon"
                    )
                ],
                evening_activities=[
                    Activity(
                        name=f"Evening dining in {spec.destination}",
                        description="Try local cuisine",
                        location="Restaurant District",
                        estimated_cost=50,
                        time_slot="evening"
                    )
                ],
                meal_suggestions=["Local breakfast cafe", "Lunch at market", "Traditional dinner"]
            ))

        # Mock hotels
        hotels_list = [
            AccommodationOption(
                name=f"Mock Hotel {spec.destination}",
                area="City Center",
                price_per_night=100,
                rating=4.0,
                description="Comfortable accommodation in the heart of the city",
                booking_link=f"https://www.google.com/search?q=hotels+in+{spec.destination.replace(' ', '+')}"
            )
        ]

        # Mock budget
        budget_obj = BudgetBreakdown(
            flights=600,
            accommodation=100 * num_days,
            activities=50 * num_days,
            food=75 * num_days,
            transport_local=20 * num_days,
            total_estimated=600 + (245 * num_days),
            currency="USD"
        )

        # Mock packing list
        packing_list = [
            PackingItem(category="Clothing", item="Comfortable walking shoes"),
            PackingItem(category="Accessories", item="Camera"),
            PackingItem(category="Documents", item="Passport and tickets")
        ]

        mock_plan = TripPlan(
            title=f"{num_days}-Day {spec.destination} Trip",
            summary=f"A {num_days}-day {spec.travel_style} adventure in {spec.destination} for {spec.travelers} traveler(s) with {spec.budget_tier} budget.",
            itinerary=itinerary,
            hotels_shortlist=hotels_list,
            intercity_travel=[],
            budget=budget_obj,
            packing_list=packing_list
        )

        return {"plan": mock_plan, "status": "completed", "plan_quality_score": 7}

    # Use Gemini 2.0 Flash for better planning
    llm = ChatVertexAI(
        model="gemini-2.5-flash",
        project=project,
        location=location,
        temperature=0.2,
        max_tokens=8000
    )

    prompt = ChatPromptTemplate.from_template(PLANNER_SYSTEM_PROMPT + "\n\n{format_instructions}")

    chain = prompt | llm | parser

    try:
        result = await chain.ainvoke({
            "budget_tier": spec.budget_tier,
            "travel_style": spec.travel_style,
            "research_notes": research,
            "weather_info": weather,
            "hotel_recommendations": hotels,
            "budget_breakdown": budget,
            "logistics_info": logistics,
            "activities_recommendations": activities,
            "format_instructions": parser.get_format_instructions()
        })
        # Result is a dict, we cast to TripPlan model
        plan = TripPlan(**result)

        # Evaluate plan quality (simple heuristic for now)
        quality_score = 8  # Default good score
        if len(plan.itinerary) < 1:
            quality_score = 3
        if len(plan.hotels_shortlist) < 1:
            quality_score = min(quality_score, 5)
        if plan.budget.total_estimated <= 0:
            quality_score = min(quality_score, 4)

        return {"plan": plan, "status": "completed", "plan_quality_score": quality_score}
    except Exception as e:
        return {"messages": [f"Error generating plan: {str(e)}"], "status": "failed", "plan_quality_score": 0}
