# 🌤️ Streamlit Frontend - Météo Dashboard

Ce projet est une interface Streamlit déployée sur Google Cloud Run.  
Elle affiche les données météo actuelles et les prévisions à partir d’une API backend, ainsi que des données issues de capteurs (via BigQuery).

## 🚀 Accès à l'application

👉 [Cliquez ici pour accéder à l'interface Streamlit en ligne](https://docker-flask-frontend-project-688745668065.europe-west6.run.app/)

[https://docker-flask-frontend-project-688745668065.europe-west6.run.app/](https://docker-flask-frontend-project-688745668065.europe-west6.run.app/)
## 🔧 Description

Ce frontend est conçu avec :
- [Streamlit](https://streamlit.io/) pour l'interface utilisateur
- Docker pour le conteneuriser
- Google Cloud Run pour le déploiement

Il consomme des données depuis :
- **OpenWeatherMap** pour la météo actuelle et les prévisions
- **BigQuery** via un backend Flask (également déployé sur Cloud Run) pour afficher des données de capteurs en temps réel.

## 📦 Contenu

- `main.py` – Application principale Streamlit
- `Dockerfile` – Pour déployer le frontend sur Cloud Run
- `requirements.txt` – Dépendances Python

