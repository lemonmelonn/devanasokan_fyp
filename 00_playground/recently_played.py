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
    scope="user-read-recently-played"
))

# Get last 10 recently played tracks (title, artist, album)
def get_recently_played():
    recently_played = sp.current_user_recently_played(limit=10)

    if recently_played and recently_played["items"]:
        tracks_info = []
        for item in recently_played["items"]:
            track = item["track"]
            track_info = {
                "title": track["name"],
                "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "album": track["album"]["name"]
            }
            tracks_info.append(track_info)
        return tracks_info
    else:
        return None

recently_played = get_recently_played()
for idx, track in enumerate(recently_played, start=1):
    print(f"{idx}. {track['title']} -- {track['artist']} -- '{track['album']}'")