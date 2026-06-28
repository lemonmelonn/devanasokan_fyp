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
def currently_listening_card(track=None, error=None):
    if error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Currently Listening", className="mb-2"),
                html.P("Unable to load the current track right now.", className="mb-1"),
                html.Small(str(error), className="text-muted")
            ]),
            className="shadow-sm border-0",
            style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
        )

    if not track:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Currently Listening", className="mb-2"),
                html.P("No song is currently playing.", className="mb-0")
            ]),
            className="shadow-sm border-0",
            style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
        )

    explicit_badge = dbc.Badge(
        "Explicit",
        color="danger",
        className="ms-2"
    ) if track.get("explicit") else dbc.Badge(
        "Clean",
        color="success",
        className="ms-2"
    )

    return dbc.Card(
        dbc.CardBody([
            html.Div(
                [
                    html.H4("Currently Listening", className="mb-1"),
                    html.Div(
                        [
                            html.Span(track.get("title", "Unknown track"), className="fw-semibold fs-5"),
                            explicit_badge,
                        ],
                        className="d-flex align-items-center flex-wrap",
                    ),
                    html.P(track.get("artist", "Unknown artist"), className="text-muted mb-1"),
                    html.Small(
                        f"Album: {track.get('album', 'Unknown album')}",
                        className="text-muted"
                    ),
                ]
            )
        ]),
        className="shadow-sm border-0",
        style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
    )

# Card for displaying the song label
def song_label_card(label=None, error=None):
    if error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Label", className="mb-2"),
                html.P("Unable to determine the song label right now.", className="mb-1"),
                html.Small(str(error), className="text-muted")
            ]),
            className="shadow-sm border-0",
            style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
        )

    if not label:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Label", className="mb-2"),
                html.P("No label has been determined for the current song.", className="mb-0")
            ]),
            className="shadow-sm border-0",
            style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
        )

    return dbc.Card(
        dbc.CardBody([
            html.Div(
                [
                    html.H4("Song Label", className="mb-1"),
                    html.P(label, className="fw-semibold fs-5 mb-0"),
                ]
            )
        ]),
        className="shadow-sm border-0",
        style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
    )

def currently_listening():
    return html.Div([
        html.H1("Currently Listening", className="mb-4"),
        html.P("This page shows the currently playing song and related information."),
        html.Div(
            id="currently-listening-content",
            children=currently_listening_card(),
            className="mt-4"
        ),
        dbc.Button("Refresh song info", id="get-current-song", color="primary", className="mt-2"),
        dbc.Button("Predict", id="predict-button", color="primary", className="mt-2"),
        html.Div(
            id="song-label-output",
            children=song_label_card(),
            className="mt-4"
        ),
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