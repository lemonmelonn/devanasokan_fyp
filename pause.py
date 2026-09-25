import base64
import hashlib
import os
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs

from dotenv import load_dotenv
import requests


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()  # Load environment variables from .env file
CLIENT_ID = os.getenv("CLIENT_ID")  # Ensure CLIENT_ID is set in the environment
if not CLIENT_ID:
    raise ValueError("CLIENT_ID is not set in the environment")

REDIRECT_URI = "http://127.0.0.1:5000/callback"

SCOPES = "user-read-playback-state user-modify-playback-state"


# ============================================================
# PKCE HELPERS
# ============================================================

def generate_code_verifier():
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier):
    digest = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


# ============================================================
# CALLBACK SERVER
# ============================================================

class CallbackHandler(BaseHTTPRequestHandler):

    authorization_code = None

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)

        if "code" in query:
            CallbackHandler.authorization_code = query["code"][0]

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.wfile.write(
                b"""
                <html>
                    <body>
                        <h2>Spotify authorization successful.</h2>
                        <p>You can close this browser window.</p>
                    </body>
                </html>
                """
            )

        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        # Hide HTTP server logs
        pass


# ============================================================
# MAIN
# ============================================================

def main():

    # Generate PKCE values
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    # Build Spotify authorization URL
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }

    auth_url = (
        "https://accounts.spotify.com/authorize?"
        + urlencode(auth_params)
    )

    print("Opening Spotify authorization page...")
    webbrowser.open(auth_url)

    print("\nWaiting for Spotify authorization...")

    # Start temporary local server
    server = HTTPServer(
        ("127.0.0.1", 5000),
        CallbackHandler
    )

    while CallbackHandler.authorization_code is None:
        server.handle_request()

    authorization_code = CallbackHandler.authorization_code

    print("Authorization code received.")

    # ========================================================
    # EXCHANGE CODE FOR ACCESS TOKEN
    # ========================================================

    token_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "client_id": CLIENT_ID,
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": code_verifier,
        },
        timeout=10,
    )

    if token_response.status_code != 200:
        print("\nFailed to obtain access token.")
        print(token_response.text)
        return

    access_token = token_response.json()["access_token"]

    print("Access token obtained.")

    # ========================================================
    # CHECK CURRENT PLAYBACK
    # ========================================================

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    playback_response = requests.get(
        "https://api.spotify.com/v1/me/player",
        headers=headers,
        timeout=10,
    )

    if playback_response.status_code == 204:
        print("\nNo active Spotify playback device.")
        return

    if playback_response.status_code != 200:
        print("\nFailed to get playback state.")
        print(playback_response.text)
        return

    playback = playback_response.json()

    device = playback.get("device")
    item = playback.get("item")

    if item:
        track_name = item.get("name", "Unknown")
        artists = ", ".join(
            artist["name"]
            for artist in item.get("artists", [])
        )

        print(f"\nCurrently playing:")
        print(f"  {track_name} - {artists}")

    if device:
        print(f"  Device: {device.get('name')}")
        print(f"  Device ID: {device.get('id')}")

    print(f"  Playing: {playback.get('is_playing')}")

    # ========================================================
    # PAUSE PLAYBACK
    # ========================================================

    if not playback.get("is_playing"):
        print("\nNothing is currently playing.")
        return

    pause_response = requests.put(
        "https://api.spotify.com/v1/me/player/pause",
        headers=headers,
        timeout=10,
    )

    if pause_response.status_code == 204:
        print("\nSUCCESS: Spotify playback paused.")

    else:
        print("\nFailed to pause playback.")
        print(f"Status code: {pause_response.status_code}")
        print(pause_response.text)


if __name__ == "__main__":
    main()