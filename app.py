from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta

app = Dash(__name__)
server = app.server

def generate_data():
    endpoints = ["/api/login", "/api/users", "/api/orders", "/api/payment", "/api/search"]
    rows = []

    now = datetime.now()

    for i in range(240):
        endpoint = random.choice(endpoints)
        base = {
            "/api/login": 90,
            "/api/users": 140,
            "/api/orders": 220,
            "/api/payment": 380,
            "/api/search": 260,
        }[endpoint]

        latency = max(20, random.gauss(base, base * 0.25))
        status = random.choices([200, 201, 400, 401, 500, 503], [70, 8, 8, 5, 6, 3])[0]

        if status >= 500:
            latency *= random.uniform(1.4, 2.8)

        rows.append({
            "time": now - timedelta(minutes=240 - i),
            "endpoint": endpoint,
            "latency_ms": round(latency, 2),
            "status": status,
            "method": random.choice(["GET", "POST", "PUT", "DELETE"]),
        })

    return pd.DataFrame(rows)

df = generate_data()

app.layout = html.Div(
    style={
        "background": "#0f172a",
        "minHeight": "100vh",
        "color": "#e5e7eb",
        "fontFamily": "Arial",
        "padding": "28px",
    },
    children=[
        html.H1("API Latency Analyzer", style={"marginBottom": "4px"}),
        html.P(
            "Technical dashboard for endpoint latency, error rate, SLA breaches, and bottleneck detection.",
            style={"color": "#94a3b8"},
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr 1fr",
                "gap": "16px",
                "marginTop": "22px",
                "marginBottom": "22px",
            },
            children=[
                html.Div([
                    html.Label("Endpoint"),
                    dcc.Dropdown(
                        id="endpoint",
                        options=[{"label": "All endpoints", "value": "all"}]
                        + [{"label": e, "value": e} for e in sorted(df["endpoint"].unique())],
                        value="all",
                        clearable=False,
                        style={"color": "#111"},
                    ),
                ]),
                html.Div([
                    html.Label("HTTP Status"),
                    dcc.Dropdown(
                        id="status",
                        options=[{"label": "All statuses", "value": "all"}]
                        + [{"label": str(s), "value": s} for s in sorted(df["status"].unique())],
                        value="all",
                        clearable=False,
                        style={"color": "#111"},
                    ),
                ]),
                html.Div([
                    html.Label("SLA Threshold"),
                    dcc.Slider(
                        id="sla",
                        min=100,
                        max=1000,
                        step=50,
                        value=300,
                        marks={100: "100ms", 300: "300ms", 600: "600ms", 1000: "1s"},
                    ),
                ]),
            ],
        ),

        html.Div(id="cards"),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "2fr 1fr",
                "gap": "18px",
                "marginTop": "22px",
            },
            children=[
                dcc.Graph(id="latency_chart"),
                dcc.Graph(id="status_chart"),
            ],
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "18px",
                "marginTop": "18px",
            },
            children=[
                dcc.Graph(id="endpoint_chart"),
                html.Div(id="analysis_box"),
            ],
        ),
    ],
)

@app.callback(
    Output("cards", "children"),
    Output("latency_chart", "figure"),
    Output("status_chart", "figure"),
    Output("endpoint_chart", "figure"),
    Output("analysis_box", "children"),
    Input("endpoint", "value"),
    Input("status", "value"),
    Input("sla", "value"),
)
def update(endpoint, status, sla):
    data = df.copy()

    if endpoint != "all":
        data = data[data["endpoint"] == endpoint]

    if status != "all":
        data = data[data["status"] == status]

    total = len(data)
    avg_latency = round(data["latency_ms"].mean(), 2) if total else 0
    p95 = round(data["latency_ms"].quantile(0.95), 2) if total else 0
    error_rate = round((len(data[data["status"] >= 500]) / total) * 100, 2) if total else 0
    sla_breaches = len(data[data["latency_ms"] > sla]) if total else 0

    cards = html.Div(
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "16px",
        },
        children=[
            metric_card("Requests", total),
            metric_card("Avg Latency", f"{avg_latency} ms"),
            metric_card("P95 Latency", f"{p95} ms"),
            metric_card("5xx Error Rate", f"{error_rate}%"),
        ],
    )

    latency_fig = px.line(
        data,
        x="time",
        y="latency_ms",
        color="endpoint",
        title="Latency Over Time",
    )
    latency_fig.add_hline(y=sla, line_dash="dash", annotation_text=f"SLA {sla}ms")
    style_fig(latency_fig)

    status_fig = px.histogram(
        data,
        x="status",
        title="HTTP Status Distribution",
    )
    style_fig(status_fig)

    endpoint_group = (
        data.groupby("endpoint")["latency_ms"]
        .mean()
        .reset_index()
        .sort_values("latency_ms", ascending=False)
    )

    endpoint_fig = px.bar(
        endpoint_group,
        x="endpoint",
        y="latency_ms",
        title="Average Latency by Endpoint",
    )
    style_fig(endpoint_fig)

    bottleneck = endpoint_group.iloc[0]["endpoint"] if not endpoint_group.empty else "N/A"

    analysis = html.Div(
        style={
            "background": "#111827",
            "border": "1px solid #334155",
            "borderRadius": "14px",
            "padding": "22px",
            "height": "100%",
        },
        children=[
            html.H3("Automated Technical Analysis"),
            html.P(f"Detected bottleneck endpoint: {bottleneck}"),
            html.P(f"SLA breaches: {sla_breaches} requests above {sla} ms"),
            html.P(f"P95 latency: {p95} ms"),
            html.H4("Suggested Engineering Actions"),
            html.Ul([
                html.Li("Check database queries for slow endpoints."),
                html.Li("Add caching for repeated expensive responses."),
                html.Li("Review 5xx logs around high-latency timestamps."),
                html.Li("Use async workers or background jobs for heavy routes."),
            ]),
        ],
    )

    return cards, latency_fig, status_fig, endpoint_fig, analysis

def metric_card(title, value):
    return html.Div(
        style={
            "background": "#111827",
            "border": "1px solid #334155",
            "borderRadius": "14px",
            "padding": "18px",
        },
        children=[
            html.Div(title, style={"color": "#94a3b8", "fontSize": "14px"}),
            html.Div(value, style={"fontSize": "28px", "fontWeight": "bold"}),
        ],
    )

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="#e5e7eb",
        title_font_color="#f8fafc",
        margin=dict(l=30, r=30, t=55, b=30),
    )
    fig.update_xaxes(gridcolor="#334155")
    fig.update_yaxes(gridcolor="#334155")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
