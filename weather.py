import streamlit as st
import requests

# -----------------------------
# Configuration
# -----------------------------
API_KEY = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key

st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🌤️ Modern Weather App")
st.write("Check the current weather for any city.")

city = st.text_input("📍 Enter City Name", placeholder="e.g. London")

if st.button("Get Weather"):

    if city == "":
        st.warning("Please enter a city name.")
    else:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:

            weather = data["weather"][0]["main"]
            description = data["weather"][0]["description"].title()

            st.success(f"Weather in {data['name']}, {data['sys']['country']}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🌡️ Temperature", f"{data['main']['temp']} °C")
                st.metric("🤗 Feels Like", f"{data['main']['feels_like']} °C")
                st.metric("💧 Humidity", f"{data['main']['humidity']}%")

            with col2:
                st.metric("🌬️ Wind Speed", f"{data['wind']['speed']} m/s")
                st.metric("☁️ Weather", weather)
                st.metric("📝 Description", description)

        else:
            st.error("City not found.")
