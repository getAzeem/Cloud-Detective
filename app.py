import streamlit as st
import re

st.set_page_config(
    page_title="Human Behavior Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Human Behavior Analyzer")
st.caption("Analyze stories, conversations and situations")

story = st.text_area(
    "Describe a situation",
    height=200,
    placeholder="Tell me what happened..."
)

if st.button("Analyze"):
    if not story.strip():
        st.warning("Please enter some text.")
        st.stop()

    words = len(story.split())

    trust_score = 90

    suspicious_words = [
        "but",
        "however",
        "later",
        "suddenly",
        "lied",
        "excuse",
        "fake"
    ]

    findings = []

    for word in suspicious_words:
        if word.lower() in story.lower():
            trust_score -= 8
            findings.append(
                f"Possible contradiction indicator: '{word}'"
            )

    trust_score = max(0, min(100, trust_score))

    if trust_score > 75:
        verdict = "Likely Consistent"
    elif trust_score > 50:
        verdict = "Needs More Context"
    else:
        verdict = "Potential Inconsistencies"

    st.metric("Trust Score", f"{trust_score}%")

    st.subheader("Verdict")
    st.success(verdict)

    st.subheader("Observations")

    if findings:
        for item in findings:
            st.write("•", item)
    else:
        st.write("No obvious contradiction patterns detected.")

    st.subheader("Text Statistics")

    st.write(f"Word Count: {words}")

    st.subheader("AI Recommendation")

    st.info(
        "Avoid jumping to conclusions. "
        "Gather more information before judging intentions."
    )
