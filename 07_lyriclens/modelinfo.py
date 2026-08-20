# modelinfo.py

from dash import html
import dash_bootstrap_components as dbc


SURFACE_STYLE = {
    "backgroundColor": "#18181b",
    "border": "1px solid rgba(255, 255, 255, 0.08)",
    "borderRadius": "12px",
    "boxShadow": "0 10px 25px rgba(15, 23, 42, 0.25)",
}

CARD_TITLE_STYLE = {
    "color": "#60a5fa",
    "fontSize": "1.05rem",
    "fontWeight": 700,
    "marginBottom": "0.75rem",
}

BODY_TEXT_STYLE = {
    "color": "#cbd5e1",
    "lineHeight": "1.65",
    "marginBottom": "0",
}


def _spec_list(items):
    return html.Ul(
        [html.Li(item, style={"marginBottom": "0.45rem"}) for item in items],
        style={"color": "#cbd5e1", "paddingLeft": "1.1rem", "marginBottom": "0"},
    )


def outline_card():
    summary = html.P(
        "Fine-tuned BERT (bert-base-uncased) sequence classification model trained for verse-level lyrical safety classification.",
        style=BODY_TEXT_STYLE,
        className="mb-4",
    )

    left_col = dbc.Card(
        dbc.CardBody(
            [
                html.H4("Architecture & Framework", style=CARD_TITLE_STYLE),
                _spec_list(
                    [
                        "Base Model: bert-base-uncased (110M Parameters)",
                        "Classification Head: BertForSequenceClassification (PyTorch)",
                        "Target Task: Verse-Level Binary Text Classification",
                        "Output Classes: SAFE (0) (Family/Child-friendly) vs UNSAFE (1) (Explicit/Adult themes)",
                    ]
                ),
            ]
        ),
        className="dashboard-card h-100 border-0",
        style=SURFACE_STYLE,
    )

    right_col = dbc.Card(
        dbc.CardBody(
            [
                html.H4("Hyperparameter Tuning - Optuna TPE Search", style=CARD_TITLE_STYLE),
                _spec_list(
                    [
                        "Learning Rate: 2e-5 (AdamW optimizer)",
                        "Batch Size: 8 (Training) / 16 (Validation)",
                        "Weight Decay: 0.01 (Regularization)",
                        "Training Configuration: 3 Epochs, Max Sequence Length 512, FP16 Automatic Mixed Precision",
                    ]
                ),
            ]
        ),
        className="dashboard-card h-100 border-0",
        style=SURFACE_STYLE,
    )

    return dbc.Card(
        dbc.CardBody(
            [
                summary,
                dbc.Row(
                    [
                        dbc.Col(left_col, xs=12, lg=6),
                        dbc.Col(right_col, xs=12, lg=6),
                    ],
                    className="g-4",
                ),
            ]
        ),
        className="dashboard-card border-0",
        style=SURFACE_STYLE,
    )


def data_prep_card():
    left_col = dbc.Card(
        dbc.CardBody(
            [
                html.H4("Data Cleaning & Normalization", style=CARD_TITLE_STYLE),
                _spec_list(
                    [
                        "Genius Structural Splitting: Regex parser segmenting songs by section markers ([Verse], [Chorus], [Bridge]).",
                        "Script Filtering: Removed non-Latin and corrupt characters.",
                        "Contraction Expansion: Replaced short forms using the contractions library (Ex: won't -> will not).",
                        "Slang & AAVE Normalization: Standardized musical slang (Ex: words ending in in' -> ing, tryna -> trying to, whatchu -> what you).",
                        "Vocable Reduction: Deduplicated repetitive adlibs and stripped noisy multi-line punctuation.",
                    ]
                ),
            ]
        ),
        className="dashboard-card h-100 border-0",
        style=SURFACE_STYLE,
    )

    right_col = dbc.Card(
        dbc.CardBody(
            [
                html.H4("Dataset Balancing & Partitioning", style=CARD_TITLE_STYLE),
                _spec_list(
                    [
                        "Corpus Scale: 34,866 clean English verses across 5,879 unique tracks.",
                        "Contextual Labeling: Ground-truth labels annotated via local LLaMA 3 zero-shot semantic safety prompts.",
                        "Class Balancing: Undersampled majority Safe class to establish an exact 50:50 balanced distribution.",
                        "Stratified Splitting: Evaluated 70:15:15 and 80:10:10 train/val/test splits with fixed seed (SEED = 42) for reproducibility.",
                        "Final Split: 80% Train, 10% Validation, 10% Test.",
                    ]
                ),
            ]
        ),
        className="dashboard-card h-100 border-0",
        style=SURFACE_STYLE,
    )

    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(left_col, xs=12, lg=6),
                    dbc.Col(right_col, xs=12, lg=6),
                ],
                className="g-4",
            )
        ),
        className="dashboard-card border-0",
        style=SURFACE_STYLE,
    )


