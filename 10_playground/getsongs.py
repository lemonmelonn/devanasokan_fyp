import requests
import os
import pandas as pd
import time
import base64
from dotenv import load_dotenv

# =========================
# 🔑 CONFIG
# =========================
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ARTIST_NAME = "Drake"   # change this


def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
        ).decode()
    }

    data = {
        "grant_type": "client_credentials"
    }

    res = requests.post(url, headers=headers, data=data)
    return res.json()['access_token']

# =========================
# 🔍 STEP 1: Get Artist ID
# =========================
def get_artist_id(artist_name):
    url = "https://api.spotify.com/v1/search"
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }
    res = requests.get(url, headers=get_access_token, params=params).json()
    print(res)
    return res['artist']['items'][0]['id']


# =========================
# 📀 STEP 2: Get All Albums
# =========================
def get_all_albums(artist_id):
    albums = []
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"

    params = {
        "limit": 50,
        "include_groups": "album,single"
    }

    while url:
        res = requests.get(url, headers=get_access_token, params=params).json()
        albums.extend(res['items'])
        url = res.get('next')
        params = None  # important after first request

    # remove duplicate albums
    unique_albums = {}
    for album in albums:
        unique_albums[album['id']] = album

    return list(unique_albums.values())


# =========================
# 🎵 STEP 3: Get Tracks
# =========================
def get_tracks_from_album(album):
    tracks = []
    url = f"https://api.spotify.com/v1/albums/{album['id']}/tracks"

    while url:
        res = requests.get(url, headers=get_access_token).json()
        tracks.extend(res['items'])
        url = res.get('next')

    return tracks


# =========================
# 🚀 MAIN PIPELINE
# =========================
def get_artist_songs(artist_name):
    dsf = get_access_token()
    print(dsf)
    artist_id = get_artist_id(artist_name)
    print(f"Artist ID: {artist_id}")

    albums = get_all_albums(artist_id)
    print(f"Found {len(albums)} albums")

    all_tracks = []

    for album in albums:
        tracks = get_tracks_from_album(album)

        for track in tracks:
            track_data = {
                "artist": artist_name,
                "album_name": album['name'],
                "album_release_date": album['release_date'],
                "album_type": album['album_type'],
                "track_name": track['name'],
                "track_id": track['id'],
                "track_number": track['track_number'],
                "duration_ms": track['duration_ms'],
                "explicit": track['explicit'],
                "disc_number": track['disc_number'],
                "track_url": track['external_urls']['spotify'],
                "album_id": album['id']
            }
            all_tracks.append(track_data)

        time.sleep(0.2)  # avoid rate limits

    return pd.DataFrame(all_tracks)


# =========================
# ▶️ RUN
# =========================
# Test it
token = get_access_token()
print(token)

df = get_artist_songs(ARTIST_NAME)

print(df.head())
print(f"Total songs: {len(df)}")

# Save to CSV
df.to_csv(f"{ARTIST_NAME}_songs.csv", index=False)