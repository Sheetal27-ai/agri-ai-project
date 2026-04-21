import requests
import os
import datetime

# 🔐 Use environment variable instead of hardcoding
# API_KEY = os.getenv("OPENWEATHER_API_KEY")
API_KEY = "0303bad7ef133a4b8068b768d401dfd7"
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"


def _get_monthly_rainfall(city: str, month: int) -> float:
    """
    Historical average monthly rainfall (mm) for major Indian cities.
    Matches ML dataset scale.
    """
    RAINFALL_TABLE = {
        "ludhiana":    [28, 42, 30, 15, 18, 72, 210, 195, 78, 18, 8, 20],
        "delhi":       [21, 19, 13, 8, 13, 54, 211, 173, 43, 10, 3, 11],
        "mumbai":      [3, 3, 3, 2, 18, 485, 617, 340, 26, 64, 13, 5],
        "bangalore":   [5, 8, 14, 38, 110, 79, 87, 130, 170, 170, 56, 20],
        "chennai":     [35, 10, 7, 15, 30, 40, 80, 98, 120, 305, 350, 140],
        "kolkata":     [13, 22, 27, 45, 120, 263, 325, 306, 253, 114, 21, 8],
        "hyderabad":   [8, 11, 13, 24, 30, 71, 165, 156, 163, 71, 24, 7],
        "jaipur":      [14, 9, 9, 4, 10, 53, 193, 198, 51, 14, 4, 7],
        "ahmedabad":   [2, 1, 1, 1, 4, 103, 320, 243, 91, 11, 3, 2],
        "chandigarh":  [35, 44, 33, 14, 21, 78, 228, 208, 86, 21, 8, 22],
        "amritsar":    [30, 38, 28, 13, 17, 68, 205, 188, 74, 17, 7, 19],
        "pune":        [3, 1, 5, 18, 58, 150, 180, 120, 110, 63, 19, 7],
    }

    city_key = city.lower().strip()

    if city_key in RAINFALL_TABLE:
        return float(RAINFALL_TABLE[city_key][month - 1])
    else:
        india_avg = [18, 20, 15, 10, 25, 150, 280, 240, 120, 50, 15, 12]
        return float(india_avg[month - 1])


def get_weather(location: str) -> dict:
    """
    Fetch real-time temperature & humidity.
    Uses historical rainfall for ML consistency.
    """

    print(f"🌦 Fetching weather for {location}...")

    # If API key missing → fallback immediately
    if not API_KEY:
        print("⚠ API key missing. Using fallback weather data.")
        return _fallback_weather(location)

    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(CURRENT_URL, params=params, timeout=5)

        if response.status_code == 401:
            raise Exception("Invalid API key.")
        if response.status_code == 404:
            raise Exception(f"City '{location}' not found.")

        response.raise_for_status()
        data = response.json()

        current_month = datetime.datetime.now().month

        return {
            "temperature": float(data["main"]["temp"]),
            "humidity": float(data["main"]["humidity"]),
            "rainfall": _get_monthly_rainfall(location, current_month),
            "city": data.get("name", location),
            "description": data["weather"][0]["description"]
        }

    except Exception as e:
        print(f"⚠ Weather API failed: {e}")
        return _fallback_weather(location)


def _fallback_weather(location: str) -> dict:
    """
    Safe fallback if API fails.
    Ensures system never crashes.
    """
    current_month = datetime.datetime.now().month

    return {
        "temperature": 25.0,
        "humidity": 60.0,
        "rainfall": _get_monthly_rainfall(location, current_month),
        "city": location,
        "description": "fallback data"
    }


# Test
if __name__ == "__main__":
    data = get_weather("Patiala")
    print("Weather Data:", data)