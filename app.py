from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Constants
API_KEY = '5f1ec2fee70cfbb8b9c4d5cdf4c44df9'  # Replace with your OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

def fetch_weather_data(city: str) -> dict:
    """Fetches weather data for a given city from OpenWeatherMap."""
    try:
        response = requests.get(BASE_URL.format(city, API_KEY))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def parse_weather_data(data: dict) -> dict:
    """Parses the weather data from the API response."""
    try:
        weather_data = {
            'location': data['name'],
            'time': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            'info': data['weather'][0]['description'],
            'temperature': data['main']['temp']
        }
        return weather_data
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    data = fetch_weather_data(city)
    if data:
        weather_data = parse_weather_data(data)
        if weather_data:
            return jsonify(weather_data)
    return jsonify({'error': 'Failed to retrieve weather data'}), 400

if __name__ == '__main__':
    app.run(debug=True)