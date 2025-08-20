import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "APPID": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["cod"] != 200:
        if data["message"] == "city not found":
            print("City not found. Make sure you typed it in correctly.\n")
        if data["message"] == "Nothing to geocode":
            print("You didn't enter a city. Please try again.\n")
    else:
        city_name = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        print(f"In {city_name}, it is {temp}°C with {description}. The humidity is {humidity}% and it feels like {feels_like}°C outside.\n")


def main():
    while True:
        input_city = input("Type in a city you'd like to get weather for. Alternatively, type 'q' to quit.\n")
        if input_city == "q":
            print("Goodbye!")
            return
        else:
            get_weather(input_city)


if __name__ == "__main__":
    main()
