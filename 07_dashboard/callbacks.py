# callbacks.py
import logging
import pickle
import re
from unittest import result
import pandas as pd
import io  # Add this import
import os  # Add this import for environment variables
from datetime import date, datetime, timedelta
from dash import Input, Output, State, callback, callback_context, html, dcc, dash_table, dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from urllib.parse import urlparse, parse_qs

from layouts import currently_listening, currently_listening_card, song_label_card, verse_label_table, graphs, song_history
from functions import load_model, get_song_details, detect_explicit, get_structured_lyrics, split_verses, clean_verses, get_model_output
from spotify_functions import get_access_token, get_currently_playing
from csv_functions import check_song_exists, retrieve_song_info, retrieve_verse_info, update_song_label, add_nonexplicit_song, add_explicit_song

logger = logging.getLogger(__name__)

# Load the classifier model and get the Spotify access token
CLASSIFIER = load_model()
TOKEN = get_access_token()

# Global variable to store the last fetched song ID
SONG_ID = None
SONG_TITLE = None
SONG_ARTIST = None
SONG_EXPLICIT = None
CSV_FILE = None

SONG_LABEL = None  # Global variable to store the song label

def register_callbacks(app):
    
    @app.callback(
        Output("page-container", "children"),
        Input("url", "href")
    )
    def display_page(href):
        parsed = urlparse(href)
        pathname = parsed.path

        if pathname == "/":
            print("Redirecting to /currently-listening")
            return currently_listening()

        if pathname == "/song-history":
            return song_history()
        
        if pathname == "/currently-listening":
            return currently_listening()

        if pathname == "/graphs":
            return graphs()

        return html.Div("404: Page not found", className="dashboard-page")
    
    @app.callback(
        Output("currently-listening-content", "children"),
        Input("url", "pathname"),
        Input("get-current-song", "n_clicks")
    )
    def get_current_song(pathname, n_clicks):
        if pathname not in ["/", "/currently-listening"]:
            raise PreventUpdate

        try:
            current_track = get_currently_playing()

            # Update global variables with song details
            global SONG_ID, SONG_TITLE, SONG_ARTIST, SONG_EXPLICIT, CSV_FILE
            SONG_ID = current_track.get("song_id")
            SONG_TITLE = current_track.get("title")
            SONG_ARTIST = current_track.get("artist")
            SONG_EXPLICIT = current_track.get("explicit")
            CSV_FILE = None

            if SONG_EXPLICIT is True:
                CSV_FILE = "explicit.csv"
            else:
                CSV_FILE = "nonexplicit.csv"

            # Print global variables for debugging
            logger.info(f"Fetched song details: SONG_ID={SONG_ID}, SONG_TITLE={SONG_TITLE}, SONG_ARTIST={SONG_ARTIST}, CSV_FILE={CSV_FILE}")

        except Exception as exc:
            logger.exception("Failed to fetch currently playing track")
            return currently_listening_card(error=exc)

        return currently_listening_card(current_track)
    

    @app.callback(
        Output("song-label-output", "children"),
        Output("verse-table-output", "children"),
        Input("predict-button", "n_clicks")
    )
    def predict_song_label(n_clicks):

        # Check if the predict button has been clicked
        print(f"Predict button clicked {n_clicks} times.")

        if n_clicks is None:
            raise PreventUpdate

        if SONG_ID is None:
            return html.P("No song available for prediction."), verse_label_table()

        try:
            verse_info = None

            # Use the loaded classifier to predict the song label
            exists = check_song_exists(SONG_ID, CSV_FILE)

            # Check if song exists in respective CSV file
            # If no record, add song details
            if not exists:
                if SONG_EXPLICIT is True:
                    add_explicit_song(SONG_ID, SONG_TITLE, SONG_ARTIST, CSV_FILE)
                    
                else:
                    add_nonexplicit_song(SONG_ID, SONG_TITLE, SONG_ARTIST, CSV_FILE)
                    
                # Clean the song title to remove any text in parentheses for better lyric fetching
                cleansongtitle = re.sub(r'\s*\(.*?\)\s*', '', SONG_TITLE)  # Remove text in parentheses
                
                full_song = get_structured_lyrics(SONG_ARTIST, cleansongtitle)
                
                split_verses(SONG_ID, full_song)        
                text = clean_verses(SONG_ID)

                ovr_label = get_model_output(CLASSIFIER, SONG_ID, "verselabels.csv")
                print(f"\nOverall label for the song: {ovr_label}")

                update_song_label(SONG_ID, ovr_label, CSV_FILE)
                
                maininfo = retrieve_song_info(SONG_ID, CSV_FILE)
                print(maininfo)
                    
            # If record exists, retrieve and print details
            else:
                print(f"Song ID {SONG_ID} already exists in {CSV_FILE}.")
                maininfo = retrieve_song_info(SONG_ID, CSV_FILE)
                if SONG_EXPLICIT is False:
                    print(maininfo)

            verse_info = retrieve_verse_info(SONG_ID, "verselabels.csv")
            if verse_info is not None:
                print(verse_info)
            print(maininfo)

            song_label = maininfo.get("ovr_label") if maininfo else None

        except Exception as exc:
            logger.exception("Failed to predict song label")
            return song_label_card(error=exc), verse_label_table(error=exc)

        return song_label_card(label=song_label), verse_label_table(verse_info=verse_info)
    

    # Try manual search modal callbacks
    @callback(
        Output("manual-search-modal", "is_open"),
        Input("manual-search-button", "n_clicks"),
        State("manual-search-modal", "is_open"),
        prevent_initial_call=True
    )
    def toggle_modal(n, is_open):
        return not is_open
    


    @callback(
        Output("manual-search-modal", "is_open", allow_duplicate=True),
        Input("search-song", "n_clicks"),
        State("manual-search-modal", "is_open"),
        prevent_initial_call=True
    )
    def close_modal(n, is_open):
        return False