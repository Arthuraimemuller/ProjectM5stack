import streamlit as st
import requests
import datetime
from collections import defaultdict

API_KEY = "72dbcc9258a8493ae64994a80e22e830"
CITY = "Lausanne"
UNITS = "metric"
LANG = "fr"



# ------------------- Functions -------------------
def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    return requests.get(url).json()

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    return requests.get(url).json()

def get_emoji(weather):
    mapping = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Snow": "❄️",
        "Thunderstorm": "⛈️", "Drizzle": "🌦️", "Mist": "🌫️"
    }
    return mapping.get(weather, "❔")

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="Weather Dashboard", page_icon="⛅", layout="wide")
st.title(f"📍 Météo à {CITY}")


# --- Current Weather ---
st.subheader("🌤️ Conditions actuelles")
current = get_current_weather(CITY)



# --- Radar Map ---
with st.expander("🛰️ Weather map",expanded=True):
    st.markdown(
        """
        <div style="position: relative; width: 100%; height: 0; padding-bottom: 60%;">
            <iframe
                src="https://embed.windy.com/embed2.html?lat=46.519&lon=6.632&detailLat=46.519&detailLon=6.632&zoom=11"
                style="position: absolute; top: 0; left: 0; width: 100%; height: 40%; border: none;"
                allowfullscreen
            ></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )





if current.get("main"):
    temp = current["main"]["temp"]
    humidity = current["main"]["humidity"]
    desc = current["weather"][0]["description"].capitalize()
    icon = current["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
    emoji = get_emoji(current["weather"][0]["main"])

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(icon_url)
    with col2:
        st.write(f"{emoji} **{desc}**")
        st.metric("🌡️ Température", f"{temp:.1f} °C")
        st.metric("💧 Humidité", f"{humidity}%")

    # Alerts
    if "pluie" in desc.lower():
        st.warning("🌧️ N'oublie pas ton parapluie !")
    if temp < 0:
        st.error("❄️ Attention au verglas !")

else:
    st.error("Erreur lors de la récupération des données.")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
         <div style='
             background-color:#1e1e1e;
             border-radius: 50%;
             width: 200px;
             height: 200px;
             display: flex;
             justify-content: center;
             align-items: center;
             color: white;
             font-size: 24px;
             margin: auto;
         '>
             🏠 {temp:.1f} °C
         </div>
         """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
         <div style='
             background-color:#1e1e1e;
             border-radius: 50%;
             width: 200px;
             height: 200px;
             display: flex;
             justify-content: center;
             align-items: center;
             color: white;
             font-size: 24px;
             margin: auto;
         '>
             🌤️ {humidity:.1f} °C
         </div>
         """,
        unsafe_allow_html=True
    )


# --- Forecast ---
st.subheader("📅 Prévisions (3 jours)")
forecast = get_forecast(CITY)

daily_data = defaultdict(list)
for entry in forecast["list"]:
    date = entry["dt_txt"].split(" ")[0]
    daily_data[date].append(entry)

for date, entries in list(daily_data.items())[:3]:
    avg_temp = sum(e['main']['temp'] for e in entries) / len(entries)
    weather_main = entries[0]['weather'][0]['main']
    weather_desc = entries[0]['weather'][0]['description'].capitalize()
    icon = entries[0]['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
    day = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A %d %B")

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(icon_url)
    with col2:
        st.markdown(f"**{day}**")
        st.write(f"🌡️ Temp. moyenne: {avg_temp:.1f}°C")
        st.write(f"🌥️ Conditions: {weather_desc}")

    # Example values: temp indoor (simulée ici) et temp outdoor (récupérée depuis OpenWeather)
    indoor_temp = 23.5  # Tu peux ici remplacer par une vraie mesure depuis un capteur
    outdoor_temp = temp  # récupéré depuis les données météo

    # Display two circles side-by-side
    st.markdown("## 🌡️ Température Intérieure vs Extérieure")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style='
                background-color:#1e1e1e;
                border-radius: 50%;
                width: 200px;
                height: 200px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                font-size: 24px;
                margin: auto;
            '>
                🏠 {indoor_temp:.1f} °C
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='
                background-color:#1e1e1e;
                border-radius: 50%;
                width: 200px;
                height: 200px;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                font-size: 24px;
                margin: auto;
            '>
                🌤️ {outdoor_temp:.1f} °C
            </div>
            """,
            unsafe_allow_html=True
        )

st.caption("Données fournies par OpenWeatherMap & Windy.com")
