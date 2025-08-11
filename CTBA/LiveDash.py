from dash import Dash, html
import pandas as pd  # only if you really use it

app = Dash(__name__)
server = app.server  # expose Flask server for gunicorn

app.layout = html.Div([
    html.H1("Hello, CTBA with Gunicorn"),
    html.P("This app runs locally and in production!")
])

if __name__ == "__main__":
    app.run(debug=True)