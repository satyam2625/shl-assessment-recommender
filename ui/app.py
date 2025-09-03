import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def get_recommendations(query):
    resp = requests.get(f"{API_URL}/recommend", params={"query": query}, timeout=20)
    resp.raise_for_status()
    return resp.json()
# rest of the app...
