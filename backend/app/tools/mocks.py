import random
from typing import List
from app.schemas.itinerary import AccommodationOption, TransportOption

class BookingMocks:
    """
    Mock adapter to simulate flight/hotel data when real APIs are not configured.
    """
    
    @staticmethod
    def search_hotels(destination: str, budget_tier: str) -> List[AccommodationOption]:
        # Identify base price based on budget
        base_price = 100
        if budget_tier == "low": base_price = 50
        elif budget_tier == "high": base_price = 250
        elif budget_tier == "luxury": base_price = 600
        
        adjectives = ["Cozy", "Grand", "City", "Boutique", "Modern", "Historic"]
        suffixes = ["Hotel", "Inn", "Suites", "Resort", "Stay"]
        
        options = []
        for i in range(3):
            name = f"{random.choice(adjectives)} {destination} {random.choice(suffixes)}"
            price = base_price * random.uniform(0.8, 1.2)
            options.append(AccommodationOption(
                name=name,
                area="City Center",
                price_per_night=round(price, 2),
                rating=round(random.uniform(3.5, 5.0), 1),
                booking_link=f"https://www.google.com/search?q={name.replace(' ', '+')}",
                description=f"A {budget_tier} option centrally located near major attractions."
            ))
        return options

    @staticmethod
    def search_flights(origin: str, destination: str, date: str) -> List[TransportOption]:
        # Simulate flight search
        airlines = ["SkyAir", "GlobalJet", "EcoFly"]
        price = 300 + random.randint(-50, 150)
        
        return [
            TransportOption(
                type="flight",
                provider=random.choice(airlines),
                departure=f"{origin} ({date} 09:00)",
                arrival=f"{destination} ({date} 14:00)",
                estimated_price=price,
                booking_link="https://www.google.com/travel/flights"
            )
        ]
