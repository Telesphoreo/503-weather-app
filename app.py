import requests
import os
from dotenv import load_dotenv
import streamlit as st

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
        if data["message"] == "Nothing to geocode":
            return "You didn't enter a city. Please try again."
        return None
    else:
        city_name = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        return f"In {city_name}, it is {temp}°C with {description}. The humidity is {humidity}% and it feels like {feels_like}°C outside."


def main():
    st.title("Weather App")
    city = st.text_input("City")
    if st.button("Get Weather"):
        if city.strip() == "":
            st.warning("Please enter a city.")
        else:
            result = get_weather(city)
            if result.__contains__("Please try again."):
                st.error(result)
            else:
                st.success(result)


if __name__ == "__main__":
    main()
