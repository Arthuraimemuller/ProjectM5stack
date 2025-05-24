import os
from dotenv import load_dotenv

def load_config():
    env_path = os.path.join(os.path.dirname(__file__), 'secrets.env')
    load_dotenv(dotenv_path=env_path, override=False)
