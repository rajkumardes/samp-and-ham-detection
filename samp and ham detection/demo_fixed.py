
from pathlib import Path

import streamlit as st
import joblib

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="SpamShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD TRAINED MODEL ----------------
MODEL_PATH = Path(__file__).resolve().parent / "spam"

@st.cache_resource
def load_model(model_path):
    if not model_path.is_file():
        raise FileNotFoundError(
            f"Model file not found at: {model_path}"
        )

    model = joblib.load(model_path)

    if not callable(getattr(model, "predict", None)):
        raise TypeError(
            "The saved model does not have a predict() method."
        )

    return model

try:
    text_model = load_model(MODEL_PATH)
    model_error = None
except Exception as exc:
    text_model = None
    model_error = f"{type(exc).__name__}: {exc}"

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(99,102,241,.22), transparent 28%),
        radial-gradient(circle at 100% 0%, rgba(6,182,212,.18), transparent 28%),
        linear-gradient(135deg, #020617 0%, #0f172a 55%, #020617 100%);
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 1rem;
}
#MainMenu, footer {
    visibility: hidden;
}
h1, h2, h3, p, label, .stMarkdown {
    color: #f8fafc;
}
.hero-icon {
    text-align: center;
    font-size: 64px;
}
.hero-title {
    text-align: center;
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 900;
    background: linear-gradient(90deg, #818cf8, #38bdf8, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
    margin: 6px 0 35px;
}
.card {
    background: rgba(30,41,59,.78);
    border: 1px solid rgba(148,163,184,.25);
    border-radius: 20px;
    padding: 24px 18px;
    min-height: 145px;
    text-align: center;
    box-shadow: 0 12px 35px rgba(0,0,0,.25);
}
.card-icon {
    font-size: 34px;
}
.card-title {
    color: #f8fafc;
    font-size: 19px;
    font-weight: 800;
    margin-top: 8px;
}
.card-text {
    color: #cbd5e1;
    font-size: 14px;
    margin-top: 7px;
}
.section-title {
    color: #f8fafc;
    font-size: 28px;
    font-weight: 800;
    margin-top: 38px;
}
.section-text {
    color: #cbd5e1;
    font-size: 15px;
    margin-bottom: 15px;
}
textarea {
    background: #0b1220 !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    border-radius: 16px !important;
    font-size: 16px !important;
}
textarea::placeholder {
    color: #94a3b8 !important;
}
.stButton > button {
    width: 100%;
    min-height: 52px;
    border: 0;
    border-radius: 15px;
    color: white !important;
    font-size: 17px;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1, #06b6d4) !important;
    box-shadow: 0 10px 28px rgba(99,102,241,.30);
}
.stButton > button:hover {
    transform: translateY(-2px);
}
div[data-testid="stAlert"] {
    border-radius: 15px;
}
.footer {
    text-align: center;
    color: #cbd5e1;
    padding: 25px 0 5px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="hero-icon">🛡️</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="hero-title">SpamShield AI</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="hero-subtitle">'
    'Intelligent Spam &amp; Ham Message Detection'
    '</div>',
    unsafe_allow_html=True
)

# ---------------- MODEL STATUS ----------------
if model_error:
    st.error("The trained spam model could not be loaded.")
    st.code(str(MODEL_PATH), language="text")
    st.error(model_error)
    st.info(
        "Check that the file named 'spam' is the trained model "
        "created by your notebook and is saved beside this script."
    )
    st.stop()

# ---------------- FEATURE CARDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🤖</div>
        <div class="card-title">AI Powered</div>
        <div class="card-text">
            Machine-learning-based message classification
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">⚡</div>
        <div class="card-title">Instant Detection</div>
        <div class="card-text">
            Analyze messages and get results instantly
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🔒</div>
        <div class="card-title">Message Protection</div>
        <div class="card-text">
            Identify potentially unwanted messages
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- MESSAGE INPUT ----------------
st.markdown(
    '<div class="section-title">💬 Analyze Your Message</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="section-text">'
    'Enter a message below to classify it as Spam or Ham.'
    '</div>',
    unsafe_allow_html=True
)

message = st.text_area(
    "Message",
    placeholder="Example: Congratulations! You have won a free prize...",
    height=180,
    label_visibility="collapsed",
    key="message_input"
)

if st.button("🚀 Analyze Message", use_container_width=True):
    if not message.strip():
        st.warning("⚠️ Please enter a message before analyzing.")
    else:
        try:
            prediction = text_model.predict([message])[0]
            result = str(prediction).strip().lower()

            if result == "spam" or "spam" in result:
                st.error("🚨 SPAM DETECTED")
                st.write(
                    "This message was classified as spam by the model."
                )
            elif result == "ham" or "ham" in result:
                st.success("✅ HAM MESSAGE")
                st.write(
                    "This message was classified as ham by the model."
                )
            else:
                st.info(f"Model prediction: {prediction}")

        except Exception as exc:
            st.error("Prediction failed.")
            st.code(f"{type(exc).__name__}: {exc}", language="text")

# ---------------- FOOTER ----------------
st.divider()
st.markdown("""
<div class="footer">
    🛡️ SpamShield AI | Machine Learning Spam Detection<br><br>
    Built with Python + Streamlit + Machine Learning
</div>
""", unsafe_allow_html=True)
