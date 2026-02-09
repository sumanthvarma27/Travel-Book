import openmeteo_requests
import requests_cache
from retry_requests import retry
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class WeatherTool:
    def __init__(self):
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"

    def get_forecast(self, latitude: float, longitude: float, start_date: str, end_date: str) -> str:
        """
        Fetches detailed weather forecast for given coords and dates from Open-Meteo API.
        Returns a comprehensive human readable string summary for agent consumption.
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_probability_max",
                "precipitation_sum",
                "weathercode",
                "windspeed_10m_max"
            ],
            "timezone": "auto",
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            responses = self.openmeteo.weather_api(self.url, params=params)
            response = responses[0]

            daily = response.Daily()

            # Extract all weather variables
            temp_max = daily.Variables(0).ValuesAsNumpy()
            temp_min = daily.Variables(1).ValuesAsNumpy()
            precip_prob = daily.Variables(2).ValuesAsNumpy()
            precip_sum = daily.Variables(3).ValuesAsNumpy()
            weather_codes = daily.Variables(4).ValuesAsNumpy()
            wind_speed = daily.Variables(5).ValuesAsNumpy()

            # Generate time array for dates
            dates = []
            current = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            while current <= end:
                dates.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)

            # Build detailed summary
            summary = f"\n=== WEATHER FORECAST ({start_date} to {end_date}) ===\n"
            summary += f"Location: ({latitude:.2f}, {longitude:.2f})\n\n"

            # Daily breakdown
            for i, date in enumerate(dates):
                if i < len(temp_max):
                    condition = self._interpret_weather_code(int(weather_codes[i]))
                    temp_max_c = temp_max[i]
                    temp_min_c = temp_min[i]
                    temp_max_f = (temp_max_c * 9/5) + 32
                    temp_min_f = (temp_min_c * 9/5) + 32

                    summary += f"📅 {date}:\n"
                    summary += f"  🌡️  Temp: {temp_min_c:.1f}°C - {temp_max_c:.1f}°C ({temp_min_f:.1f}°F - {temp_max_f:.1f}°F)\n"
                    summary += f"  ☁️  Condition: {condition}\n"
                    summary += f"  💧 Precipitation: {precip_prob[i]:.0f}% chance, {precip_sum[i]:.1f}mm expected\n"
                    summary += f"  💨 Wind: {wind_speed[i]:.1f} km/h\n\n"

            # Overall summary
            avg_temp_max = temp_max.mean()
            avg_temp_min = temp_min.mean()
            avg_precip_prob = precip_prob.mean()
            total_precip = precip_sum.sum()

            summary += "📊 OVERALL SUMMARY:\n"
            summary += f"  • Average temperatures: {avg_temp_min:.1f}°C - {avg_temp_max:.1f}°C\n"
            summary += f"  • Average precipitation chance: {avg_precip_prob:.0f}%\n"
            summary += f"  • Total expected rainfall: {total_precip:.1f}mm\n"

            # Travel recommendations
            summary += "\n💡 PACKING RECOMMENDATIONS:\n"
            if avg_temp_max > 25:
                summary += "  • Light, breathable clothing\n"
                summary += "  • Sun protection (hat, sunscreen)\n"
            elif avg_temp_max > 15:
                summary += "  • Comfortable layers\n"
                summary += "  • Light jacket for evenings\n"
            else:
                summary += "  • Warm clothing and layers\n"
                summary += "  • Winter jacket\n"

            if avg_precip_prob > 50:
                summary += "  • Waterproof jacket or umbrella (high rain chance)\n"
            elif avg_precip_prob > 30:
                summary += "  • Light rain gear recommended\n"

            if wind_speed.max() > 30:
                summary += "  • Windproof outer layer\n"

            return summary

        except Exception as e:
            # Fallback with helpful error message
            return f"""
=== WEATHER FORECAST UNAVAILABLE ===
Could not fetch weather data for ({latitude:.2f}, {longitude:.2f})
Error: {str(e)}

Please check:
1. Internet connection
2. Coordinates are valid
3. Dates are in correct format (YYYY-MM-DD)

