# callbacks.py
import logging
import pickle
import re
from unittest import result
import ollama
import pandas as pd
import io  # Add this import
import os  # Add this import for environment variables
from datetime import date, datetime, timedelta
from dash import Input, Output, State, callback, callback_context, ALL, ctx, html, dcc, dash_table, dash, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from urllib.parse import urlparse, parse_qs

from layouts import song_card, song_classification_page, song_label_card, verse_label_table, model, song_history
from functions import load_model, get_song_details, detect_explicit, get_structured_lyrics, split_verses, clean_verses, get_model_output
from spotify_functions import get_access_token, get_currently_playing, search_possible_songs
from csv_functions import add_song_to_csv, check_song_exists, retrieve_song_info, retrieve_verse_info, update_song_label

logger = logging.getLogger(__name__)

# print(ALL)

# Load the classifier model and get the Spotify access token
CLASSIFIER = load_model()
TOKEN = get_access_token()

# Global variable to store the last fetched song ID
SONG_ID = None
SONG_TITLE = None
SONG_ARTIST = None
SONG_EXPLICIT = None

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
            return song_classification_page()

        if pathname == "/song-history":
            return song_history()
        
        if pathname == "/currently-listening":
            return song_classification_page()

        if pathname == "/model":
            return model()

        return html.Div("404: Page not found", className="dashboard-page")
    
    # Callback to fetch the currently playing song and update the song card
    @app.callback(
        Output("currently-listening-content", "children"),
        Input("url", "pathname"),
        Input("get-current-song", "n_clicks")
    )
    def get_current_song(pathname, n_clicks):
        if pathname not in ["/", "/currently-listening"]:
            raise PreventUpdate

        try:
            # Fetch the currently playing track from Spotify
            current_track = get_currently_playing()

            # Update global variables with song details
            global SONG_ID, SONG_TITLE, SONG_ARTIST, SONG_EXPLICIT
            SONG_ID = current_track.get("song_id")
            SONG_TITLE = current_track.get("title")
            SONG_ARTIST = current_track.get("artist")
            SONG_EXPLICIT = current_track.get("explicit")
            

            # Add method to track details
            current_track["method"] = "Currently Listening"

            # Print selected song details for debugging
            print(f"\n[DEBUG] Current song: {current_track['title']} by {current_track['artist']}")

            # Print global variables for debugging
            logger.info(f"Fetched song details: SONG_ID={SONG_ID}, SONG_TITLE={SONG_TITLE}, SONG_ARTIST={SONG_ARTIST}, SONG_EXPLICIT={SONG_EXPLICIT}\n")

        except Exception as exc:
            logger.exception("Failed to fetch currently playing track")
            return song_card(error=exc)

        return song_card(current_track)
    
    # Callback to predict the song label and update the song label card and verse label table
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
            return song_label_card(error="No song selected"), verse_label_table()

        try:
            verse_info = None

            # Use the loaded classifier to predict the song label
            exists = check_song_exists(SONG_ID)

            # If record does not exist, add song details
            if not exists:
                # Add the song to the CSV file
                add_song_to_csv(SONG_ID, SONG_TITLE, SONG_ARTIST, SONG_EXPLICIT)

                # Clean the song title to remove any text in parentheses for better lyric fetching
                cleansongtitle = re.sub(r'\s*\(.*?\)\s*', '', SONG_TITLE)  # Remove text in parentheses
                
                # Fetch structured lyrics
                full_song = get_structured_lyrics(SONG_ARTIST, cleansongtitle)
                
                # Split the lyrics into verses and clean them
                split_verses(SONG_ID, full_song)        
                text = clean_verses(SONG_ID)

                # Use the classifier to get the overall label for the song
                ovr_label = get_model_output(CLASSIFIER, SONG_ID, "verselabels.csv")

                logger.info(f"Overall label for the song: {ovr_label}")

                update_song_label(SONG_ID, ovr_label)
                
                maininfo = retrieve_song_info(SONG_ID)
                #print(maininfo)
                    
            # If record exists, retrieve and print details
            else:
                print(f"\nSong ID {SONG_ID} already exists.")
                maininfo = retrieve_song_info(SONG_ID)
                print(maininfo)

            # Retrieve verse information for the song
            verse_info = retrieve_verse_info(SONG_ID, "verselabels.csv")
            # if verse_info is not None:
            #     print(verse_info)
            # print(maininfo)
            # print(f"\n[DEBUG] Retrieved verse information for Song ID {SONG_ID}: {verse_info.shape()}")


            # Get the overall label for the song from maininfo
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
    
    # Callback to handle song search and display results
    @callback(
        Output("search-results-store", "data"),
        Output("search-results", "children"),
        Input("input-song-name", "value"),
        prevent_initial_call=True
    )
    def update_search_results(query):

        if not query or len(query.strip()) < 2:
            return [], []

        # Search for possible songs using the provided query
        songs = search_possible_songs(query)

        cards = []

        for i, song in enumerate(songs):

            cards.append(
                html.Div(
                    id={
                        "type": "song-card",
                        "index": i
                    },
                    n_clicks=0,
                    className="song-card",
                    children=[

                        # LEFT: album cover
                        html.Img(
                            src=song["album_cover"],
                            className="song-card-img"
                        ),

                        # RIGHT: details
                        html.Div(
                            className="song-card-info",
                            children=[

                                html.Div(song["title"], className="song-title"),
                                html.Div(song["artist"], className="song-artist"),
                                html.Div(song["album"], className="song-album"),
                            ]
                        )
                    ]
                )
            )

        return songs, cards
    

    # Callback to handle song selection and update the song card
    @callback(
        Output("selected-song", "data"),
        Output("manual-search-modal", "is_open", allow_duplicate=True),
        Output("currently-listening-content", "children", allow_duplicate=True),
        Output("input-song-name", "value"),
        Input({"type": "song-card", "index": ALL}, "n_clicks"),
        State("search-results-store", "data"),
        prevent_initial_call=True
    )
    def select_song(n_clicks_list, songs):

        # nothing stored yet
        if not songs:
            return no_update, no_update, no_update, no_update

        triggered = ctx.triggered_id

        # must be a real card click
        if not triggered or not isinstance(triggered, dict):
            return no_update, no_update, no_update, no_update

        if triggered.get("type") != "song-card":
            return no_update, no_update, no_update, no_update

        index = triggered["index"]

        # safety: ignore empty clicks
        if not n_clicks_list or all(v is None or v == 0 for v in n_clicks_list):
            return no_update, no_update, no_update, no_update

        selected = songs[index]

        # Update global variables with song details
        global SONG_ID, SONG_TITLE, SONG_ARTIST, SONG_EXPLICIT
        SONG_ID = selected.get("song_id")
        SONG_TITLE = selected.get("title")
        SONG_ARTIST = selected.get("artist")
        SONG_EXPLICIT = selected.get("explicit")

        # Add method to track details
        selected["method"] = "Manual Search"

        # Rename album_cover to album_image for consistency
        selected["album_image"] = selected.pop("album_cover", None)

        # Print selected song details for debugging
        print(f"\n[DEBUG] Selected song: {selected['title']} by {selected['artist']}")

        # Print global variables for debugging
        logger.info(f"Fetched song details: SONG_ID={SONG_ID}, SONG_TITLE={SONG_TITLE}, SONG_ARTIST={SONG_ARTIST}, SONG_EXPLICIT={SONG_EXPLICIT}\n")

        # Return output
        return {
            "song_id": selected["song_id"],
            "title": selected["title"],
            "artist": selected["artist"],
            "album": selected["album"],
            "album_image": selected["album_image"],
            "explicit": selected["explicit"],
            "method": selected["method"]
        }, False, song_card(selected), ""
    

    # Callback to clear info when new song is selected from modal
    @app.callback(
        Output("song-label-output", "children", allow_duplicate=True),
        Output("verse-table-output", "children", allow_duplicate=True),
        Input({"type": "song-card", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def clear_labels(n_clicks_list):
        
        return song_label_card(label=None), verse_label_table(verse_info=None)

    
    # Callback to clear info when "Current Song" button is clicked
    @app.callback(
        Output("song-label-output", "children", allow_duplicate=True),
        Output("verse-table-output", "children", allow_duplicate=True),
        Input("get-current-song", "n_clicks"),
        prevent_initial_call=True
    )
    def clear_labels(n_clicks):
        
        return song_label_card(label=None), verse_label_table(verse_info=None)