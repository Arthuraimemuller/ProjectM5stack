## 📁 Project Structure

```plaintext
ProjectM5stack/
│
├── 📁 backend/
│   ├── __init__.py
│   ├── 📁 api/                  # Communication avec BigQuery, OpenWeather, etc.
│   │   ├── bigquery_service.py
│   │   ├── weather_service.py
│   │   └── presence_service.py
│   ├── 📁 core/                 # Logique métier (alertes, calculs, seuils)
│   │   └── logic.py
│   ├── 📁 config/               # Paramètres globaux
│   │   ├── settings.py
│   │   └── secrets.env         # Fichier à ne pas push sur Git
│   ├── main.py                 # Point d'entrée backend (Flask ou API handler)
│   └── readme.md
│
├── 📁 frontend/                 # Streamlit
│   ├── 📁 .streamlit/
│   │   └── config.toml
│   ├── 📁 app/                  # Code principal Streamlit
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── 📁 pages/
│   │   │   └── historical.py
│   │   └── 📁 components/
│   │       └── charts.py
│   ├── 📁 assets/               # Images/icônes météo
│   ├── Dockerfile
│   └── readme.md
│
├── 📁 device_ui/               # UI pour M5Stack
│   ├── 📁 display/
│   │   └── ui_main.py          # Affichage des données
│   ├── 📁 sensors/
│   │   ├── env_sensor.py
│   │   ├── air_quality.py
│   │   └── motion_sensor.py
│   ├── 📁 tts/
│   │   └── speech_announcer.py
│   ├── 📁 sync/
│   │   └── sync_bigquery.py
│   └── main.py                 # Point d'entrée M5Stack
│
├── 📁 shared/                  # Code partagé : fonctions utiles, constantes
│   ├── utils.py
│   └── constants.py
│
├── 📁 design/                  # Design de l’UI
│   ├── 📁 existing/
│   ├── 📁 sketches/
│   └── 📁 mockups/
│
├── 📁 tests/
│   ├── 📁 backend/
│   ├── 📁 frontend/
│   └── 📁 device/
│
├── README.md
├── requirements.txt
└── .gitignore
```
