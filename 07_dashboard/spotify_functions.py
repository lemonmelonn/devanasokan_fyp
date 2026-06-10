import requests
from dotenv import load_dotenv
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ALBUM_NAME = "1989"

# Initialize Spotify client with user-read-currently-playing scope
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:5000/callback",
    scope="user-read-currently-playing"
))

def get_currently_playing():
    current = sp.current_user_playing_track()

    if current and current["is_playing"]:
        return {
            "explicit": current["item"]["explicit"],
            "song": current["item"]["name"],
            "artist": current["item"]["artists"][0]["name"],
            "album": current["item"]["album"]["name"],
            "id": current["item"]["artists"][0]["id"]
        }
    else:
        return None

currently_playing = get_currently_playing()
print(currently_playing)

artist = sp.artist(currently_playing["id"])
print(artist["genres"])


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


# token = get_access_token()
# album = find_album(ALBUM_NAME)

# if album:
#     print("Album:", album["name"], album["id"])
#     print("Artist:", album["artists"][0]["name"])

#     tracks = get_album_tracks(album["id"], token)

#     print("\nTracks:")
#     for track in tracks:
#         print(track["track_number"], "-", track["name"])
# else:
#     print("Album not found")