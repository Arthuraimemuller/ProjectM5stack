# ProjectM5stack (written using chatgpt)
Final project for the Cloud and Advanced Analytics course, designed to integrate all the acquired knowledge and utilize a connected IoT device as a weather station.

First I have imagined some designed like in Interaction Design. I wanted to add a circle animation, however it renders not very well on the M5stack (you can test them on the pygame folder). I choose an other option with no animation but interactive buttons.
There is a video of the M5stack UI, which consist of three buttons that rotate clockwise the humidity or indoor/outdoor temperature. 
It allows user to little bit customize their frontend, and the button are large enough to be click. I found not easy to use the small buttons from the menu page of the application.

The code for UI is contained in `4. Triangle`.

Furthermore I have added the video `video_rotating_m5stack.mp4`. 

I had time to add the backend (very small) and check that it connect and add data to Bigquery.

# UIm5stack

https://rop.nl/truetype2gfx/

# 🌍 ProjectM5stack

**Une plateforme IoT complète** basée sur le microcontrôleur M5Stack Core2, avec interface Web (Streamlit), backend Python (API météo, BigQuery), et une suite de tests pour l'UI embarquée sur l'écran du M5Stack.

---

## 📁 Structure du projet

```plaintext
ProjectM5stack/
│
├── backend/               # API Python + config BigQuery/OpenWeather
│   ├── app/
│   │   ├── api/           # Services d'accès à BigQuery et OpenWeather
│   │   ├── config/        # Secrets et fichiers de config
│   │   ├── app.py         # Point d'entrée principal
│   │   └── key_bigquery.json
│
├── frontend/              # Interface utilisateur Streamlit
│   ├── app/
│   │   ├── pages/         # Pages Streamlit
│   │   ├── .streamlit/    # Thèmes (config.toml)
│   │   └── home.py        # Page d'accueil principale
│
├── UIM5Stack/             # Tests UI et animations sur écran M5Stack
│   ├── M5stackTests/      # Visualisations et boutons
│   └── PygameTests/       # Simulations et prototypes sur PC
