# spotify_functions.py

import requests
from dotenv import load_dotenv
import os
from spotipy import Spotify

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Create a Spotify client with an access token
def get_spotify_client(access_token):
    return Spotify(auth=access_token)

# Spotify OAuth functions
def get_auth_url():
    scopes = "user-read-currently-playing"
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scopes}&show_dialog=true"
    return auth_url

# Exchange authorization code for access token
def exchange_code_for_token(code):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

# Get currently playing track
def get_currently_playing(access_token):
    sp = get_spotify_client(access_token)
    current = sp.current_user_playing_track()

    if current and current["is_playing"]:
        return {
            "song_id": current["item"]["id"],
            "title": current["item"]["name"],
            "artist": current["item"]["artists"][0]["name"],
            "album": current["item"]["album"]["name"],
            "album_image": current["item"]["album"]["images"][0]["url"],
            "explicit": current["item"]["explicit"],
            "id": current["item"]["artists"][0]["id"]
        }
    else:
        return None

# Search for songs using the Spotify API
def search_possible_songs(query, limit=5):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    token = response.json()["access_token"]
    sp = get_spotify_client(token)
    
    results = sp.search(q=query, type="track", limit=limit)
    items = results["tracks"]["items"]

    formatted = []
    for item in items:
        formatted.append({
            "song_id": item["id"],
            "title": item["name"],
            "artist": item["artists"][0]["name"],
            "album": item["album"]["name"],
            "album_cover": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
            "explicit": item["explicit"]
        })

    return formatted

# Get Client Credentials token for general searches
def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    response.raise_for_status()
    return response.json()["access_token"]

# Get the current user's display name or ID
def get_current_user(access_token):
    sp = get_spotify_client(access_token)
    user = sp.current_user()
    return user.get("display_name") or user.get("id")