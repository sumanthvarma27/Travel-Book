from app.graph.state import TripState
from app.tools.weather import WeatherTool
import datetime

async def weather_node(state: TripState):
    """
    Weather Agent: Fetches real-time weather forecast data from Open-Meteo API
    for the destination city during the travel dates.
    """
    spec = state['spec']

    # Get coordinates for the destination city
    city = spec.destination
    lat, lon = WeatherTool.get_city_coordinates(city)

    # Parse dates
    # Assuming 'YYYY-MM-DD to YYYY-MM-DD' format
    try:
        start, end = spec.dates.split(' to ')
        start = start.strip()
        end = end.strip()
    except:
        # Fallback to reasonable defaults if date parsing fails
        start = datetime.date.today().strftime("%Y-%m-%d")
        end = (datetime.date.today() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")

    # Fetch weather forecast
    tool = WeatherTool()
    info = tool.get_forecast(lat, lon, start, end)

    return {"weather_info": info}
