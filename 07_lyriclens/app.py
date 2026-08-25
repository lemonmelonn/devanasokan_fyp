# app.py

import logging
from dash import Dash
import dash_bootstrap_components as dbc
from flask import request, redirect, session
from spotify_functions import exchange_code_for_token, get_auth_url
from callbacks import register_callbacks
from layouts import create_app_layout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the Dash app with external stylesheets and suppress callback exceptions
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "https://cdn.jsdelivr.net/npm/ag-grid-community@30/styles/ag-grid.css",
        "https://cdn.jsdelivr.net/npm/ag-grid-community@30/styles/ag-theme-alpine.css",
    ],
)

# Set the server and secret key for session management
server = app.server
server.secret_key = "fyp-secret-key"  # Add a secret key for sessions

# Initialize the app layout
app.layout = create_app_layout()

# Login endpoint
@server.route("/login")
def login():
    return redirect(get_auth_url())

# Logout endpoint
@server.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# OAuth callback
@server.route("/callback")
def callback():
    code = request.args.get('code')
    if code:
        token = exchange_code_for_token(code)
        if token:
            session['spotify_token'] = token
            return redirect("/classification")
    return redirect("/")

# Register callbacks for the Dash app
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)