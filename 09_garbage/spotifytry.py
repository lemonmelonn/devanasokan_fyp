import os
import base64
import urllib.parse
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = "dev_secret_key"

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# IMPORTANT: must match Spotify Dashboard EXACTLY
REDIRECT_URI = "http://127.0.0.1:5000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    if "access_token" in session:
        return """
        <h2>🎧 Logged in</h2>
        <a href="/current"><button>Now Playing</button></a>
        <br><br>
        <a href="/logout"><button>Logout</button></a>
        """

    return """
    <h2>Spotify OAuth Demo</h2>
    <a href="/login"><button>Login with Spotify</button></a>
    """


# -------------------------
# LOGIN
# -------------------------
@app.route("/login")
def login():
    scope = "user-read-currently-playing user-read-playback-state"

    auth_url = (
        f"{AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&scope={urllib.parse.quote(scope)}"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    )

    return redirect(auth_url)


# -------------------------
# CALLBACK
# -------------------------
@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return f"""
        <h2>❌ No code received</h2>
        <p>URL: {request.url}</p>
        <p>Make sure you start from /login</p>
        """

    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    ).decode()

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    token_headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    r = requests.post(TOKEN_URL, data=token_data, headers=token_headers)
    token_json = r.json()

    if "access_token" not in token_json:
        return f"Token error: {token_json}"

    session["access_token"] = token_json["access_token"]

    return redirect("/")


# -------------------------
# CURRENTLY PLAYING
# -------------------------
@app.route("/current")
def current():

    if "access_token" not in session:
        return redirect("/")

    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    res = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers=headers
    )

    if res.status_code == 204:
        return """
        <h2>🎧 Nothing is playing</h2>
        <a href="/"><button>Home</button></a>
        """

    if res.status_code == 401:
        return f"401 - Missing permissions (check scope)"

    try:
        data = res.json()
        item = data.get("item")

        if not item:
            return "No track data"

        song = item["name"]
        artist = item["artists"][0]["name"]

        return f"""
        <h2>🎧 Now Playing</h2>
        <h3>{song} - {artist}</h3>
        <br>
        <a href="/"><button>Back</button></a>
        <a href="/logout"><button>Logout</button></a>
        """

    except:
        return "Error reading Spotify response"


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)