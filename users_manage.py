from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os
from passlib.context import CryptContext
from cachetools import TTLCache

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "json_manage", "users.json")

user_cache = TTLCache(maxsize=100, ttl=3600)

def load_users():
    if not os.path.exists(os.path.dirname(USERS_FILE)):
        os.makedirs(os.path.dirname(USERS_FILE))
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            json.dump({}, file)
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


def save_logged_user(username: str):
    user_cache["logged_user"] = username
    print(f"Usuario {username} guardado en caché.")

def get_logged_user() -> str:
    if "logged_user" not in user_cache:
        raise HTTPException(status_code=401, detail="No hay usuario logueado.")
    return user_cache["logged_user"]

class User(BaseModel):
    username: str
    password: str
    full_name: str = None