# layouts.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import date, timedelta
# import dash_ag_grid as dag


def dashboard_menu():
    return dbc.NavbarSimple(
        brand="Song Safeness Dashboard",
        color="primary",
        dark=True,
        fluid=True,
        className="dashboard-navbar",
        children=[
            dbc.NavItem(dbc.NavLink("Song Classification", href="/currently-listening")),
            dbc.NavItem(dbc.NavLink("Manual Search", href="/manual-search")),
            dbc.NavItem(dbc.NavLink("Song History", href="/song-history")),
        ],
    )

# Currently Listening Layout
def currently_listening_card(track=None, error=None):
    if error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Currently Listening", className="section-header mb-2"),
                html.P("Unable to load the current track right now.", className="section-body mb-1")
                # html.Small(str(error), className="text-muted")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    if not track:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Currently Listening", className="section-header mb-2"),
                html.P("No song is currently playing.", className="section-body mb-0")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    explicit_badge = dbc.Badge(
        "Explicit",
        color="danger",
        className="ms-2"
    ) if track.get("explicit") else dbc.Badge(
        "Not Explicit",
        color="success",
        className="ms-2"
    )

    album_image = track.get("album_image")

    cover = html.Img(
        src=album_image,
        alt=f"{track.get('album', 'Album cover')} cover",
        className="dashboard-cover"
    ) if album_image else html.Div(
        "No cover",
        className="dashboard-cover dashboard-cover--placeholder d-flex align-items-center justify-content-center"
    )

    return dbc.Card(
        dbc.CardBody(
            html.Div(
                [
                    cover,
                    html.Div(
                        [
                            html.H4("Currently Listening", className="section-header mb-1"),
                            html.Div(
                                [
                                    html.Span(track.get("title", "Unknown track"), className="track-title"),
                                    explicit_badge,
                                ],
                                className="d-flex align-items-center flex-wrap",
                            ),
                            html.P(track.get("artist", "Unknown artist"), className="section-body mb-1"),
                            html.Small(
                                f"Album: {track.get('album', 'Unknown album')}",
                                className="section-meta"
                            ),
                        ],
                        className="flex-grow-1"
                    ),
                ],
                className="d-flex align-items-center gap-3 flex-wrap"
            )
        ),
        className="dashboard-card shadow-sm border-0"
    )

# Card for displaying the song label
def song_label_card(label=None, error=None):
    if error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Label", className="section-header mb-2"),
                html.P("Unable to determine the song label right now.", className="section-body mb-1"),
                html.Small(str(error), className="section-meta")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    if not label:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Label", className="section-header mb-2"),
                html.P("No label has been determined for the current song.", className="section-body mb-0")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    return dbc.Card(
        dbc.CardBody([
            html.Div(
                [
                    html.H4("Song Label", className="section-header mb-1"),
                    html.P(label, className="label-value mb-0"),
                ]
            )
        ]),
        className="dashboard-card shadow-sm border-0"
    )


def verse_label_table(verse_info=None, error=None):
    if error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Verses", className="section-header mb-2"),
                html.P("Unable to load the verses for this song right now.", className="section-body mb-1"),
                html.Small(str(error), className="section-meta")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    if verse_info is None or len(verse_info) == 0:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Verses", className="section-header mb-2"),
                html.P("No verses are available for this song yet.", className="section-body mb-0")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    display_columns = ["ori_verse", "label", "score"]
    table_data = verse_info.copy()

    for column in display_columns:
        if column not in table_data.columns:
            table_data[column] = ""

    table_data = table_data[display_columns].fillna("")

    table = html.Div(
        dash_table.DataTable(
            columns=[
                {"name": "Verse", "id": "ori_verse"},
                {"name": "Label", "id": "label"},
                {"name": "Confidence", "id": "score"},
            ],
            data=table_data.to_dict("records"),
            fixed_rows={"headers": True},
        ),
        className="dashboard-table",
    )

    return dbc.Card(
        dbc.CardBody([
            html.H4("Song Verses", className="section-header mb-3"),
            table,
        ]),
        className="dashboard-card shadow-sm border-0"
    )

def currently_listening():
    return html.Div([
        html.H1("Currently Listening", className="page-title mb-4"),
        html.P("This page shows the currently playing song and related information.", className="page-subtitle"),
        html.Div(
            id="currently-listening-content",
            children=currently_listening_card(),
            className="content-stack mt-4"
        ),
        html.Div(
            [
                dbc.Button("Refresh", id="get-current-song", color="primary", className="dashboard-button"),
                dbc.Button("Get Report", id="predict-button", color="primary", className="dashboard-button"),
            ],
            className="button-row mt-2"
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="song-label-output",
                        children=song_label_card(),
                    ),
                    md=4,
                ),
                dbc.Col(
                    html.Div(
                        id="verse-table-output",
                        children=verse_label_table(),
                    ),
                    md=8,
                ),
            ],
            className="mt-4 g-3",
        ),
    ], className="dashboard-page")

# Manual Search Layout
def manual_search():
    return html.Div([
        html.H1("Graphs?", className="page-title mb-4"),
        html.P("This page will allow users to perform manual searches.", className="page-subtitle")
    ], className="dashboard-page")

# History Layout
def song_history():
    return html.Div([
        html.H1("Song History", className="page-title mb-4"),
        html.P("This page will display the history of songs played.", className="page-subtitle")
    ], className="dashboard-page")


def create_app_layout():
    return dmc.MantineProvider(
        theme={"colorScheme": "dark"},
        children=[
            dcc.Location(id="url", refresh=False),
            dashboard_menu(),
            html.Div(id="page-container", className="dashboard-container")
        ]
    )