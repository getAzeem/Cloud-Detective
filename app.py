import streamlit as st
import random
import time

st.set_page_config(page_title="Duck Dash", page_icon="🦆", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #87CEEB 0%, #B7F08A 100%);
}
.game-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #ff6b00;
    text-shadow: 3px 3px #fff;
}
.duck-box {
    background: rgba(255,255,255,0.35);
    border: 4px solid white;
    border-radius: 25px;
    padding: 30px;
    min-height: 420px;
}
.score-card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    font-size: 25px;
    font-weight: bold;
}
button {
    font-size: 30px !important;
    border-radius: 20px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="game-title">🦆 Duck Dash</div>', unsafe_allow_html=True)
st.caption("Click the duck before it flies away!")

if "score" not in st.session_state:
    st.session_state.score = 0
if "misses" not in st.session_state:
    st.session_state.misses = 0
if "round" not in st.session_state:
    st.session_state.round = 1
if "duck_pos" not in st.session_state:
    st.session_state.duck_pos = random.randint(0, 8)

left, mid, right = st.columns(3)

with left:
    st.markdown(f'<div class="score-card">🎯 Score<br>{st.session_state.score}</div>', unsafe_allow_html=True)

with mid:
    st.markdown(f'<div class="score-card">🔥 Round<br>{st.session_state.round}</div>', unsafe_allow_html=True)

with right:
    st.markdown(f'<div class="score-card">❌ Misses<br>{st.session_state.misses}/5</div>', unsafe_allow_html=True)

st.write("")

if st.session_state.misses >= 5:
    st.error("Game Over! The ducks escaped.")
    st.balloons()

    if st.button("🔁 Restart Game", use_container_width=True):
        st.session_state.score = 0
        st.session_state.misses = 0
        st.session_state.round = 1
        st.session_state.duck_pos = random.randint(0, 8)
        st.rerun()

    st.stop()

st.markdown('<div class="duck-box">', unsafe_allow_html=True)

positions = st.columns(3)

cell = 0
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        with cols[col]:
            if cell == st.session_state.duck_pos:
                if st.button("🦆", key=f"duck_{cell}", use_container_width=True):
                    st.session_state.score += 10
                    st.session_state.round += 1
                    st.session_state.duck_pos = random.randint(0, 8)
                    st.success("Hit! Nice shot 🎯")
                    time.sleep(0.3)
                    st.rerun()
            else:
                if st.button("🌿", key=f"grass_{cell}", use_container_width=True):
                    st.session_state.misses += 1
                    st.warning("Missed!")
                    time.sleep(0.3)
                    st.rerun()
        cell += 1

st.markdown('</div>', unsafe_allow_html=True)

st.write("")

if st.button("Duck escaped! Next round 🦆", use_container_width=True):
    st.session_state.misses += 1
    st.session_state.round += 1
    st.session_state.duck_pos = random.randint(0, 8)
    st.rerun()
