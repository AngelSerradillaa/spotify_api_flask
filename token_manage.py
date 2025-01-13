import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "json_manage", "token.json")

def save_token(token_data: dict):
    """
    Guarda los datos del token en un archivo JSON.
    """
    with open(TOKEN_FILE, "w") as file:
        json.dump(token_data, file, indent=4)

def load_token():
    """
    Carga el token desde el archivo JSON, si existe.
    """
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    return None