# import os
# from dotenv import load_dotenv
# from flask import Flask
#
#
# from config import load_config
# load_config()
#
# from app.api.indoor import indoor_api, init_indoor_routes
# init_indoor_routes()  # ✅ Corrigé
# from app.api.outdoor import outdoor_api
# #from app.api.forecast import forecast_api
# #from app.api.system import system_api
#
#
# load_dotenv(os.path.join(os.path.dirname(__file__), "config/secrets.env"))
#
# def create_app():
#     app = Flask(__name__)
#
#     # Enregistrement des blueprints
#     app.register_blueprint(indoor_api)
#     app.register_blueprint(outdoor_api)
#     #app.register_blueprint(forecast_api)
#     #app.register_blueprint(system_api)
#
#     return app


import os
from flask import Flask
from config import load_config
from dotenv import load_dotenv

# 🔁 Charge les variables d'environnement dès le début
load_config()  # charge config/secrets.env via dotenv

# ❌ Plus besoin de recharger dotenv manuellement ici :
# load_dotenv(os.path.join(os.path.dirname(__file__), "config/secrets.env"))

# ✅ Import du nouveau blueprint unifié
from app.api.measurements import measurements_api, init_measurements_routes
init_measurements_routes()  # Initialise le BigQueryService

def create_app():
    app = Flask(__name__)

    # ✅ Enregistrement du seul blueprint nécessaire
    app.register_blueprint(measurements_api)

    return app
