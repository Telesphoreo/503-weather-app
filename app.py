import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_cities(city, limit=5):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": limit,
        "APPID": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()


def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "APPID": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    return response.json()


def print_data(data):
    city_name = data["name"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    return f"In {city_name}, it is {temp}°C with {description}. The humidity is {humidity}% and it feels like {feels_like}°C outside."


def main():
    st.title("Weather App")
    city = st.text_input("City")
    if 'city' not in st.session_state:
        st.session_state.city = None
    if st.button("Get Weather"):
        if city.strip() == "":
            st.warning("Please enter a city.")
            st.session_state.result = None
        else:
            st.session_state.city = fetch_cities(city)

    result = st.session_state.city

    if result is None:
        pass
    elif len(result) == 0 or not isinstance(result, list):
        st.warning("City not found.")
    else:
        options = [
            f"{cities['name']}, {cities.get('state', '-')}, {cities['country']}"
            for cities in st.session_state.city
        ]
        selected_from_dropdown = st.selectbox("Choose your city from the list:", options)
        selected_city = options.index(selected_from_dropdown)
        data = get_weather(st.session_state.city[selected_city]['lat'], st.session_state.city[selected_city]['lon'])
        st.success(print_data(data))


if __name__ == "__main__":
    main()
