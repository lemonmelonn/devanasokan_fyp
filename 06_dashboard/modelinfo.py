# modelinfo.py
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# Outline Card
def outline_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4("Outline", className="card-title mb-3"),
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
                html.H4("Model Info", className="card-title mb-3"),
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
                html.H4("Data Preparation", className="card-title mb-3"),
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
                html.H4("Model Performance", className="card-title mb-3"),
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
                html.Div(
                    [
                        html.Div(
                            html.Img(
                                src="/assets/roc-auc.png",
                                alt="ROC-AUC curve",
                                className="performance-plot-img",
                            ),
                            className="performance-plot-item",
                        ),
                        html.Div(
                            html.Img(
                                src="/assets/confusionmatrix.png",
                                alt="Confusion matrix",
                                className="performance-plot-img",
                            ),
                            className="performance-plot-item",
                        ),
                    ],
                    className="mt-3 performance-plot-row",
                ),
            ]
        ),
        className="dashboard-card shadow-sm border-0 mb-4",
    )