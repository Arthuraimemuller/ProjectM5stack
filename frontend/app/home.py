import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime


#BASE_URL = "https://docker-flask-backend-688745668065.europe-west6.run.app" #http://localhost:5000
BASE_URL = "http://localhost:5000"
# Endpoint de ton backend Elasticsearch
API_URL_AUTOCOMPLETE = BASE_URL + "/autocomplete"  # Remplace par l'URL de ton API
RECOMMEND_API_URL = BASE_URL + "/recommend"  # Remplace par ton endpoint de recommandation


# Ajouter un bouton de recommandation et une sidebar
st.set_page_config(page_title="WeHo", page_icon="img/icon.svg", layout="wide")


st.title('Dashboard!')





# -- Connexion à BigQuery à isoler dans un module séparé --
def get_historical_data():
    # Simuler ici la récupération de données depuis BigQuery
    dates = pd.date_range(end=datetime.now(), periods=100, freq='H')
    indoor_temp = 20 + 2 * np.sin(np.linspace(0, 10, 100))
    indoor_humidity = 40 + 10 * np.cos(np.linspace(0, 5, 100))
    air_quality = 50 + 20 * np.sin(np.linspace(0, 3, 100))
    df = pd.DataFrame({'datetime': dates,
                       'indoor_temp': indoor_temp,
                       'indoor_humidity': indoor_humidity,
                       'air_quality': air_quality})
    return df

def main():
    st.title("Dashboard météo indoor/outdoor")
    st.markdown("### Visualisation des données historiques")

    # Récupérer données
    df = get_historical_data()

    # Sélection période
    start_date = st.date_input("Date début", df['datetime'].min().date())
    end_date = st.date_input("Date fin", df['datetime'].max().date())

    mask = (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)
    df_filtered = df.loc[mask]

    # Graphiques
    fig_temp = px.line(df_filtered, x='datetime', y='indoor_temp', title='Température intérieure (°C)')
    fig_humidity = px.line(df_filtered, x='datetime', y='indoor_humidity', title='Humidité intérieure (%)')
    fig_air = px.line(df_filtered, x='datetime', y='air_quality', title='Qualité de l\'air')

    st.plotly_chart(fig_temp)
    st.plotly_chart(fig_humidity)
    st.plotly_chart(fig_air)

    # Alertes basiques
    latest = df.iloc[-1]
    if latest['indoor_humidity'] < 40:
        st.warning(f"Attention : humidité intérieure basse ({latest['indoor_humidity']:.1f}%) !")
    if latest['air_quality'] > 70:
        st.error(f"Qualité de l'air mauvaise ({latest['air_quality']:.1f}) !")

if __name__ == "__main__":
    main()
