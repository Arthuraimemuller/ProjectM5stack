import os
from dotenv import load_dotenv

# Toujours charger le .env AVANT de lire les variables d'env !
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


class Settings:
    def __init__(self):
        self.GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "default_project")
        self.BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "default_dataset")
        self.BQ_TABLE_ID = os.getenv("BQ_TABLE_ID", "default_table")
        self.OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
        self.GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        # S'assure que la variable d'environnement est bien set pour les librairies Google
        if self.GOOGLE_APPLICATION_CREDENTIALS:
            abs_path = self.GOOGLE_APPLICATION_CREDENTIALS
            if not os.path.isabs(abs_path):
                # Le chemin dans .env est relatif à "backend/", donc on le base sur ce dossier                !!!!! vraiment important pour que quand on lance les tests en lancant avec Pycharm, ils s'executent correctement. Autrement, il est possible de lancer en cmd, e.g "python -m unittest tests.test_measurements".
                backend_root = os.path.dirname(os.path.dirname(__file__))  # == dossier "backend"
                abs_path = os.path.abspath(os.path.join(backend_root, self.GOOGLE_APPLICATION_CREDENTIALS))
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = abs_path
            #print("GOOGLE_APPLICATION_CREDENTIALS points to:", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
            #print("File exists?", os.path.isfile(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]))
        else:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is required. Please set it in your .env file.")

        if not self.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY is required. Please set it in your .env file.")

    def as_dict(self):
        return self.__dict__


settings = Settings()
#print(settings.as_dict())
