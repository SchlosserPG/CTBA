import dash

from dash import Dash, html, page_container, page_registry

app = Dash(
    __name__,
    use_pages=True,
    pages_folder="docs",  
    suppress_callback_exceptions=True,
    title="CTBA"
)
server = app.server

def toc():
    pages_sorted = sorted(
        page_registry.values(),
        key=lambda p: (p.get("order", 10_000), p["path"])
    )
    return html.Nav(
        [
            html.A(p.get("name", p["module"]), href=p["path"], className="toc-link")
            for p in pages_sorted
        ],
        className="toc"
    )

app.layout = html.Div(
    [
        html.Div([html.H2("Table of Contents"), toc()], className="sidebar"),
        html.Div([page_container], className="content")
    ],
    className="shell"
)

if __name__ == "__main__":
    app.run(debug=True)