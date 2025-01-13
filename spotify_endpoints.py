from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
from spotify_connect import get_auth_url, get_valid_token, load_token, refresh_token, is_token_expired
from search_manage import save_search_results
from users_manage import get_logged_user

router = APIRouter()

#Endpoints con spotify api
@router.get("/login")
def login():
    auth_url = get_auth_url()
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def api_callback(request: Request):
    
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    token_data = get_valid_token(code, error)

    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    expires_in = token_data["expires_in"]

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

@router.get("/search/{type}/{query}")
def searchWithParams(type: str, query: str):


    token_data = load_token()
    if is_token_expired(token_data):
        print("El token ha expirado, renovando...")
        token_data = refresh_token(token_data["refresh_token"])

    access_token = token_data["access_token"]
    url = f"https://api.spotify.com/v1/search?q={query}&type={type}&limit=10"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        results = response.json()

        # Guardar los resultados en un archivo JSON específico para el usuario
        user = get_logged_user()
        save_search_results(user, type, query, results)

        return results
    else:
        print(f"Error al buscar en Spotify: {response.status_code}, {response.content}")
        return None