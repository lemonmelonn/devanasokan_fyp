import logging

from dash import Dash
import dash_bootstrap_components as dbc

from layouts import create_app_layout
from callbacks import register_callbacks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
        "https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap",
        "https://cdn.jsdelivr.net/npm/ag-grid-community@30/styles/ag-grid.css",
        "https://cdn.jsdelivr.net/npm/ag-grid-community@30/styles/ag-theme-alpine.css",
    ],
)

server = app.server
app.layout = create_app_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
