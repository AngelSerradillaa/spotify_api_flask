'''from flask import Flask, request, jsonify, redirect, Request, abort, Response      Empecé con flask pero conseguía que funcionase y después de horas de intentarlo y 
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
import uvicorn

app = FastAPI()

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
    print(token)

    return HTMLResponse(content=f'''
        <html>
            <body>
                <h1>El token ha sido almacenado correctamente.</h1>
                <p>Puedes ir a la documentación para probar los endpoints <a href="/docs">aquí</a>.</p>
            </body>
        </html>
    ''')

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8000/login")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)