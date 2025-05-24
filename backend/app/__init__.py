import os
from dotenv import load_dotenv
from flask import Flask


from config import load_config
load_config()

from app.api.indoor import indoor_api, init_indoor_routes
init_indoor_routes()  # ✅ Corrigé
from app.api.outdoor import outdoor_api
#from app.api.forecast import forecast_api
#from app.api.system import system_api


load_dotenv(os.path.join(os.path.dirname(__file__), "config/secrets.env"))

def create_app():
    app = Flask(__name__)

    # Enregistrement des blueprints
    app.register_blueprint(indoor_api)
    app.register_blueprint(outdoor_api)
    #app.register_blueprint(forecast_api)
    #app.register_blueprint(system_api)

    return app
