# callbacks.py
import logging
import re
import pandas as pd
from dash import Input, Output, State, callback, ALL, ctx, dash, html, no_update
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse

from layouts import song_card, song_classification_page, song_label_card, verse_label_table, model_page, home_page
from functions import load_model_from_hf, get_structured_lyrics, split_verses, clean_verses, get_model_output
from spotify_functions import get_access_token, get_currently_playing, search_possible_songs
from data import init_dashboard_data

logger = logging.getLogger(__name__)

# print(ALL)

# Load the classifier model and get the Spotify access token
CLASSIFIER = load_model_from_hf()
TOKEN = get_access_token()

def register_callbacks(app):
    
    @app.callback(
        Output("page-container", "children"),
        Input("url", "href")
    )
    def display_page(href):
        parsed = urlparse(href)
        pathname = parsed.path

        if pathname == "/":
            print("Redirecting to /home")
            return home_page()

        if pathname == "/home":
            return home_page()
        
        if pathname == "/classification":
            return song_classification_page()

        if pathname == "/model":
            return model_page()

        return html.Div("404: Page not found", className="dashboard-page")
    
    # Callback to fetch the currently playing song and update the song card
    @app.callback(
        Output("currently-listening-content", "children"),
        Output("selected-song", "data"),
        Input("url", "pathname"),
        Input("get-current-song", "n_clicks")
    )
    def get_current_song(pathname, n_clicks):
        if pathname not in ["/", "/classification"]:
            raise PreventUpdate

        try:
            # Fetch the currently playing track from Spotify
            current_track = get_currently_playing()

            if not current_track:
                return song_card(error="No currently playing track found"), no_update

            # Add method to track details
            current_track["method"] = "Currently Listening"

            # Print selected song details for debugging
            print(f"\n[DEBUG] Current song: {current_track['title']} by {current_track['artist']}")

            logger.info(
                "Fetched Spotify song details: SONG_ID=%s, SONG_TITLE=%s, SONG_ARTIST=%s, SONG_EXPLICIT=%s",
                current_track.get("song_id"),
                current_track.get("title"),
                current_track.get("artist"),
                current_track.get("explicit"),
            )

        except Exception as exc:
            logger.exception("Failed to fetch currently playing track")
            return song_card(error=exc), no_update

        selected_song = {
            "song_id": current_track.get("song_id"),
            "title": current_track.get("title"),
            "artist": current_track.get("artist"),
            "album": current_track.get("album"),
            "album_image": current_track.get("album_image"),
            "explicit": current_track.get("explicit"),
            "method": current_track.get("method"),
        }

        return song_card(current_track), selected_song
    
    # Callback to predict the song label and update the song label card and verse label table
    @app.callback(
        Output("song-label-output", "children"),
        Output("verse-table-output", "children"),
        Output("song-label-store", "data"),
        Output("dashboard-data-store", "data"),
        Input("predict-button", "n_clicks"),
        State("selected-song", "data"),
        State("dashboard-data-store", "data"),
        prevent_initial_call=True
    )
    def predict_song_label(n_clicks, selected_song, dashboard_data):

        # Check if the predict button has been clicked
        print(f"Predict button clicked {n_clicks} times.")

        if n_clicks is None:
            raise PreventUpdate

        if not selected_song or not selected_song.get("song_id"):
            return song_label_card(error="No song selected"), verse_label_table(), None, no_update

        try:
            song_id = str(selected_song.get("song_id"))
            song_title = selected_song.get("title") or ""
            song_artist = selected_song.get("artist") or ""
            song_explicit = selected_song.get("explicit")

            dashboard_data = init_dashboard_data(dashboard_data)
            cached_song = dashboard_data["songs_by_id"].get(song_id)
            cached_verses = dashboard_data["verses_by_song_id"].get(song_id)

            if cached_song and cached_verses:
                verse_info = pd.DataFrame(cached_verses)
                if "score" in verse_info.columns:
                    verse_info["score"] = verse_info["score"].apply(
                        lambda x: f"{x * 100:.3f}%" if isinstance(x, (int, float)) else x
                    )
                song_label = cached_song.get("ovr_label")
                return song_label_card(label=song_label), verse_label_table(verse_info=verse_info), song_label, dashboard_data

            # Clean the song title to remove any text in parentheses for better lyric fetching
            cleansongtitle = re.sub(r'\s*\(.*?\)\s*', '', song_title)
                
            # Fetch structured lyrics
            full_song = get_structured_lyrics(song_artist, cleansongtitle)
            if not full_song:
                return song_label_card(error="Lyrics not found for this track"), verse_label_table(), None, no_update
                
            # Split, clean, and classify in memory.
            verse_records = split_verses(song_id, full_song)
            verse_records = clean_verses(verse_records)

            # Use the classifier to get the overall label for the song
            verse_records, ovr_label = get_model_output(CLASSIFIER, verse_records)

            logger.info(f"Overall label for the song: {ovr_label}")
            dashboard_data["songs_by_id"][song_id] = {
                "song_id": song_id,
                "title": song_title,
                "artist": song_artist,
                "explicit": song_explicit,
                "ovr_label": ovr_label,
            }
            dashboard_data["verses_by_song_id"][song_id] = verse_records

            verse_info = pd.DataFrame(verse_records)
            if "score" in verse_info.columns:
                verse_info["score"] = verse_info["score"].apply(
                    lambda x: f"{x * 100:.3f}%" if isinstance(x, (int, float)) else x
                )

        except Exception as exc:
            logger.exception("Failed to predict song label")
            return song_label_card(error=exc), verse_label_table(error=exc), None, no_update

        return song_label_card(label=ovr_label), verse_label_table(verse_info=verse_info), ovr_label, dashboard_data
    

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
        Output("selected-song", "data", allow_duplicate=True),
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

        # Add method to track details
        selected["method"] = "Manual Search"

        # Rename album_cover to album_image for consistency
        selected["album_image"] = selected.pop("album_cover", None)

        # Print selected song details for debugging
        print(f"\n[DEBUG] Selected song: {selected['title']} by {selected['artist']}")

        logger.info(
            "Fetched manual song details: SONG_ID=%s, SONG_TITLE=%s, SONG_ARTIST=%s, SONG_EXPLICIT=%s",
            selected.get("song_id"),
            selected.get("title"),
            selected.get("artist"),
            selected.get("explicit"),
        )

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
    

    # Clear label and verse display whenever the selected song changes.
    @app.callback(
        Output("song-label-output", "children", allow_duplicate=True),
        Output("verse-table-output", "children", allow_duplicate=True),
        Output("song-label-store", "data", allow_duplicate=True),
        Input("selected-song", "data"),
        State("dashboard-data-store", "data"),
        prevent_initial_call=True
    )
    def clear_labels_on_song_change(selected_song, dashboard_data):
        if not selected_song or not selected_song.get("song_id"):
            raise PreventUpdate

        dashboard_data = init_dashboard_data(dashboard_data)
        song_id = str(selected_song.get("song_id"))

        cached_song = dashboard_data["songs_by_id"].get(song_id)
        cached_verses = dashboard_data["verses_by_song_id"].get(song_id)

        if cached_song and cached_verses:
            verse_info = pd.DataFrame(cached_verses)
            if "score" in verse_info.columns:
                verse_info["score"] = verse_info["score"].apply(
                    lambda x: f"{x * 100:.3f}%" if isinstance(x, (int, float)) else x
                )

            song_label = cached_song.get("ovr_label")
            return song_label_card(label=song_label), verse_label_table(verse_info=verse_info), song_label

        return song_label_card(label=None), verse_label_table(verse_info=None), None


    # Add this callback to handle logout
    @callback(
        Output("url", "pathname"),
        Input("logout-button", "n_clicks"),
        prevent_initial_call=True
    )
    def logout(n_clicks):
        if n_clicks:
            return "/logout"
        return dash.no_update