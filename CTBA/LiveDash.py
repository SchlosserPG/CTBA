from dash import Dash, html
import pandas as pd

# Create Dash instance
app = Dash(__name__)
server = app.server  # expose the Flask server for gunicorn

# Layout
app.layout = html.Div([
    html.H1("Hello, CTBA with Gunicorn"),
    html.P("This app runs locally and in production!")
])

if __name__ == "__main__":
    # Local run
    app.run_server(debug=True)
