import streamlit as st
import requests

# Replace with your OpenWeatherMap API key
API_KEY = "YOUR_API_KEY"

st.set_page_config(page_title="Live Weather", page_icon="🌤️")

st.title("🌤️ Live Weather App")

city = st.text_input("Enter City Name")

if st.button("Get Live Weather"):

    if city.strip() == "":
        st.warning("Please enter a city.")
    else:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            st.success(f"Weather in {data['name']}, {data['sys']['country']}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🌡 Temperature", f"{data['main']['temp']} °C")
                st.metric("💧 Humidity", f"{data['main']['humidity']}%")
                st.metric("🌬 Wind", f"{data['wind']['speed']} m/s")

            with col2:
                st.metric("🤗 Feels Like", f"{data['main']['feels_like']} °C")
                st.metric("📊 Pressure", f"{data['main']['pressure']} hPa")
                st.metric("☁ Condition", data['weather'][0]['main'])

            st.write("### Description")
            st.info(data["weather"][0]["description"].title())

        else:
            st.error("City not found or API key is invalid.")
