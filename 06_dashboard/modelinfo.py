# modelinfo.py
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# Outline Card
def outline_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    """
                    This model classifies song lyrics into Appropriate and
                    Inappropriate categories using a fine-tuned DistilBERT model.
                    """,
                    className="mb-2",
                ),
                html.Ul(
                    [
                        html.Li("Architecture: DistilBERT"),
                        html.Li("Framework: PyTorch"),
                        html.Li("Classes: Appropriate / Inappropriate"),
                    ]
                ),
            ]
        ),
        className="dashboard-card shadow-sm border-0 mt-4 mb-4",
    )

# Model Info Card
def model_info_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    """
                    This model classifies song lyrics into Appropriate and
                    Inappropriate categories using a fine-tuned DistilBERT model.
                    """,
                    className="mb-2",
                ),
                html.Ul(
                    [
                        html.Li("Learning Rate: 2e-5"),
                        html.Li("Training Batch Size: 16"),
                        html.Li("Weight Decay: 0.01"),
                    ]
                ),
            ]
        ),
        className="dashboard-card shadow-sm border-0 mt-4 mb-4",
    )


# Data Preparation Card
def data_preparation_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    """
                    The dataset was preprocessed to clean and tokenize the lyrics.
                    """,
                    className="mb-2",
                ),
                html.Ul(
                    [
                        html.Li("Tokenization: DistilBERT Tokenizer"),
                        html.Li("Cleaning: Lowercasing, removing special characters"),
                        html.Li("Splitting: Train/Test/Validation sets"),
                    ]
                ),
            ]
        ),
        className="dashboard-card shadow-sm border-0 mb-4",
    )


# Performance Card
def performance_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(
                    """
                    The model's performance is evaluated using standard metrics.
                    """,
                    className="mb-2",
                ),
                html.Ul(
                    [
                        html.Li("Accuracy: 89.07%"),
                        html.Li("Precision: 88.87%"),
                        html.Li("Recall: 89.34%"),
                        html.Li("F1 Score: 89.10%"),
                    ]
                ),
            ]
        ),
        className="dashboard-card shadow-sm border-0 mb-4",
    )

layout = dbc.Container(
    [
        html.H2("Outline", className="section-header mb-3"),
        outline_card(),
        html.Div(style={"height": "1.5rem"}),
        model_info_card(),

        html.Div(style={"height": "1.5rem"}),
        html.H2("Data Preparation", className="section-header mb-3"),
        data_preparation_card(),

        
        html.Div(style={"height": "1.5rem"}),
        html.H2("Model Performance", className="section-header mb-3"),
        performance_card(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("ROC-AUC Curve", style={"fontSize": "1.1rem", "fontWeight": 600}),
                                html.Img(src="/assets/roc-auc.png", style={"width": "100%", "height": "auto", "marginBottom": "1rem"}),
                            ]
                        ),
                        style={
                            "backgroundColor": "#18181b",
                            "border": "1px solid rgba(255,255,255,0.08)",
                            "borderRadius": "12px",
                            "boxShadow": "0 10px 25px rgba(15, 23, 42, 0.25)",
                            "height": "100%",
                        },
                    ),
                    width=12,
                    lg=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Confusion Matrix", style={"fontSize": "1.1rem", "fontWeight": 600}),
                                html.Img(src="/assets/confusionmatrix.png", style={"width": "100%", "height": "auto", "marginBottom": "1rem"}),
                            ]
                        ),
                        style={
                            "backgroundColor": "#18181b",
                            "border": "1px solid rgba(255,255,255,0.08)",
                            "borderRadius": "12px",
                            "boxShadow": "0 10px 25px rgba(15, 23, 42, 0.25)",
                            "height": "100%",
                        },
                    ),
                    width=12,
                    lg=6,
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