import streamlit as st
import random

st.set_page_config(page_title="Duck Shot", page_icon="🦆")

if "score" not in st.session_state:
    st.session_state.score = 0
if "misses" not in st.session_state:
    st.session_state.misses = 0
if "duck" not in st.session_state:
    st.session_state.duck = random.randint(0, 8)

st.title("🦆 Duck Shot")
st.write("Click the duck. Avoid the empty spots.")

col1, col2 = st.columns(2)
col1.metric("Score", st.session_state.score)
col2.metric("Misses", st.session_state.misses)

if st.session_state.misses >= 5:
    st.error("Game Over!")
    if st.button("Restart"):
        st.session_state.score = 0
        st.session_state.misses = 0
        st.session_state.duck = random.randint(0, 8)
        st.rerun()
    st.stop()

cell = 0
for _ in range(3):
    cols = st.columns(3)
    for col in cols:
        with col:
            if cell == st.session_state.duck:
                if st.button("🦆", key=cell, use_container_width=True):
                    st.session_state.score += 1
                    st.session_state.duck = random.randint(0, 8)
                    st.rerun()
            else:
                if st.button("🌫️", key=cell, use_container_width=True):
                    st.session_state.misses += 1
                    st.rerun()
        cell += 1
