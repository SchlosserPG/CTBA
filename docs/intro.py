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

app = Dash(__name__, title="Purpose of Git")


layout = html.Div(
    [
        # 1) Purpose of Git
        html.Div(html.H1("Understanding Git and GitLab", style={"textAlign": "center"})),
        html.Div(
            html.Ul(
                [
                    html.Li(
                        "Git is a decentralized version control system for tracking file changes, "
                        "especially in software projects with many small text files. It records who "
                        "made changes and when, supports collaboration, and keeps all past versions "
                        "and branches."
                    ),
                    html.Li(
                        "Works best with text files; less effective for binary files like Word docs, "
                        "audio/video, or VM images."
                    ),
                    html.Li(
                        [
                            html.Strong("git Command"),
                            html.Ul(
                                [
                                    html.Li("The primary way to control Git via the terminal/PowerShell."),
                                    html.Li("Tasks: download projects, commit changes, switch branches, undo edits, etc."),
                                    html.Li(['“', html.B("Git"), '” (capitalized) = the system/concepts;'], className="check"),
                                    html.Li([html.B("git"), " (lowercase) = the command."], className="check"),
                                ],
                                className="sub",
                            ),
                        ]
                    ),
                    html.Li(
                        "IDEs (e.g., Visual Studio) and editors (e.g., VS Code) offer built-in Git tools; "
                        "web platforms like GitHub/GitLab add extra features (issue tracking, automated tests)."
                    ),
                ],
                className="bullets",
            ),
            className="panel",
        ),

        # 2) Git / GitHub / GitLab
        html.Div(html.H2("Git, GitHub, GitLab", className="h2"), className="card header"),
        html.Div(
            html.Ul(
                [
                    html.Li([html.Strong("Git:"), " Works without central servers."]),
                    html.Li(
                        [
                            html.Strong("GitHub:"),
                            " Most popular host; acquired by Microsoft in 2018; free for public and most private projects.",
                            html.Ul(
                                [
                                    html.Li("A cloud-based platform for hosting and collaborating on code projects."),
                                    html.Li("Built on Git (a distributed version control system)."),
                                    html.Li("Supports version tracking, collaboration, and project management."),
                                    html.Li("Enables teamwork on coding projects."),
                                    html.Li("Provides a historical record of changes."),
                                    html.Li("Integrates with many tools."),
                                ],
                                className="sub",
                            ),
                        ]
                    ),
                    html.Li(
                        [html.Strong("GitLab:"), " Similar features; open-source, can be self-hosted—good for organizations that want control."]
                    ),
                ],
                className="bullets",
            ),
            className="panel",
        ),

        # 3) Getting Started with Git & GitHub
        html.Div(html.H2("Getting Started with Git & GitHub", className="h2"), className="card header"),
html.Div(
    [
        html.Ul(
            [
                html.Li(["Create an account at ", html.A("github.com", href="https://github.com", target="_blank")]),
                html.Li("Install Git (if using locally)"),
                html.Li(
                    [
                        html.Strong("Configure Git"),
                        html.Ul(
                            [
                                html.Li("Set your name and email (used in commit metadata):"),
                            ],
                            className="sub",
                        ),
                    ]
                ),
                html.Li(["Install ", html.A("GitHub Desktop", href="https://desktop.github.com/", target="_blank"), " (optional) for a GUI"]),
                html.Li(["Choose an editor (", html.A("VS Code", href="https://code.visualstudio.com/", target="_blank"), " recommended)"]),
            ],
            className="bullets",
        ),
        # code block OUTSIDE the list
        html.Pre(
            'git config --global user.name "Your Name"\n'
            'git config --global user.email "you@example.com"',
            className="code",
        ),
    ],
    className="panel",
),

       # Create a Repository & First Push
html.Div(html.H2("Create a Repository & First Push", className="h2"), className="card header"),
html.Div(
    [
        html.Ul(
            [
                html.Li([ "Go to ", html.A("GitHub", href="https://github.com", target="_blank"), " → Click ", html.B("New Repository") ]),
                html.Li(
                    [
                        "Name your repo and choose:",
                        html.Ul([ html.Li("Public or Private"), html.Li("Add a README (optional but recommended)") ], className="sub"),
                    ]
                ),
                html.Li("Local option: create a folder → initialize Git → link to the GitHub repo"),
                html.Li("Initial commit example:"),
            ],
            className="bullets",
        ),
        # code block OUTSIDE the list
        html.Pre(
            "git init\n"
            "git add .\n"
            "git commit -m \"Initial commit\"\n"
            "git branch -M main\n"
            "git remote add origin https://github.com/USERNAME/REPO_NAME.git\n"
            "git push -u origin main",
            className="code",
        ),
    ],
    className="panel",
    ),
    ],
    className="container",
)
app.layout = layout 

