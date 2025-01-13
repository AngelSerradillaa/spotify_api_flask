import os
import json

from fastapi import HTTPException
from users_manage import load_users
def save_search_results(username: str, search_type: str, query: str, results: dict):
    
    users = load_users()

    if not username in users:
        raise HTTPException(status_code=400, detail=f"No se ha introducido un usuario registrado.")

    # Crear una carpeta para los usuarios si no existe
    user_folder = f"search_results/{username}"
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Definir el archivo JSON donde se guardarán los resultados de la búsqueda
    file_path = os.path.join(user_folder, f"{search_type}_{query}.json")

    # Guardar los resultados de la búsqueda en el archivo
    with open(file_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Resultados guardados en {file_path}")