import requests
from datetime import datetime

# Constants
API_KEY = '5f1ec2fee70cfbb8b9c4d5cdf4c44df9'  # Replace with your OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

def fetch_weather_data(city: str) -> dict:
    """Fetches weather data for a given city from OpenWeatherMap."""
    try:
        response = requests.get(BASE_URL.format(city, API_KEY))
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def parse_weather_data(data: dict) -> dict:
    """Parses the weather data from the API response."""
    try:
        weather_data = {
            'location': data['name'],
            'time': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'),  # Convert Unix timestamp to human-readable format
            'info': data['weather'][0]['description'],
            'temperature': data['main']['temp']
        }
        return weather_data
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        return None

def display_weather(weather_data: dict):
    """Displays the weather data."""
    if weather_data:
        print(f"Location: {weather_data['location']}")
        print(f"Time: {weather_data['time']}")
        print(f"Weather: {weather_data['info']}")
        print(f"Temperature: {weather_data['temperature']}°C")
    else:
        print("Unable to display weather data.")

def main():
    """Main function to run the weather application."""
    print("Enter the city name:")
    city = input().strip()
    
    data = fetch_weather_data(city)
    if data:
        weather_data = parse_weather_data(data)
        display_weather(weather_data)
    else:
        print("Failed to retrieve weather data.")

if __name__ == "__main__":
    main()