def _kpi_card(title, value, accent):
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(title, style={"color": "#94a3b8", "marginBottom": "0.35rem", "fontWeight": 600}),
                html.H3(value, style={"color": accent, "marginBottom": "0"}),
            ]
        ),
        className="dashboard-card h-100 border-0",
        style={
            **SURFACE_STYLE,
            "borderLeft": f"4px solid {accent}",
        },
    )


def performance_card():
    metric_row = dbc.Row(
        [
            dbc.Col(_kpi_card("Accuracy", "89.25%", "#0ea5e9"), xs=12, sm=6, xl=3),
            dbc.Col(_kpi_card("Precision", "89.18%", "#0ea5e9"), xs=12, sm=6, xl=3),
            dbc.Col(_kpi_card("Recall", "89.34%", "#0ea5e9"), xs=12, sm=6, xl=3),
            dbc.Col(_kpi_card("F1-Score", "89.26%", "#0ea5e9"), xs=12, sm=6, xl=3),
        ],
        className="g-4",
    )

    diagnostics_row = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("ROC-AUC Curve", style=CARD_TITLE_STYLE),
                            html.Img(
                                src="/assets/roc-auc.png",
                                alt="ROC-AUC Curve",
                                style={"width": "100%", "height": "auto", "display": "block"},
                            ),
                        ]
                    ),
                    className="dashboard-card h-100 border-0",
                    style=SURFACE_STYLE,
                ),
                xs=12,
                lg=6,
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Confusion Matrix", style=CARD_TITLE_STYLE),
                            html.Img(
                                src="/assets/confusionmatrix.png",
                                alt="Confusion Matrix",
                                style={"width": "100%", "height": "auto", "display": "block"},
                            ),
                        ]
                    ),
                    className="dashboard-card h-100 border-0",
                    style=SURFACE_STYLE,
                ),
                xs=12,
                lg=6,
            ),
        ],
        className="g-4 mt-1",
    )

    return html.Div([metric_row, diagnostics_row])


def deployment_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4("Production Deployment & Real-Time Pipeline", style=CARD_TITLE_STYLE),
                _spec_list(
                    [
                        (
                            "Hugging Face Hub: Model weights and tokenizer hosted at"
                            " devanasokan/bert-lyrics-classifier and loaded dynamically via"
                            ' pipeline("text-classification").'
                        ),
                        (
                            "Spotify Web API Integration: Real-time track querying and"
                            " currently playing stream extraction via Spotipy."
                        ),
                        (
                            "Dynamic Lyrics Fetcher: Live lyrical retrieval via Genius API"
                            " (lyricsgenius)."
                        ),
                        (
                            "Real-Time Inference Engine: On-the-fly regex cleaning, verse"
                            " segmentation, and BERT softmax confidence scoring."
                        ),
                        # Clickable GitHub Link
                        html.Span([
                            "Link to GitHub Repository: ",
                            html.A(
                                "lemonmelonn/devanasokan_fyp",
                                href="https://github.com/lemonmelonn/devanasokan_fyp",
                                target="_blank",
                                style={
                                    "color": "#38bdf8",
                                    "textDecoration": "underline",
                                    "wordBreak": "break-all",
                                },
                            ),
                        ]),
                        # Clickable Hugging Face Link
                        html.Span([
                            "Link to Hugging Face Model Hub: ",
                            html.A(
                                "devanasokan/bert-lyrics-classifier",
                                href=(
                                    "https://huggingface.co/devanasokan/bert-lyrics-classifier"
                                ),
                                target="_blank",
                                style={
                                    "color": "#38bdf8",
                                    "textDecoration": "underline",
                                    "wordBreak": "break-all",
                                },
                            ),
                        ]),
                    ]
                ),
            ]
        ),
        className="dashboard-card border-0",
        style=SURFACE_STYLE,
    )


layout = dbc.Container(
    [
        html.H2("Model Architecture & Outline", className="section-header mb-3"),
        outline_card(),
        html.Div(style={"height": "1.5rem"}),
        html.H2("Data Engineering & Preprocessing", className="section-header mb-3"),
        data_prep_card(),
        html.Div(style={"height": "1.5rem"}),
        html.H2("Model Performance & Evaluation", className="section-header mb-3"),
        performance_card(),
        html.Div(style={"height": "1.5rem"}),
        html.H2("Production Deployment & Real-Time Pipeline", className="section-header mb-3"),
        deployment_card(),
    ],
    fluid=True,
    style={
        "backgroundColor": "#09090b",
        "color": "#f8fafc",
        "padding": "2rem 1.5rem 4rem",
        "minHeight": "100vh",
    },
)