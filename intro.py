# LiveDash.py
from dash import Dash, dcc, html
from electricity import electricity_layout, register_callbacks

app = Dash(__name__, suppress_callback_exceptions=True, title="LiveDash")
server = app.server  # Render/Gunicorn entry

WM_GREEN = "#115740"
WM_GOLD = "#B9975B"

home_layout = html.Div(
    [
        html.H1("Live Dashboard", style={"color": WM_GREEN}),
        html.P("Welcome! Use the nav to switch pages (single Render app, multiple pages)."),
    ]
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        html.Nav(
            [
                dcc.Link("Home", href="/", style={"marginRight": 16, "color": WM_GREEN, "textDecoration": "none", "fontWeight": 600}),
                dcc.Link("Home", href="/goingLive", style={"marginRight": 16, "color": WM_GREEN, "textDecoration": "none", "fontWeight": 600}),
                dcc.Link("Electricity", href="/electricity", style={"color": WM_GREEN, "textDecoration": "none", "fontWeight": 600}),
            ],
            style={"padding": "12px 0", "borderBottom": f"3px solid {WM_GOLD}", "marginBottom": 16},
        ),
        html.Div(id="page-content", style={"maxWidth": 900}),
    ],
    style={"maxWidth": 960, "margin": "0 auto", "fontFamily": "Arial, sans-serif"},
)

@app.callback(dcc.Output("page-content", "children"), dcc.Input("url", "pathname"))
def render_page(pathname):
    if pathname in ("/", ""):
        return home_layout
    if pathname == "/electricity":
        return electricity_layout
    return html.Div([html.H2("404 — Page not found"), dcc.Link("Go Home", href="/")])

# register the electricity callbacks with this app
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
