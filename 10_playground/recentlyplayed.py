import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Replace these with your own
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-recently-played"
))

print("Tracking your Spotify listening activity...\n")

last_song = None

while True:
    results = sp.current_user_recently_played(limit=1)

    track = results['items'][0]['track']
    song = track['name']
    artist = track['artists'][0]['name']

    current_song = f"{song} - {artist}"

    if current_song != last_song:
        print(f"New song detected: {current_song}")
        last_song = current_song

    time.sleep(5)