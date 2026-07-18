# layouts.py
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import date, timedelta
# import dash_ag_grid as dag


# Layout for the dashboard
def dashboard_menu():
    return dbc.NavbarSimple(
        brand="LyricLens",
        color="primary",
        dark=True,
        fluid=True,
        className="dashboard-navbar",
        children=[
            dbc.NavItem(dbc.NavLink("Song Classification", href="/currently-listening")),
            dbc.NavItem(dbc.NavLink("Model", href="/graphs")),
            dbc.NavItem(dbc.NavLink("Song History", href="/song-history")), # Maybe not
        ],
    )

# Song Card Layout (Handles both currently listening and manual search results)
def song_card(track=None, error=None):

    method = track.get("method") if track else "Currently Listening"
    # print("Album cover:", track.get("album_image") if track else "No track data")

    # Use placeholder image if no track is available
    cover_src = "/assets/monke.jpg"
    false_cover = html.Img(
        src=cover_src,
        alt="Album cover",
        className="dashboard-cover"
    )

    if error:
        return dbc.Card(
            dbc.CardBody(
                html.Div(
                    [
                        false_cover,
                        html.Div(
                            [
                                html.H4("Something went wrong", className="section-header mb-2"),
                                html.P("Unable to load the track right now.", className="section-body mb-1")
                            ],
                            className="flex-grow-1"
                        ),
                    ],
                    className="d-flex align-items-center gap-3 flex-wrap"
                )
            ),
            className="dashboard-card shadow-sm border-0"
        )

    if not track:
        return dbc.Card(
            dbc.CardBody([
                html.Div(
                    [
                        false_cover,
                        html.Div(
                            [
                                html.H4("No Track Available", className="section-header mb-2"),
                                html.P("No song is currently playing.", className="section-body mb-1")
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
                            html.H4(method, className="section-header mb-1"),
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
                html.Small(str(error), className="section-meta"),
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

    if not label:
        return dbc.Card(
            dbc.CardBody([
                html.H4("Song Label", className="section-header mb-2"),
                html.P("No label has been determined for the current song.", className="section-body mb-0"),
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
                    html.H4("Song Label", className="section-header mb-1"),
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

    display_columns = ["section", "ori_verse", "label", "score"]
    table_data = verse_info.copy()

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

    table = html.Div(
        html.Table([header, body], className="dashboard-html-table"),
        className="dashboard-table",
    )

    # Return the card with the verse table
    return dbc.Card(
        dbc.CardBody([
            html.H4("Song Verses", className="section-header mb-3"),
            table,
        ]),
        className="dashboard-card shadow-sm border-0"
    )

# Song Classification Page Layout
def song_classification_page():
    return html.Div([
        html.H1("Song Classification", className="page-title mb-4"),
        # html.P("This page shows the currently playing song and related information.", className="page-subtitle"),

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

        html.Div(
            [
                dbc.Button("Manual Search", id="manual-search-button", color="primary", className="dashboard-button"),
                dbc.Button("Spotify", id="get-current-song", color="primary", className="dashboard-button"),
                dbc.Button("Get Report", id="predict-button", color="primary", className="dashboard-button"),
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
        dcc.Store(id="llm-explanation-store"),

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

# Graphs Layout
def graphs():
    return html.Div([
        html.H1("Model", className="page-title mb-4"),
        html.P("This page will display various graphs and visualizations.", className="page-subtitle")
    ], className="dashboard-page")

# History Layout
def song_history():
    return html.Div([
        html.H1("Song History", className="page-title mb-4"),
        html.P("This page will display the history of songs played.", className="page-subtitle")
    ], className="dashboard-page")

# App Layout
def create_app_layout():
    return dmc.MantineProvider(
        theme={"colorScheme": "dark"},
        children=[
            dcc.Location(id="url", refresh=False),
            dashboard_menu(),
            html.Div(id="page-container", className="dashboard-container")
        ]
    )