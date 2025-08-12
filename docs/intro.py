# docs/index.py  — Landing page (root path)
import dash
from dash import Dash, html, dcc

WM_GREEN = "#115740"
WM_GOLD = "#B9975B"

app = Dash(__name__)
server = app.server  # Required for Gunicorn in production



dash.register_page(
    __name__,
    path="/",                 
    name="Introduction to CTBA",
    order=0
)

layout = html.Div(
    [
        # Hero section
        html.Div(
            [
                html.H1("Welcome to CTBA", className="hero-title"),
                html.P(
                    "Explore interactive dashboards and course materials built with Dash Pages.",
                    className="hero-subtitle"
                ),
                html.Div(
                    [
                    ],
                    className="hero-actions"
                ),
            ],
            className="hero"
        ),

        # Quick features
        html.Div(
            [
                html.H2("What you’ll find"),
                html.Ul(
                    [
                        html.Li("Book-style navigation powered by Dash Pages"),
                        html.Li("Consistent layout and William & Mary styling"),
                        html.Li("Interactive figures and data exploration"),
                    ]
                ),
            ],
            className="content-section"
        ),
    ],
    className="page"
)
