from flask import Flask, render_template, jsonify, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_current_weather():
    try:
        # Get location from query parameter
        location = request.args.get('location')
        if not location:
            return jsonify({'error': 'Location parameter is missing'}), 400

        # Fetch weather data from OpenWeatherMap API
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        # Check if API response contains expected data
        if 'main' not in data or 'weather' not in data:
            return jsonify({'error': 'Unable to retrieve weather data'})

        # Extract relevant weather information
        temperature_kelvin = data['main']['temp']
        description = data['weather'][0]['description']
        
        # Convert temperature from Kelvin to Celsius and round to 2 decimal places
        temperature_celsius = round(temperature_kelvin - 273.15, 2)

        # Return weather data as JSON
        return jsonify({'location': location, 'temperature': temperature_celsius, 'description': description})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