Using general recommendations:
• Pack layers for variable conditions
• Bring rain gear as precaution
• Check weather closer to travel dates
"""

    def _interpret_weather_code(self, code: int) -> str:
        """
        Interprets WMO Weather interpretation codes.
        https://open-meteo.com/en/docs
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, f"Unknown condition (code {code})")

    @staticmethod
    def get_city_coordinates(city: str) -> tuple[float, float]:
        """
        Returns approximate coordinates for common cities.
        In production, use a geocoding API like Nominatim or Google Geocoding.
        """
        city_coords = {
            "new york": (40.7128, -74.0060),
            "nyc": (40.7128, -74.0060),
            "london": (51.5074, -0.1278),
            "paris": (48.8566, 2.3522),
            "tokyo": (35.6762, 139.6503),
            "sydney": (-33.8688, 151.2093),
            "dubai": (25.2048, 55.2708),
            "singapore": (1.3521, 103.8198),
            "barcelona": (41.3874, 2.1686),
            "rome": (41.9028, 12.4964),
            "berlin": (52.5200, 13.4050),
            "amsterdam": (52.3676, 4.9041),
            "madrid": (40.4168, -3.7038),
            "vienna": (48.2082, 16.3738),
            "prague": (50.0755, 14.4378),
            "istanbul": (41.0082, 28.9784),
            "athens": (37.9838, 23.7275),
            "los angeles": (34.0522, -118.2437),
            "la": (34.0522, -118.2437),
            "san francisco": (37.7749, -122.4194),
            "chicago": (41.8781, -87.6298),
            "miami": (25.7617, -80.1918),
            "seattle": (47.6062, -122.3321),
            "boston": (42.3601, -71.0589),
            "washington": (38.9072, -77.0369),
            "toronto": (43.6532, -79.3832),
            "vancouver": (49.2827, -123.1207),
            "mexico city": (19.4326, -99.1332),
            "rio de janeiro": (22.9068, -43.1729),
            "sao paulo": (-23.5505, -46.6333),
            "buenos aires": (-34.6037, -58.3816),
            "cairo": (30.0444, 31.2357),
            "johannesburg": (-26.2041, 28.0473),
            "mumbai": (19.0760, 72.8777),
            "delhi": (28.7041, 77.1025),
            "bangalore": (12.9716, 77.5946),
            "bangkok": (13.7563, 100.5018),
            "seoul": (37.5665, 126.9780),
            "beijing": (39.9042, 116.4074),
            "shanghai": (31.2304, 121.4737),
            "hong kong": (22.3193, 114.1694),
            "melbourne": (-37.8136, 144.9631),
            "auckland": (-36.8485, 174.7633),
            "lisbon": (38.7223, -9.1393),
            "dublin": (53.3498, -6.2603),
            "copenhagen": (55.6761, 12.5683),
            "stockholm": (59.3293, 18.0686),
            "oslo": (59.9139, 10.7522),
            "helsinki": (60.1699, 24.9384),
            "warsaw": (52.2297, 21.0122),
            "budapest": (47.4979, 19.0402),
            "zurich": (47.3769, 8.5417),
            "geneva": (46.2044, 6.1432),
            "brussels": (50.8503, 4.3517),
            "kyoto": (35.0116, 135.7681),
            "osaka": (34.6937, 135.5023),
        }

        # Try exact match first, then normalize common formats (e.g., "Tokyo, Japan")
        city_lower = city.lower().strip()
        coords = city_coords.get(city_lower)
        if not coords and "," in city_lower:
            primary = city_lower.split(",")[0].strip()
            coords = city_coords.get(primary)

        if coords:
            return coords

        # If not found, return NYC as default (could be improved with actual geocoding API)
        print(f"Warning: City '{city}' not found in database, using default coordinates")
        return (40.7128, -74.0060)  # Default to NYC


# Module-level helper for compatibility with older imports
_weather_tool = WeatherTool()

def weather_forecast(*args) -> str:
    """
    Flexible weather_forecast wrapper.
    Acceptable signatures:
      - weather_forecast(city: str, start_date: str, end_date: str)
      - weather_forecast(latitude: float, longitude: float, start_date: str, end_date: str)
    """
    if len(args) == 3 and isinstance(args[0], str):
        city, start_date, end_date = args
        lat, lon = WeatherTool.get_city_coordinates(city)
        return _weather_tool.get_forecast(lat, lon, start_date, end_date)
    elif len(args) == 4:
        latitude, longitude, start_date, end_date = args
        return _weather_tool.get_forecast(latitude, longitude, start_date, end_date)
    else:
        raise TypeError("weather_forecast expects (city, start_date, end_date) or (lat, lon, start_date, end_date)")


def get_city_coordinates(city: str) -> tuple[float, float]:
    return WeatherTool.get_city_coordinates(city)
