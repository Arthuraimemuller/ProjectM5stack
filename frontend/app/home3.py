import streamlit as st
import requests
import datetime
from collections import defaultdict

# URL de ton backend Flask exposant les données BigQuery
BACKEND_CURRENT_URL = "https://docker-flask-backend-project-688745668065.europe-west6.run.app/weather/current"
BACKEND_FORECAST_URL = "https://docker-flask-backend-project-688745668065.europe-west6.run.app/weather/forecast"

CITY = "Lausanne"

# ------------------- Fonctions -------------------

def get_current_weather_from_backend():
    try:
        res = requests.get(BACKEND_CURRENT_URL)
        res.raise_for_status()
        data = res.json()
        # Exemple attendu : {"temperature": 22.5, "humidity": 50, "description": "ciel dégagé", "main": "Clear", "icon": "01d"}
        return data
    except Exception as e:
        st.error(f"Erreur récupération météo courante : {e}")
        return None

def get_forecast_from_backend():
    try:
        res = requests.get(BACKEND_FORECAST_URL)
        res.raise_for_status()
        data = res.json()
        # Exemple attendu : liste de dict [{ "date": "2025-05-22", "temp": 23.5, "description": "nuageux", "main": "Clouds", "icon": "03d" }, ...]
        return data
    except Exception as e:
        st.error(f"Erreur récupération prévisions : {e}")
        return []

def get_emoji(weather):
    mapping = {
        "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Snow": "❄️",
        "Thunderstorm": "⛈️", "Drizzle": "🌦️", "Mist": "🌫️"
    }
    return mapping.get(weather, "❔")

# ------------------- Streamlit UI -------------------

st.set_page_config(page_title="Weather Dashboard", page_icon="⛅", layout="wide")
st.title(f"📍 Météo à {CITY}")

# --- Météo courante ---
st.subheader("🌤️ Conditions actuelles")

current = get_current_weather_from_backend()
if current:
    temp = current.get("temperature", "--")
    humidity = current.get("humidity", "--")
    desc = current.get("description", "Inconnue").capitalize()
    main = current.get("main", "")
    icon = current.get("icon", "01d")
    icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
    emoji = get_emoji(main)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(icon_url)
    with col2:
        st.write(f"{emoji} **{desc}**")
        st.metric("🌡️ Température", f"{temp} °C")
        st.metric("💧 Humidité", f"{humidity}%")

    # Alerts
    if "pluie" in desc.lower():
        st.warning("🌧️ N'oublie pas ton parapluie !")
    if isinstance(temp, (int, float)) and temp < 0:
        st.error("❄️ Attention au verglas !")
else:
    st.error("Impossible de récupérer la météo courante.")

# --- Prévisions ---
st.subheader("📅 Prévisions (3 jours)")

forecast = get_forecast_from_backend()

if forecast:
    for day_data in forecast[:3]:
        date_str = day_data.get("date", "1970-01-01")
        temp = day_data.get("temp", "--")
        desc = day_data.get("description", "Inconnue").capitalize()
        main = day_data.get("main", "")
        icon = day_data.get("icon", "01d")
        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
        day = datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%A %d %B")

        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(icon_url)
        with col2:
            st.markdown(f"**{day}**")
            st.write(f"🌡️ Température prévue: {temp} °C")
            st.write(f"🌥️ Conditions: {desc}")

else:
    st.error("Impossible de récupérer les prévisions météo.")

# Tu peux aussi afficher ici les données indoor si tu les as, ou autres infos...

st.caption("Données fournies par ton backend BigQuery via Flask")
