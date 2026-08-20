# spotify_functions.py

import requests
from dotenv import load_dotenv
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Initialize Spotify client with user-read-currently-playing scope
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:5000/callback",
    scope="user-read-currently-playing"
))

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

# Function to get the currently playing song for the authenticated user
def get_currently_playing():
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


# Returns a Spotify access token using Client Credentials Flow
def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )

    response.raise_for_status()
    return response.json()["access_token"]


# Function to search for possible songs based on a query
def search_possible_songs(query, limit=5):
    """
    Search songs using Spotify API
    Returns list formatted for Dash dropdown
    """

    if not query:
        return []

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