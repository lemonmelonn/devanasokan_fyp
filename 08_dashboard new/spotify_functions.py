import base64
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import session

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
CURRENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8050/callback")
SPOTIFY_SCOPES = "user-read-currently-playing user-read-playback-state"


class SpotifyAuthError(Exception):
    pass


def build_spotify_auth_url():
    if not CLIENT_ID:
        raise SpotifyAuthError("Spotify client ID is not configured.")

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": SPOTIFY_SCOPES,
        "redirect_uri": REDIRECT_URI,
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(code):
    if not code:
        raise SpotifyAuthError("Missing authorization code.")

    if not CLIENT_ID or not CLIENT_SECRET:
        raise SpotifyAuthError("Spotify client credentials are not configured.")

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    token_headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(TOKEN_URL, data=token_data, headers=token_headers, timeout=15)
    token_json = response.json()

    if response.status_code != 200 or "access_token" not in token_json:
        raise SpotifyAuthError(f"Token exchange failed: {token_json}")

    token_json["expires_at"] = time.time() + int(token_json.get("expires_in", 3600)) - 60
    return token_json


def refresh_spotify_token(refresh_token):
    if not refresh_token:
        raise SpotifyAuthError("Missing refresh token.")

    if not CLIENT_ID or not CLIENT_SECRET:
        raise SpotifyAuthError("Spotify client credentials are not configured.")

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    token_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    token_headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(TOKEN_URL, data=token_data, headers=token_headers, timeout=15)
    token_json = response.json()

    if response.status_code != 200 or "access_token" not in token_json:
        raise SpotifyAuthError(f"Token refresh failed: {token_json}")

    token_json["refresh_token"] = token_json.get("refresh_token", refresh_token)
    token_json["expires_at"] = time.time() + int(token_json.get("expires_in", 3600)) - 60
    return token_json


def clear_spotify_session():
    session.pop("spotify_auth", None)


def store_spotify_session(token_json):
    session["spotify_auth"] = {
        "access_token": token_json.get("access_token"),
        "refresh_token": token_json.get("refresh_token"),
        "token_type": token_json.get("token_type"),
        "scope": token_json.get("scope"),
        "expires_at": token_json.get("expires_at"),
    }


def is_spotify_authenticated():
    auth = session.get("spotify_auth")
    return bool(auth and auth.get("access_token"))


def get_spotify_access_token_from_session():
    auth = session.get("spotify_auth")

    if not auth:
        return None

    access_token = auth.get("access_token")
    expires_at = auth.get("expires_at")
    refresh_token = auth.get("refresh_token")

    if access_token and expires_at and time.time() < float(expires_at):
        return access_token

    if refresh_token:
        refreshed = refresh_spotify_token(refresh_token)
        store_spotify_session(refreshed)
        return refreshed.get("access_token")

    clear_spotify_session()
    return None

# Function to get details of given song
def get_song_details(song_title, artist_name, access_token):
    """
    Search Spotify for a song using title and artist.

    Returns:
        dict containing song details, or None if not found.
    """

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    queries = []
    if song_title and artist_name:
        queries.append(f'track:"{song_title}" artist:"{artist_name}"')
    if song_title:
        queries.append(f'track:"{song_title}"')
    if song_title and artist_name:
        queries.append(f"{song_title} {artist_name}")

    track = None

    for query in queries:
        params = {
            "q": query,
            "type": "track",
            "limit": 10
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return None

        data = response.json()
        tracks = data.get("tracks", {}).get("items", [])

        if not tracks:
            continue

        if artist_name:
            normalized_artist = artist_name.strip().lower()

            for candidate in tracks:
                candidate_artists = [artist["name"].strip().lower() for artist in candidate.get("artists", [])]

                if any(normalized_artist in artist_name_value for artist_name_value in candidate_artists):
                    track = candidate
                    break

        if track is None:
            track = tracks[0]

        if track is not None:
            break

    if track is None:
        print("Song not found")
        return None

    return {
        "song_id": track["id"],
        "title": track["name"],
        "artist": ", ".join([artist["name"] for artist in track["artists"]]),
        "album": track["album"]["name"],
        "explicit": track["explicit"]
    }


def get_currently_playing(access_token=None):
    if access_token is None:
        access_token = get_spotify_access_token_from_session()

    if not access_token:
        return None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(CURRENTLY_PLAYING_URL, headers=headers, timeout=15)

    if response.status_code == 204:
        return None

    if response.status_code == 401:
        clear_spotify_session()
        raise SpotifyAuthError("Spotify session expired.")

    if response.status_code != 200:
        raise SpotifyAuthError(f"Spotify API error: {response.status_code}")

    current = response.json()
    item = current.get("item")

    if not item:
        return None

    return {
        "song_id": item["id"],
        "title": item["name"],
        "artist": item["artists"][0]["name"],
        "album": item["album"]["name"],
        "album_image": item["album"]["images"][0]["url"] if item["album"].get("images") else None,
        "explicit": item["explicit"],
        "id": item["artists"][0]["id"]
    }

# currently_playing = get_currently_playing()
# print(currently_playing)

# artist = sp.artist(currently_playing["id"])
# print(artist["genres"])


# Returns a Spotify access token using Client Credentials Flow
def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )

    response.raise_for_status()
    return response.json()["access_token"]


# Searches for an album by name and returns the first match
def find_album(album_name):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": album_name,
        "type": "album",
        "limit": 1
    }

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers=headers,
        params=params
    )

    response.raise_for_status()

    albums = response.json()["albums"]["items"]

    if not albums:
        return None

    return albums[0]


# Returns the tracks of a given album
def get_album_tracks(album_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"https://api.spotify.com/v1/albums/{album_id}/tracks",
        headers=headers
    )

    response.raise_for_status()

    return response.json()["items"]


def search_possible_songs(query, limit=5):
    """
    Search songs using Spotify API
    Returns list formatted for Dash dropdown
    """

    if not query:
        return []

    token = get_access_token()

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query, "type": "track", "limit": limit},
        timeout=15,
    )

    response.raise_for_status()

    items = response.json()["tracks"]["items"]

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