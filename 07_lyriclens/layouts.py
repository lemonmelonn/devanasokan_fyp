# layouts.py
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import projectinfo
import modelinfo
from data import INITIAL_DASHBOARD_DATA

# Layout for the dashboard
def dashboard_menu():
    return dbc.NavbarSimple(
        brand="LyricLens 🎶",
        color="primary",
        dark=True,
        fluid=True,
        sticky="top",
        className="dashboard-navbar",
        children=[
            dbc.NavItem(dbc.NavLink("Project Overview", href="/home")),
            dbc.NavItem(dbc.NavLink("Song Classification", href="/classification")),
            dbc.NavItem(dbc.NavLink("Model Info", href="/model")),
            dbc.NavItem(
                html.Div([
                    dcc.Store(id="spotify-username-store"),
                    dbc.Button(
                        html.Img(
                            src="/assets/spotify.png",
                            height="42px",
                            alt="Spotify"
                        ),
                        id="spotify-auth-btn",
                        color="link",
                        className="ms-auto",
                        style={"border": "none", "padding": "0"}
                    ),
                    dbc.Tooltip(
                        id="spotify-tooltip",
                        children="Login",
                        target="spotify-auth-btn",
                        placement="bottom"
                    )
                ])
            ),
        ],
    )

# Song Card Layout (Handles both currently listening and manual search results)
def song_card(track=None, error=None):

    method = track.get("method") if track else "Currently Listening"

    # Use placeholder image if no track is available
    cover_src = "/assets/monke.jpg"
    false_cover = html.Img(
        src=cover_src,
        alt="Album cover",
        className="dashboard-cover"
    )

    # Return a card indicating no track is available
    if not track or error:
        return dbc.Card(
            dbc.CardBody([
                html.Div(
                    [
                        false_cover,
                        html.Div(
                            [
                                html.H5(method, className="section-header mb-2", style={"marginBottom": "20px", "color": "#0ea5e9"}),
                                html.H4("No Track Available", className="section-header mb-2"),
                                html.P("Either no track is currently playing or your account is not connected", className="section-body mb-1")
                            ],
                            className="flex-grow-1"
                        ),
                    ],
                    className="d-flex align-items-center gap-3 flex-wrap"
                )
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    # Create the explicit badge based on the track's explicit status
    explicit_badge = dbc.Badge(
        "Explicit",
        color="danger",
        className="ms-2"
    ) if track.get("explicit") else dbc.Badge(
        "Not Explicit",
        color="success",
        className="ms-2"
    )

    # Display album cover
    album_image = track.get("album_image")
    cover = html.Img(
        src=album_image,
        alt=f"{track.get('album', 'Album cover')} cover",
        className="dashboard-cover"
    ) if album_image else html.Div(
        "No cover",
        className="dashboard-cover dashboard-cover--placeholder d-flex align-items-center justify-content-center"
    )

    # Return the card with track details
    return dbc.Card(
        dbc.CardBody(
            html.Div(
                [
                    cover,
                    html.Div(
                        [
                            html.H5(method, className="section-header mb-2", style={"marginBottom": "20px", "color": "#0ea5e9"}),
                            
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

    # Create a badge for the error state
    error_badge = dbc.Badge("No Label", color="#6c757d", className="ms-2", 
                            style={"fontSize": "18px", "font-weight": "bold"})

    # Return a card indicating no label is available
    if not label or error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Label", className="section-header mb-2", style={"color": "#0ea5e9"}),
                html.Br(),
                error_badge,
                html.Br(),
                html.Br(),
                html.P(
                    "SAFE: Suitable for children\nUNSAFE: Not suitable for children",
                    style={
                        "marginTop": "15px",
                        "fontSize": "12px",
                        "color": "#4F5860",
                        "whiteSpace": "pre-line",
                    },
                ),
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    # Create the explicit badge based on the track's explicit status
    label_badge = dbc.Badge(
        "UNSAFE",
        color="danger",
        className="ms-2",
        style={"fontSize": "18px", "font-weight": "bold", "text-transform": "uppercase"}
    ) if label == "UNSAFE" else dbc.Badge(
        "SAFE",
        color="success",
        className="ms-2",
        style={"fontSize": "18px", "font-weight": "bold", "text-transform": "uppercase"}
    )
    
    # Return the card with the song label
    return dbc.Card(
        dbc.CardBody([
            html.Div(
                [
                    html.H4("Song Label", className="section-header mb-1", style={"color": "#0ea5e9"}),
                    html.Br(),
                    label_badge,
                    html.Br(),
                    html.Br(),
                    html.P(
                        "SAFE: Suitable for children\nUNSAFE: Not suitable for children",
                        style={
                            "marginTop": "15px",
                            "fontSize": "12px",
                            "color": "#4F5860", # adjust colour later
                            "whiteSpace": "pre-line",
                        },
                    ),
                ]
            )
        ]),
        className="dashboard-card shadow-sm border-0"
    )

# Card for displaying the verse label table
def verse_label_table(verse_info=None, error=None):

    # Return a card indicating no verses are available
    if error:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Verses", className="section-header mb-2", style={"color": "#0ea5e9"}),
                html.P("Unable to load the verses for this song right now.", className="section-body mb-1"),
                html.Small(str(error), className="section-meta")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    # Return a card indicating no verses are available
    if verse_info is None or len(verse_info) == 0:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Verses", className="section-header mb-2", style={"color": "#0ea5e9"}),
                html.P("No verses are available for this song yet.", className="section-body mb-0")
            ]),
            className="dashboard-card shadow-sm border-0"
        )

    display_columns = ["section", "ori_verse", "label", "score"]
    table_data = verse_info.copy()

    # Clean "ori_verse" column to remove line breaks and extra spaces   
    table_data["ori_verse"] = table_data["ori_verse"].str.strip().str.replace("\n", " ")

    # Remove whitespace after brackets in the "ori_verse" column
    table_data["ori_verse"] = table_data["ori_verse"].str.replace(r'\(\s+', '(', regex=True).str.replace(r'\s+\)', ')', regex=True)

    for column in display_columns:
        if column not in table_data.columns:
            table_data[column] = ""

    table_data = table_data[display_columns].fillna("")

    header = html.Thead(
        html.Tr([
            html.Th("Section", style={"width": "15%"}),
            html.Th("Verse", style={"width": "55%"}),
            html.Th("Label", style={"width": "15%"}),
            html.Th("Confidence", style={"width": "15%"}),
        ])
    )

    body = html.Tbody([
        html.Tr(
            [
                html.Td(str(row["section"])),
                html.Td(str(row["ori_verse"])),
                html.Td(str(row["label"])),
                html.Td(str(row["score"])),
            ]
        )
        for _, row in table_data.iterrows()
    ])

    # Create the table with the header and body
    table = html.Div(
        html.Table([header, body], className="dashboard-html-table"),
        className="dashboard-table",
    )

    # Return the card with the verse table
    return dbc.Card(
        dbc.CardBody([
            html.H4("Song Verses", className="section-header mb-3", style={"color": "#0ea5e9"}),
            table,
        ]),
        className="dashboard-card shadow-sm border-0"
    )

# Song Classification Page Layout
def song_classification_page():
    return html.Div([
        html.H1("Song Classification", className="page-title mb-4"),

        # Song Info and Song Label Cards
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="currently-listening-content",
                        children=song_card(),
                        className="content-stack mt-4"
                    ),
                    md=8,
                ),
                dbc.Col(
                    html.Div(
                        id="song-label-output",
                        children=song_label_card(),
                        className="content-stack mt-4"
                    ),
                    md=4,
                ),
            ],
            className="mt-4 g-3",
        ),

        # Buttons for manual search, Currently Listening, and report generation
        html.Div(
            [
                dbc.Button("Manual Search", id="manual-search-button", color="primary", className="dashboard-button me-2"),
                dbc.Button("Currently Listening", id="get-current-song", color="primary", className="dashboard-button"),
                dbc.Button("Get Report", id="predict-button", color="primary", className="dashboard-button ms-auto"),
            ],
            className="button-row mt-2"
        ),

        html.Br(),

        html.Div(
            id="verse-table-output",
            children=verse_label_table(),
        ),
        
        dcc.Store(id="search-results-store"),
        dcc.Store(id="selected-song"),
        dcc.Store(id="song-label-store"),
        dcc.Store(id="dashboard-data-store", data=INITIAL_DASHBOARD_DATA),

        # Manual Search Modal
        dbc.Modal(
            [
                dbc.ModalHeader("Manual Search"),

                dbc.ModalBody([
                    dcc.Input(
                        id="input-song-name",
                        type="text",
                        placeholder="Search Spotify...",
                        style={"width": "100%", "height": "40px", "padding": "0 10px", "border-radius": "5px", "border": "1px solid #ccc"},
                        debounce=True,
                        className="search-input"
                    ),

                    html.Hr(),

                    html.Div(
                        "Results",
                        className="modal-section-title"
                    ),

                    html.Div(
                        id="search-results",
                        className="search-results"
                    )

                    

                ]),

                dbc.ModalFooter(
                    dbc.Button("Close", id="close-search", color="primary")
                )
            ],

            id="manual-search-modal",
            is_open=False,
            size="lg",
            centered=True,
            scrollable=True,
        )
    ], className="dashboard-page")

# Model Info Layout
def model_page():
    return html.Div([
        html.H1("Model Information", className="page-title mb-4"),
        html.Div(id="page-content", children=modelinfo.layout),
    ], className="dashboard-page")

# Home Page Layout
def home_page():
    return html.Div([
        html.H1("Project Overview", className="page-title mb-4"),
        html.Div(id="page-content", children=projectinfo.layout),
    ], className="dashboard-page")

# App Layout (used in app.py)
def create_app_layout():
    return dmc.MantineProvider(
        theme={"colorScheme": "dark"},
        children=[
            dcc.Location(id="url", refresh=True),
            dashboard_menu(),
            html.Div(id="page-container", className="dashboard-container")
        ]
    )