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
                html.P("Unable to load the current track right now.", className="mb-1")
                # html.Small(str(error), className="text-muted")
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
        "Not Explicit",
        color="success",
        className="ms-2"
    )

    album_image = track.get("album_image")

    cover = html.Img(
        src=album_image,
        alt=f"{track.get('album', 'Album cover')} cover",
        className="border"
    ) if album_image else html.Div(
        "No cover",
        className="d-flex align-items-center justify-content-center text-muted bg-white border",
        style={
            "width": "96px",
            "height": "96px",
            "borderRadius": "14px"
        }
    )

    if album_image:
        cover.style = {
            "width": "96px",
            "height": "96px",
            "objectFit": "cover",
            "borderRadius": "14px"
        }

    return dbc.Card(
        dbc.CardBody(
            html.Div(
                [
                    cover,
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
                        ],
                        className="flex-grow-1"
                    ),
                ],
                className="d-flex align-items-center gap-3 flex-wrap"
            )
        ),
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


def verse_label_table(verse_info=None, error=None):
    if error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Verses", className="mb-2"),
                html.P("Unable to load the verses for this song right now.", className="mb-1"),
                html.Small(str(error), className="text-muted")
            ]),
            className="shadow-sm border-0",
            style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
        )

    if verse_info is None or len(verse_info) == 0:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Verses", className="mb-2"),
                html.P("No verses are available for this song yet.", className="mb-0")
            ]),
            className="shadow-sm border-0",
            style={"borderRadius": "16px", "backgroundColor": "#f8f9fa"}
        )

    display_columns = ["ori_verse", "label", "score"]
    table_data = verse_info.copy()

    for column in display_columns:
        if column not in table_data.columns:
            table_data[column] = ""

    table_data = table_data[display_columns].fillna("")

    table = dash_table.DataTable(
        columns=[
            {"name": "Verse", "id": "ori_verse"},
            {"name": "Label", "id": "label"},
            {"name": "Confidence", "id": "score"},
        ],
        data=table_data.to_dict("records"),
        style_table={
            "overflowX": "auto",
            "maxHeight": "420px",
            "overflowY": "auto",
        },
        style_header={
            "backgroundColor": "#e9ecef",
            "fontWeight": "600",
            "border": "none",
        },
        style_cell={
            "textAlign": "left",
            "whiteSpace": "pre-line",
            "height": "auto",
            "padding": "12px",
            "backgroundColor": "#f8f9fa",
            "border": "none",
            "fontSize": "14px",
            "overflowWrap": "anywhere",
        },
        style_data_conditional=[
            {
                "if": {"column_id": "label"},
                "fontWeight": "600",
                "width": "120px",
            },
            {
                "if": {"column_id": "score"},
                "width": "110px",
            },
            {
                "if": {"column_id": "ori_verse"},
                "width": "auto",
            },
        ],
        fixed_rows={"headers": True},
    )

    return dbc.Card(
        dbc.CardBody([
            html.H4("Song Verses", className="mb-3"),
            table,
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
        dbc.Button("Refresh", id="get-current-song", color="primary", className="mt-2"),
        dbc.Button("Get Report", id="predict-button", color="primary", className="mt-2"),
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