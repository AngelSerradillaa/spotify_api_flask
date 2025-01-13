from dotenv import load_dotenv
load_dotenv()
'''from flask import redirect, Request'''
import os
import requests
import time
import random
import string
import urllib
import requests
from token_manage import save_token, load_token
from fastapi import HTTPException


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_ID_SECRET = os.getenv("CLIENT_ID_SECRET")
URL_TOKEN = "https://accounts.spotify.com/api/token"
REDIRECT_URL = "http://localhost:8000/callback"

def get_valid_token(code:str, error:str):

    if error:
        raise HTTPException(status_code=400, detail=f"Spotify ha retornado el siguiente error: {error}")
    if not code:
       raise HTTPException(status_code=400, detail="No se ha retornado código de autorización")
    
    token_data = load_token()

    if not token_data["access_token"] or not token_data["refresh_token"]or not token_data["expires_in"]:
        print("No hay token se va a realizar el getToken")
        token_data = get_token(code)

    if is_token_expired(token_data):
        print("El token ha expirado, renovando...")
        token_data = refresh_token(token_data["refresh_token"])

    if not token_data:
        raise HTTPException(status_code=500, detail="No se pudo obtener el token de Spotify")
    
    return token_data

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
        access_token = json_result.get("access_token")
        refresh_token = json_result.get("refresh_token")
        expires_in = time.time() + json_result.get("expires_in", 0)

        token_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": expires_in,
            "timestamp": time.time()
        }
        print(token_data)
        save_token(token_data)

        return token_data
    else:
        print("Error al obtener el token:", result.status_code, result.content)
        return None

def refresh_token(refresh_token: str):
    """
    Renueva el access_token utilizando el refresh_token.
    """
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_ID_SECRET,
    }

    result = requests.post(URL_TOKEN, data=data)

    if result.status_code == 200:
        json_result = result.json()

        # Estructura del nuevo token a guardar
        token_data = {
            "access_token": json_result["access_token"],
            "refresh_token": refresh_token,  # El refresh_token no cambia
            "expires_in": json_result["expires_in"],
            "timestamp": time.time()
        }
        print(token_data)
        save_token(token_data)

        return token_data
    else:
        print("Error al renovar el token:", result.status_code, result.content)
        return None

def is_token_expired(token_data):
    """
    Verifica si el token ha expirado comparando el tiempo actual con el timestamp.
    """
    current_time = time.time()
    if token_data["expires_in"] is None or token_data["timestamp"] is None:
        return True 

    expires_in = token_data["expires_in"]
    timestamp = token_data["timestamp"]

    return current_time > (timestamp + expires_in)

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

