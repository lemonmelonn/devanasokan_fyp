import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

artists = ["Taylor Swift", "Ed Sheeran", "Adele"]

def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=30
    )

    response.raise_for_status()
    return response.json()["access_token"]


def get_all_artist_songs(artist_name, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    artists = response.json()["artists"]["items"]

    if not artists:
        return None

    artist_id = artists[0]["id"]

    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US",
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    tracks = response.json()["tracks"]
    return [track["name"] for track in tracks]


def get_artist_albums(artist_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    albums = []
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"

    while url:
        response = requests.get(
            url,
            headers=headers,
            timeout=30,
            params={
                "include_groups": "album,single",
                "limit": 50
            }
        )

        response.raise_for_status()

        data = response.json()

        albums.extend(data["items"])

        url = data["next"]

    return albums


def get_album_tracks(album_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    tracks = []
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"

    while url:
        response = requests.get(
            url,
            headers=headers,
            params={"limit": 50},
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        tracks.extend(data["items"])

        url = data["next"]

    return tracks

def get_artist_id(artist_name, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    artists = response.json()["artists"]["items"]

    if not artists:
        return None

    return artists[0]["id"]

token = get_access_token()

all_artist_songs = {}

for artist_name in artists:
    print(f"Fetching songs for {artist_name}...")

    artist_id = get_artist_id(artist_name, token)

    if not artist_id:
        all_artist_songs[artist_name] = []
        continue

    albums = get_artist_albums(artist_id, token)
    songs = set()

    for album in albums:
        tracks = get_album_tracks(album["id"], token)

        for track in tracks:
            songs.add(track["name"])

    all_artist_songs[artist_name] = sorted(songs)
    print(f"Found {len(all_artist_songs[artist_name])} unique songs for {artist_name}")

with open("artist_songs.csv", "w", encoding="utf-8") as f:
    f.write("Artist,Song\n")

    for artist_name, songs in all_artist_songs.items():
        for song in songs:
            f.write(f"{artist_name},{song}\n")

for artist_name, songs in all_artist_songs.items():
    print(f"{artist_name}: {len(songs)} songs")