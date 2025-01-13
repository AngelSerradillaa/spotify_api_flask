'''from flask import Flask, request, jsonify, redirect, Request, abort, Response      Empecé con flask pero no conseguía que funcionase y después de horas de intentarlo y 
from spotify_service import get_auth_url, get_token                                   no saber qué hacer probé con FastAPI a ver si funcionaba y efectivamente.
import webbrowser
import requests

app = Flask(__name__)

@app.route('/login')
def login():
    auth_url = get_auth_url()
    return redirect(auth_url)

@app.route('/callback')
async def api_callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        abort(status_code=400, detail=f"Spotify ha retornado el siguiente error: {error}")
    if not code:
       abort(status_code=400, detail="No se ha retornado código de autorización")
    
    token = get_token(code)
    print(token)

if __name__ == "__main__":
    webbrowser.open("https://127.0.0.1:8000/login")
    app.run(port=8000, debug=True)'''

import uuid
from fastapi import FastAPI, HTTPException, Request 
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import webbrowser
from spotify_connect import get_auth_url, get_token
from users_manage import User, save_users, load_users
from passlib.context import CryptContext
import uvicorn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

#Endpoints con spotify api
@app.get("/login")
def login():
    auth_url = get_auth_url()
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def api_callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        raise HTTPException(status_code=400, detail=f"Spotify ha retornado el siguiente error: {error}")
    if not code:
       raise HTTPException(status_code=400, detail="No se ha retornado código de autorización")
    
    token = get_token(code)

    if not token:
        raise HTTPException(status_code=500, detail="No se pudo obtener el token de Spotify")

    access_token = token["access_token"]
    refresh_token = token["refresh_token"]
    expires_in = token["expires_in"]

    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
    print(f"Expires In: {expires_in}")

    return HTMLResponse(content=f'''
        <html>
            <body>
                <h1>El token ha sido almacenado correctamente.</h1>
                <p>Access Token: {access_token}</p>
                <p>Refresh Token: {refresh_token}</p>
                <p>Expires In: {expires_in}</p>
                <p>Puedes ir a la documentación para probar los endpoints <a href="/docs">aquí</a>.</p>
            </body>
        </html>
    ''')



#Crear usuario
@app.post("/users/")
def create_user(user: User):
    users = load_users()

    if user.username in users:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = pwd_context.hash(user.password)
    users[user.username] = {"password": hashed_password, "full_name": user.full_name}
    save_users(users)
    return {"message": f"Usuario {user.username} creado exitosamente"}

#Eliminar usuario
@app.delete("/users/{username}")
def delete_user(username: str):
    users = load_users()

    if username not in users:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    del users[username]
    save_users(users)
    return {"message": f"Usuario {username} eliminado exitosamente"}

#Actualizar usuario
@app.put("/users/{username}")
def update_user(username: str, user: User):
    users = load_users()

    if username not in users:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    hashed_password = pwd_context.hash(user.password)
    users[username] = {"password": hashed_password, "full_name": user.full_name}
    save_users(users)
    return {"message": f"Usuario {username} actualizado exitosamente"}

#Loguear usuario
@app.post("/login-user/")
def login(user: User):
    users = load_users()

    if user.username not in users:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    stored_user = users[user.username]
    if not pwd_context.verify(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    
    return {"message": f"Usuario {user.username} autenticado exitosamente"}



if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8000/login")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)