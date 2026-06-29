from dash import Dash, html, dcc, Input, Output
import random

app = Dash(__name__)
server = app.server

moods = {
    "Happy": {
        "emoji": "😄",
        "color": "#FFD93D",
        "songs": ["Happy - Pharrell Williams", "Can't Stop the Feeling", "Uptown Funk"],
        "activity": "Go for a walk, call a friend, or dance for 5 minutes."
    },
    "Sad": {
        "emoji": "😔",
        "color": "#74B9FF",
        "songs": ["Fix You - Coldplay", "Someone Like You", "Let Her Go"],
        "activity": "Write your thoughts, drink water, and take a slow walk."
    },
    "Focused": {
        "emoji": "🎯",
        "color": "#55EFC4",
        "songs": ["Lo-fi Beats", "Deep Focus", "Coding Mode"],
        "activity": "Start a 25-minute focus timer and avoid distractions."
    },
    "Angry": {
        "emoji": "😤",
        "color": "#FF7675",
        "songs": ["Believer - Imagine Dragons", "Numb - Linkin Park", "Stronger"],
        "activity": "Take 10 deep breaths and do a quick workout."
    },
    "Relaxed": {
        "emoji": "🌙",
        "color": "#A29BFE",
        "songs": ["Weightless", "Calm Piano", "Ocean Sounds"],
        "activity": "Stretch, breathe slowly, and relax your shoulders."
    }
}

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "padding": "40px",
        "fontFamily": "Arial",
        "background": "linear-gradient(135deg, #141E30, #243B55)",
        "color": "white",
        "textAlign": "center",
    },
    children=[
        html.H1("🎧 Mood Music Recommender", style={"fontSize": "48px"}),
        html.P("Pick your mood and get music + activity suggestions instantly."),

        html.Div(
            style={
                "maxWidth": "500px",
                "margin": "30px auto",
                "background": "rgba(255,255,255,0.12)",
                "padding": "25px",
                "borderRadius": "20px",
            },
            children=[
                dcc.Dropdown(
                    id="mood",
                    options=[{"label": f"{v['emoji']} {k}", "value": k} for k, v in moods.items()],
                    value="Happy",
                    clearable=False,
                    style={"color": "black"},
                ),
                html.Br(),
                html.Button(
                    "Generate Recommendation",
                    id="btn",
                    n_clicks=0,
                    style={
                        "padding": "12px 25px",
                        "border": "none",
                        "borderRadius": "12px",
                        "fontSize": "16px",
                        "fontWeight": "bold",
                        "cursor": "pointer",
                    },
                ),
            ],
        ),

        html.Div(id="result"),
    ],
)

@app.callback(
    Output("result", "children"),
    Input("btn", "n_clicks"),
    Input("mood", "value"),
)
def recommend(n_clicks, mood):
    data = moods[mood]
    song = random.choice(data["songs"])

    return html.Div(
        style={
            "maxWidth": "650px",
            "margin": "30px auto",
            "padding": "30px",
            "borderRadius": "25px",
            "background": data["color"],
            "color": "#111",
            "boxShadow": "0 15px 40px rgba(0,0,0,0.35)",
        },
        children=[
            html.H1(data["emoji"], style={"fontSize": "70px", "margin": "0"}),
            html.H2(f"Your mood: {mood}"),
            html.H3("🎵 Recommended Song"),
            html.P(song, style={"fontSize": "22px", "fontWeight": "bold"}),
            html.H3("✨ Suggested Activity"),
            html.P(data["activity"], style={"fontSize": "18px"}),
        ],
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
