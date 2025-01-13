from pydantic import BaseModel
from typing import Optional
import json
import os
from passlib.context import CryptContext

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "json_manage", "users.json")

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

class User(BaseModel):
    username: str
    password: str
    full_name: str = None