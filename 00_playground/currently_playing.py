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

def get_currently_playing():
    current = sp.current_user_playing_track()

    if current and current["is_playing"]:
        return {
            "song": current["item"]["name"],
            "artist": current["item"]["artists"][0]["name"],
            "album": current["item"]["album"]["name"],
            "album_cover": current["item"]["album"]["images"][0]["url"]
        }
    else:
        return None

currently_playing = get_currently_playing()
print(currently_playing)