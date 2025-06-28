import streamlit as st
from emotion_detector import detect_emotion
import pandas as pd
import time
import plotly.express as px

# ✅ Session states
if "emotion_log" not in st.session_state:
    st.session_state.emotion_log = []

# ✅ Background color and contrast text
def set_background_color(emotion):
    colors = {
        "joy": ("#FFF176", "#212121"),
        "sadness": ("#81D4FA", "#0D47A1"),
        "anger": ("#FF8A80", "#B71C1C"),
        "fear": ("#CE93D8", "#4A148C"),
        "neutral": ("#E0E0E0", "#212121")
    }
    bg_color, text_color = colors.get(emotion, ("#FFFFFF", "#000000"))

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        h1, h2, h3, h4, h5, h6, p, div, span, label {{
            color: {text_color} !important;
        }}
        button {{
            color: {text_color} !important;
            background-color: white !important;
            border: 1px solid {text_color} !important;
        }}
        .stButton>button:hover {{
            background-color: #f1f1f1 !important;
            color: {text_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 🎵 Music button
def custom_button(text, link):
    st.markdown(f"""
    <a href="{link}" target="_blank">
        <button style='background-color:black;color:white;padding:10px 18px;border:none;border-radius:8px;font-size:16px;margin:6px 2px;cursor:pointer'>
            {text}
        </button>
    </a>
    """, unsafe_allow_html=True)

# 🚀 Page setup
st.set_page_config(page_title="EmotionRide", layout="centered")
st.title("🚗 EmotionRide")
st.subheader("📝 Type to Detect Emotion")

# ✍️ Text input
user_text = st.text_input("📝 Type your feeling:")

# 🧠 Emotion detection
if user_text:
    with st.spinner("Analyzing emotion..."):
        emotion, confidence = detect_emotion(user_text)
        set_background_color(emotion)

        st.session_state.emotion_log.append({
            "emotion": emotion,
            "confidence": confidence,
            "time": time.strftime("%H:%M:%S")
        })

        st.success(f"Detected Emotion: **{emotion}** ({confidence*100:.1f}%)")

        if emotion == "joy":
            st.balloons()
            st.info("🎉 You're glowing! Do something exciting!")
        elif emotion == "sadness":
            st.warning("🧸 You deserve peace. Try something calming.")
        elif emotion == "anger":
            st.warning("🕊️ Take a deep breath. Let it go.")
        elif emotion == "fear":
            st.info("🛡️ You're strong. You're safe.")
        elif emotion == "neutral":
            st.info("☕ Nice balance! Chill or explore.")

        st.markdown("### 🎵 Mood Music")
        links = {
            "joy": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
            "sadness": "https://www.youtube.com/watch?v=2OEL4P1Rz04",
            "anger": "https://www.youtube.com/watch?v=2OEL4P1Rz04",
            "fear": "https://www.youtube.com/watch?v=2OEL4P1Rz04",
            "neutral": "https://www.youtube.com/watch?v=jfKfPfyJRdk"
        }
        custom_button("▶️ Play Playlist", links.get(emotion, "#"))

        # 📊 Emotion graph
        if st.session_state.emotion_log:
            df = pd.DataFrame(st.session_state.emotion_log)
            mood_counts = df["emotion"].value_counts().reset_index()
            mood_counts.columns = ["Emotion", "Count"]

            fig = px.bar(
                mood_counts,
                x="Emotion",
                y="Count",
                color="Emotion",
                title="🧠 Mood Frequency This Session",
                color_discrete_map={
                    "joy": "#FFD700",
                    "sadness": "#4FC3F7",
                    "anger": "#EF5350",
                    "fear": "#BA68C8",
                    "neutral": "#90A4AE"
                }
            )

            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(color="#000000", size=14)
            )

            st.plotly_chart(fig, use_container_width=True)

