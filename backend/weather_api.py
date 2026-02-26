"""
Weather API Integration
Fetches live weather data from OpenWeatherMap API
"""

import requests


def get_weather_data(city, api_key):
    """Fetch live weather data from OpenWeatherMap API"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': f"{city},IN",
        'appid': api_key,
        'units': 'metric'
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'] * 3.6,  # m/s to km/h
            'rainfall_1h': data.get('rain', {}).get('1h', 0),
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }

    except Exception:
        return None
