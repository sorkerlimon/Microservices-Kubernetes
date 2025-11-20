from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = "a7608bfe258027d7c46a9f2e14d6daf2"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        city_input = request.form.get('city', '').strip()
        
        if not city_input:
            return jsonify({'error': 'Please enter a city name'}), 400
        
        # Get weather data directly using city name (works with free tier)
        weather_params = {
            'q': city_input,
            'appid': API_KEY,
            'units': 'metric'  # Use metric for Celsius
        }
        
        weather_response = requests.get(WEATHER_API_URL, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Format the response
        result = {
            'city': weather_data['name'],
            'country': weather_data['sys'].get('country', ''),
            'temperature': weather_data['main']['temp'],
            'feels_like': weather_data['main']['feels_like'],
            'description': weather_data['weather'][0]['description'].title(),
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'wind_speed': weather_data['wind']['speed'],
            'visibility': weather_data.get('visibility', 0) / 1000,  # Convert to km
            'icon': weather_data['weather'][0]['icon']
        }
        
        return jsonify(result)
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching weather data: {str(e)}'}), 500
    except KeyError as e:
        return jsonify({'error': f'Unexpected API response format: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

