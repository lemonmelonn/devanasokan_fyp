import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


def stat_card(value, label, accent="#10b981"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    value,
                    style={
                        "fontSize": "2rem",
                        "fontWeight": 700,
                        "color": "#0ea5e9",
                        "lineHeight": 1.2,
                    },
                ),
                html.Div(
                    label,
                    style={
                        "fontSize": "0.82rem",
                        "color": "#94a3b8",
                        "marginTop": "8px",
                        "letterSpacing": "0.02em",
                    },
                ),
            ],
            style={
                "padding": "1.2rem 1.1rem",
                "backgroundColor": "#18181b",
                "border": "1px solid rgba(255,255,255,0.08)",
                "borderRadius": "12px",
                "boxShadow": "0 10px 25px rgba(15, 23, 42, 0.25)",
            },
        ),
        className="h-100 border-0",
    )

# Home Info Layout
layout = dbc.Container(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "Implementing A Machine Learning Based Approach For Classifying Song Lyrics Appropriateness For Children",
                                    style={
                                        "fontSize": "2.5rem",
                                        "fontWeight": 700,
                                        "lineHeight": 1.15,
                                        "marginBottom": "0.75rem",
                                        "letterSpacing": "-0.02em",
                                    },
                                ),
                                html.Div(
                                    "Devan Asokan | TP070977 | APU2601CS(DA) | Final Year Project",
                                    style={
                                        "fontSize": "0.95rem",
                                        "fontWeight": 600,
                                        "color": "#10b981",
                                        "marginBottom": "1rem",
                                        "letterSpacing": "0.04em",
                                        "textTransform": "uppercase",
                                    },
                                ),
                                html.P(
                                    "This project applies deep learning and transformer-based NLP (BERT) to evaluate song lyrics appropriateness for children, enabling safer listening experiences through contextual verse-level moderation.",
                                    style={
                                        "fontSize": "1.05rem",
                                        "lineHeight": 1.7,
                                        "color": "#cbd5e1",
                                        "maxWidth": "820px",
                                        "marginBottom": "1.5rem",
                                    },
                                ),
                                html.Div(
                                    [
                                        dbc.Badge("Text Classification", color="success", className="me-2 mb-2"),
                                        dbc.Badge("NLP", color="primary", className="me-2 mb-2"),
                                        dbc.Badge("Lyrical Analysis", color="warning", className="me-2 mb-2"),
                                        dbc.Badge("Content Moderation", color="info", className="me-2 mb-2"),
                                        dbc.Badge("SDG 3: Good Health and Well-being", color="secondary", className="me-2 mb-2"),
                                    ]
                                ),
                            ],
                            style={"paddingRight": "1rem"},
                        ),
                    ],
                    style={"flex": 1},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                "System Overview",
                                style={
                                    "fontSize": "0.78rem",
                                    "fontWeight": 600,
                                    "color": "#0ea5e9",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "0.08em",
                                    "marginBottom": "0.9rem",
                                },
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div("Model Layer", style={"color": "#94a3b8", "fontSize": "0.85rem"}),
                                            html.Div("BERT", style={"fontSize": "1.1rem", "fontWeight": 600}),
                                        ],
                                        style={"marginBottom": "1rem"},
                                    ),
                                    html.Div(
                                        [
                                            html.Div("Prediction Scope", style={"color": "#94a3b8", "fontSize": "0.85rem"}),
                                            html.Div("Verse-level Labeling", style={"fontSize": "1.1rem", "fontWeight": 600}),
                                        ],
                                        style={"marginBottom": "1rem"},
                                    ),
                                    html.Div(
                                        [
                                            html.Div("Action", style={"color": "#94a3b8", "fontSize": "0.85rem"}),
                                            html.Div("Risk-aware Child Safety Filter", style={"fontSize": "1.1rem", "fontWeight": 600}),
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    ),
                    style={
                        "backgroundColor": "#18181b",
                        "border": "1px solid rgba(255,255,255,0.08)",
                        "borderRadius": "12px",
                        "boxShadow": "0 10px 25px rgba(15, 23, 42, 0.25)",
                        "minWidth": "260px",
                        "maxWidth": "300px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "gap": "1.5rem",
                "padding": "2rem 0",
                "flexWrap": "wrap",
            },
        ),

        # Statistics Section
        dbc.Row(
            [
                dbc.Col(stat_card("2.5 hours/day", "Average music engagement among young listeners (American Academy of Child and Adolescent Psychiatry., 2024)"), width=12, md=3),
                dbc.Col(stat_card("40%", "Percentage of top billboard hits containing sexual lyrics (Coyne, 2023)"), width=12, md=3),
                dbc.Col(stat_card("69%", "Percentage of explicit songs on the Billboard charts that are rap songs (Parris, 2023)"), width=12, md=3),
                dbc.Col(stat_card("27%", "Proportion of children under the age of 8 that are exposed to explicit content online (TxNaturalPediatrics, 2024)"), width=12, md=3),
            ],
            className="g-3 mt-2",
        ),

        # Problem and Solution Section
        html.Div(style={"height": "1.5rem"}),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2(
                                    "The Problem & Motivation",
                                    style={"fontSize": "2.0rem", "fontWeight": 700, "marginBottom": "1rem", "color": "#0ea5e9"},
                                ),
                                html.P(
                                    "Digital music consumption is rising rapidly among children and young listeners, while lyrical content is becoming increasingly explicit, violent, and psychologically mature.",
                                    style={"color": "#cbd5e1", "lineHeight": 1.75},
                                ),
                                html.P(
                                    "Traditional moderation systems rely on coarse metadata such as the binary 'Explicit' tag, which fails to capture subtle references, coded language, profanity in metaphorical contexts, and hidden adult themes embedded in individual verses.",
                                    style={"color": "#cbd5e1", "lineHeight": 1.75},
                                ),
                                html.P(
                                    "This creates a dangerous blind spot: a track may appear safe at a glance while still containing harmful language at specific moments in the song.",
                                    style={"color": "#cbd5e1", "lineHeight": 1.75},
                                ),
                            ]
                        ), className="home-card"
                    ),
                    width=12,
                    lg=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2(
                                    "The Solution & Impact",
                                    style={"fontSize": "2.0rem", "fontWeight": 700, "marginBottom": "1rem", "color": "#0ea5e9"},
                                ),
                                html.P(
                                    "This system bridges the gap between surface-level music metadata and child safety by using context-aware transformer models to classify lyrics at the verse level.",
                                    style={"color": "#cbd5e1", "lineHeight": 1.75},
                                ),
                                html.P(
                                    "Instead of labeling the whole track uniformly, the model evaluates the semantics and tone of individual sections to identify inappropriate language, hidden adult themes, or harmful messaging with greater precision.",
                                    style={"color": "#cbd5e1", "lineHeight": 1.75},
                                ),
                                html.P(
                                    "The result is a more responsible, transparent moderation workflow for parents, educators, streaming services, and digital content reviewers seeking safer listening environments.",
                                    style={"color": "#cbd5e1", "lineHeight": 1.75},
                                ),
                            ]
                        ), className="home-card"
                    ),
                    width=12,
                    lg=6,
                ),
            ],
            className="g-4",
        ),

        # Research Insights Section
        html.Div(style={"height": "2.5rem"}),
        html.H2(
            "Research Insights",
            style={
                "fontWeight": 700,
                "marginBottom": "1rem",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Presence of Explicit Songs across Genres on Billboard Charts", style={"fontSize": "1.1rem", "fontWeight": 600, "color": "#0ea5e9"}),
                                html.Img(src="/assets/percentageofexplicit.png", style={"width": "100%", "height": "auto", "marginBottom": "1rem"}),
                                html.P("(Source: Parris, 2023)"),
                            ]
                        ), className="home-card"
                    ),
                    width=12,
                    lg=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Percentage of Explicit Songs by Year in Billboard Top 100 Charts", style={"fontSize": "1.1rem", "fontWeight": 600, "color": "#0ea5e9"}),
                                html.Img(src="/assets/riseofexplicit.png", style={"width": "100%", "height": "auto", "marginBottom": "1rem"}),
                                html.P("(Source: Chandra et al., 2025)"),
                            ]
                        ), className="home-card"
                    ),
                    width=12,
                    lg=6,
                ),
            ],
            className="g-4 mt-1",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Trend of Use of Profanity in Song Lyrics", style={"fontSize": "1.1rem", "fontWeight": 600, "color": "#0ea5e9"}),
                                html.Img(src="/assets/profanitytrend.png", style={"width": "100%", "height": "auto", "marginBottom": "1rem"}),
                                html.P("(Source: Perera & Teh, 2025)"),
                            ]
                        ), className="home-card"
                    ),
                    width=12,
                ),
            ],
            className="g-4 mt-1",
        ),

        # Target Users Section
        html.Div(style={"height": "2.5rem"}),
        html.H2(
                "Target Users",
                style={
                    "fontWeight": 700,
                    "marginBottom": "1rem",
                },
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(
                                        "👨‍👩‍👧‍👦",
                                        style={"fontSize": "2rem", "marginBottom": "0.8rem"},
                                    ),
                                    html.H4("Parents & Guardians", style={"fontSize": "1.05rem", "fontWeight": 700, "color": "#0ea5e9"}),
                                    html.P(
                                        "Have a reliable method for evaluating whether song lyrics are appropriate for their children, without requiring manual review.",
                                        style={"color": "#cbd5e1", "lineHeight": 1.7},
                                    ),
                                ]
                            ), className="home-card"
                        ),
                        width=12,
                        md=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(
                                        "🎧",
                                        style={"fontSize": "2rem", "marginBottom": "0.8rem"},
                                    ),
                                    html.H4("Music Streaming Platforms", style={"fontSize": "1.05rem", "fontWeight": 700, "color": "#0ea5e9"}),
                                    html.P(
                                        "Improve the accuracy of explicit content labelling by detecting the context of potential inappropriate lyrics, rather than relying fully on keyword-based tagging.",
                                        style={"color": "#cbd5e1", "lineHeight": 1.7},
                                    ),
                                ]
                            ), className="home-card"
                        ),
                        width=12,
                        md=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(
                                        "📱",
                                        style={"fontSize": "2rem", "marginBottom": "0.8rem"},
                                    ),
                                    html.H4("Social Media Platforms", style={"fontSize": "1.05rem", "fontWeight": 700, "color": "#0ea5e9"}),
                                    html.P(
                                        "Detect the use of songs with inappropriate lyrics in user-generated content, where original explicit labels may not be preserved",
                                        style={"color": "#cbd5e1", "lineHeight": 1.7},
                                    ),
                                ]
                            ), className="home-card"
                        ),
                        width=12,
                        md=4,
                    ),
                ],
                className="g-4 mt-1",
        ),

    ],
    fluid=True,
    style={
        "backgroundColor": "#09090b",
        "color": "#f8fafc",
        "padding": "2rem 1.5rem 4rem",
        "minHeight": "100vh",
    },
)