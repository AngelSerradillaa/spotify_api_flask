from dotenv import load_dotenv
load_dotenv()
'''from flask import redirect, Request'''
import os
import base64
import time
import random
import string
import urllib
import requests

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_ID_SECRET = os.getenv("CLIENT_ID_SECRET")
URL_TOKEN = "https://accounts.spotify.com/api/token"
REDIRECT_URL = "http://localhost:8000/callback"

def get_token(code: str):
    '''auth_string = f"{CLIENT_ID}:{CLIENT_ID_SECRET}"              Primero probé de esta forma pero me salía invalid user id por lo que probé con el client_token,
    auth_bytes = auth_string.encode("utf-8")                        solución que encontré en internet después de darle bastantes vueltas ya que este método lo utilizan
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")        en un vídeo y funciona correctamente.
    print(f"Basic {auth_base64}")
    url = URL_TOKEN
    headers = {
    "Authorization": f"Basic {auth_base64}",
    "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials"
    }
    result = requests.post(url, headers=headers, data=data)'''

    client_token = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_ID_SECRET,
    }

    result = requests.post(URL_TOKEN, data=client_token)

    # Manejo de errores para evitar fallos si algo no está en el JSON
    if result.status_code == 200:
        json_result = result.json()
        access_token = json_result["access_token"]
        refresh_token = json_result["refresh_token"]
        expires_in = time.time() + json_result["expires_in", 0]

        return access_token
    else:
        print("Error al obtener el token:", result.status_code, result.content)
        return None

def generar_string_aleatorio():
    caracteres = string.ascii_letters + string.digits  # Letras (a-z, A-Z) y números (0-9)
    return ''.join(random.choice(caracteres) for _ in range(16))

def get_auth_url():
    state = generar_string_aleatorio()
    scope = "user-read-private user-read-email"

    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URL,
        'scope': scope,
        'state': state
    }

    return f"{"https://accounts.spotify.com/authorize"}?{urllib.parse.urlencode(params)}"



'''encoded_value = "YmNkOTAwZGZhNWQ2NGYwZWFlZjQxOWJiZTYwZDZiZDY6ODMwNzMwMjRhMjA5NGRkYmE0YjlmNDNhNDlhNDMyM2I="
decoded_value = base64.b64decode(encoded_value).decode("utf-8")
print(decoded_value)'''

