import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

ALBUM_NAME = "1989"


def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )

    response.raise_for_status()
    return response.json()["access_token"]


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


token = get_access_token()

album = find_album(ALBUM_NAME)

if album:
    print("Album:", album["name"], album["id"])
    print("Artist:", album["artists"][0]["name"])

    tracks = get_album_tracks(album["id"], token)

    print("\nTracks:")
    for track in tracks:
        print(track["track_number"], "-", track["name"])
else:
    print("Album not found")