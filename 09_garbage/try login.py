import os
import base64
import urllib.parse
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = "dev_secret_key"  # needed for session

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


# -------------------------
# HOME PAGE (UI)
# -------------------------
@app.route("/")
def home():
    if "access_token" in session:
        return """
        <h2>Logged in 🎧</h2>
        <a href="/recent"><button>View Recently Played</button></a>
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
    scope = "user-read-recently-played user-top-read"

    auth_query = (
        f"{AUTH_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&scope={urllib.parse.quote(scope)}"
        f"&redirect_uri={REDIRECT_URI}"
    )

    return redirect(auth_query)


# -------------------------
# CALLBACK
# -------------------------
@app.route("/callback")
def callback():
    code = request.args.get("code")

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
        return str(token_json)

    session["access_token"] = token_json["access_token"]

    return redirect(url_for("home"))


# -------------------------
# RECENTLY PLAYED PAGE
# -------------------------
@app.route("/recent")
def recent():

    if "access_token" not in session:
        return redirect("/")

    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    recent = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played",
        headers=headers
    )

    if recent.status_code != 200:
        return f"{recent.status_code} - {recent.text}"

    data = recent.json()

    songs = [
        item["track"]["name"] + " - " + item["track"]["artists"][0]["name"]
        for item in data.get("items", [])
    ]

    html = "<h2>Recently Played</h2>"
    html += "<br>".join(songs)
    html += "<br><br><a href='/logout'><button>Logout</button></a>"

    return html


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