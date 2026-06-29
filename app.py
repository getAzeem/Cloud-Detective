from dash import Dash, html, dcc, Input, Output, State
import base64
import io
import pandas as pd

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "background": "#0f172a",
        "color": "white",
        "minHeight": "100vh",
        "padding": "40px",
    },
    children=[
        html.H1("📦 File Pipeline Builder"),
        html.P("Drag and drop a CSV file to simulate a simple data pipeline."),

        dcc.Upload(
            id="upload",
            children=html.Div(["Drag and drop file here, or click to upload"]),
            style={
                "width": "100%",
                "height": "160px",
                "lineHeight": "160px",
                "borderWidth": "2px",
                "borderStyle": "dashed",
                "borderRadius": "14px",
                "textAlign": "center",
                "background": "#111827",
                "borderColor": "#38bdf8",
                "cursor": "pointer",
            },
            multiple=False,
        ),

        html.Div(id="output", style={"marginTop": "30px"}),
    ],
)

@app.callback(
    Output("output", "children"),
    Input("upload", "contents"),
    State("upload", "filename"),
)
def process_file(contents, filename):
    if contents is None:
        return html.Div("No file uploaded yet.")

    try:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)

        if filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        else:
            return html.Div("Only CSV files are supported right now.", style={"color": "#f87171"})

        rows, cols = df.shape

        return html.Div([
            html.H2("✅ Pipeline Completed"),

            html.Div([
                html.P("1. File received ✅"),
                html.P("2. CSV schema detected ✅"),
                html.P(f"3. Rows detected: {rows} ✅"),
                html.P(f"4. Columns detected: {cols} ✅"),
                html.P("5. File ready for processing ✅"),
            ], style={
                "background": "#111827",
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "20px",
            }),

            html.H3("Preview"),
            html.Table(
                [
                    html.Tr([html.Th(col) for col in df.columns])
                ] + [
                    html.Tr([html.Td(str(df.iloc[i][col])) for col in df.columns])
                    for i in range(min(5, len(df)))
                ],
                style={
                    "width": "100%",
                    "background": "#111827",
                    "borderCollapse": "collapse",
                },
            ),
        ])

    except Exception as e:
        return html.Div(f"Error processing file: {e}", style={"color": "#f87171"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
