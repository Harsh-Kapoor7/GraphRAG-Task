## authentication.py
import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

USER_DATA_FILE = "users.json"

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

if "users" not in st.session_state:
    st.session_state.users = load_users()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def authenticate(username, password):
    return username in st.session_state.users and st.session_state.users[username] == password

def register(username, password):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = password
    save_users(st.session_state.users)
    return True