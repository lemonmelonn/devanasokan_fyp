# callbacks.py
import logging
import pickle
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

from layouts import currently_listening, manual_search, song_history

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

logger = logging.getLogger(__name__)

def register_callbacks(app):
    
    @app.callback(
        Output("page-container", "children"),
        Input("url", "href")
    )
    def display_page(href):
        parsed = urlparse(href)
        pathname = parsed.path

        if pathname == "/":
            return currently_listening()

        if pathname == "/song-history":
            return song_history()
        
        if pathname == "/currently-listening":
            return currently_listening()

        if pathname == "/manual-search":
            return manual_search()
        
        return html.Div("404: Page not found", style={"padding": "2rem"})

    @app.callback(
        Output("currently-listening-content", "children"),
        Input("get-model-output", "n_clicks")
    )
    def get_model_output(n):
        # Load the model and make predictions here
        from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

        # Load the model and tokenizer from your local folder
        path = "./05_model_training/my_final_model"
        model = AutoModelForSequenceClassification.from_pretrained(path)
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased") # Ensure you saved the tokenizer there too!

        # Create a 'pipeline' (the easiest way to use the model)
        classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

        result = classifier("good morning")
        print(result)

        # For demonstration, we'll just return a placeholder
        print("Button clicked, fetching model output...")
        return html.Div([
            html.H3("Currently Playing Song"),
            html.P("Artist: Placeholder Artist"),
            html.P("Song: Placeholder Song"),
            html.P("Predicted Genre: Placeholder Genre")
        ])