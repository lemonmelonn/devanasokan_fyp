# layouts.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import date, timedelta
# import dash_ag_grid as dag


def dashboard_menu():
    return dbc.NavbarSimple(
        brand="Dashboard",
        color="primary",
        dark=True,
        fluid=True,
        children=[
            dbc.NavItem(dbc.NavLink("Currently Listening", href="/currently-listening")),
            dbc.NavItem(dbc.NavLink("Manual Search", href="/manual-search")),
            dbc.NavItem(dbc.NavLink("Song History", href="/song-history")),
        ],
    )

# Currently Listening Layout
def currently_listening():
    return html.Div([
        html.H1("Currently Listening", className="mb-4"),
        html.P("This page will show the currently playing song and related information."),

        # Load model from 05_model_training and display predictions here
        dbc.Button("Refresh", id="get-model-output", color="primary", className="mt-3"),
    ])

# Manual Search Layout
def manual_search():
    return html.Div([
        html.H1("Manual Search", className="mb-4"),
        html.P("This page will allow users to perform manual searches.")
    ])

# History Layout
def song_history():
    return html.Div([
        html.H1("Song History", className="mb-4"),
        html.P("This page will display the history of songs played.")
    ])


def create_app_layout():
    return dmc.MantineProvider(
        theme={"colorScheme": "light"},
        children=[
            dcc.Location(id="url", refresh=False),
            dashboard_menu(),
            html.Div(id="page-container")
        ]
    )