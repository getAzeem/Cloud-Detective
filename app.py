from dash import Dash, html, dcc, Input, Output, State
import re

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "background": "#0f172a",
        "color": "white",
        "minHeight": "100vh",
        "padding": "35px",
    },
    children=[
        html.H1("RegexLab"),
        html.P("Test regular expressions against real text instantly."),

        html.Label("Regex Pattern"),
        dcc.Input(
            id="pattern",
            value=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            style={"width": "100%", "padding": "12px", "marginBottom": "18px"},
        ),

        html.Label("Test Text"),
        dcc.Textarea(
            id="text",
            value="Contact azeem@example.com or admin@test.io for support.",
            style={
                "width": "100%",
                "height": "180px",
                "padding": "12px",
                "marginBottom": "18px",
            },
        ),

        html.Button("Run Regex", id="run", n_clicks=0),

        html.Div(id="output", style={"marginTop": "25px"}),
    ],
)

@app.callback(
    Output("output", "children"),
    Input("run", "n_clicks"),
    State("pattern", "value"),
    State("text", "value"),
)
def run_regex(n_clicks, pattern, text):
    try:
        matches = list(re.finditer(pattern, text))

        if not matches:
            return html.Div([
                html.H3("No matches found", style={"color": "#f87171"})
            ])

        result_rows = []

        for i, match in enumerate(matches, start=1):
            result_rows.append(
                html.Div(
                    style={
                        "background": "#111827",
                        "border": "1px solid #334155",
                        "borderRadius": "10px",
                        "padding": "15px",
                        "marginBottom": "12px",
                    },
                    children=[
                        html.H4(f"Match #{i}"),
                        html.P(f"Value: {match.group()}"),
                        html.P(f"Start index: {match.start()}"),
                        html.P(f"End index: {match.end()}"),
                    ],
                )
            )

        return html.Div([
            html.H3(f"{len(matches)} match(es) found", style={"color": "#4ade80"}),
            *result_rows
        ])

    except re.error as e:
        return html.Div([
            html.H3("Invalid Regex", style={"color": "#f87171"}),
            html.P(str(e))
        ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
