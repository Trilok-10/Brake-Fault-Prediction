# ======================================================
# FIX FOR MODULE IMPORT (CRITICAL FOR STREAMLIT)
# ======================================================
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ======================================================
# Imports
# ======================================================
import streamlit as st
import pandas as pd
import joblib
import time
import shap
import matplotlib.pyplot as plt
import numpy as np

from alerts.alert_service import send_whatsapp_alert, send_sms_alert

st.set_page_config(page_title="Brake Fault Dashboard", layout="wide")

# ======================================================
# Language configuration
# ======================================================
LANGUAGES = {
    "English": "en",
    "தமிழ்": "ta",
    "हिन्दी": "hi"
}

TEXT = {
    "en": {
        "title": "🚛 Real-Time Brake Fault Monitoring Dashboard",
        "controls": "⚙️ Controls",
        "samples": "Samples",
        "delay": "Delay (seconds)",
        "start": "▶ Start Streaming",
        "safe": "✅ Vehicle operating normally.",
        "fault": "🚨 Brake fault detected! Immediate attention required.",
        "status_safe": "✅ BRAKE STATUS: SAFE",
        "status_fault": "⚠️ BRAKE FAULT DETECTED",
        "finished": "Streaming finished (demo limit)",
        "switch_language": "🌐 Switch Language",
        "shap_title": "🔍 Model Explanation (SHAP)",
        "select_language": "Select your preferred language"
    },
    "ta": {
        "title": "🚛 நேரடி பிரேக் கோளாறு கண்காணிப்பு டாஷ்போர்டு",
        "controls": "⚙️ கட்டுப்பாடுகள்",
        "samples": "மாதிரிகள்",
        "delay": "தாமதம் (வினாடிகள்)",
        "start": "▶ ஸ்ட்ரீமிங் தொடங்கு",
        "safe": "✅ வாகனம் சாதாரணமாக இயங்குகிறது.",
        "fault": "🚨 பிரேக் கோளாறு கண்டறியப்பட்டது! உடனடி கவனம் தேவை.",
        "status_safe": "✅ பிரேக் நிலை: பாதுகாப்பானது",
        "status_fault": "⚠️ பிரேக் கோளாறு கண்டறியப்பட்டது",
        "finished": "ஸ்ட்ரீமிங் முடிந்தது (டெமோ வரம்பு)",
        "switch_language": "🌐 மொழியை மாற்றவும்",
        "shap_title": "🔍 மாதிரி விளக்கம் (SHAP)",
        "select_language": "மொழியை தேர்வு செய்யவும்"
    },
    "hi": {
        "title": "🚛 रीयल-टाइम ब्रेक फॉल्ट मॉनिटरिंग डैशबोर्ड",
        "controls": "⚙️ नियंत्रण",
        "samples": "नमूने",
        "delay": "विलंब (सेकंड)",
        "start": "▶ स्ट्रीमिंग शुरू करें",
        "safe": "✅ वाहन सामान्य रूप से चल रहा है।",
        "fault": "🚨 ब्रेक में खराबी पाई गई! तुरंत ध्यान दें।",
        "status_safe": "✅ ब्रेक स्थिति: सुरक्षित",
        "status_fault": "⚠️ ब्रेक में खराबी पाई गई",
        "finished": "स्ट्रीमिंग समाप्त (डेमो सीमा)",
        "switch_language": "🌐 भाषा बदलें",
        "shap_title": "🔍 मॉडल व्याख्या (SHAP)",
        "select_language": "भाषा चुनें"
    }
}

# ======================================================
# Multilingual Alert Messages
# ======================================================
ALERT_TEXT = {
    "en": "🚨 Brake fault detected! Immediate maintenance required.",
    "ta": "🚨 பிரேக் கோளாறு கண்டறியப்பட்டது! உடனடி பராமரிப்பு தேவை.",
    "hi": "🚨 ब्रेक में खराबी पाई गई! तुरंत मरम्मत आवश्यक है।"
}

# ======================================================
# Session state
# ======================================================
if "language" not in st.session_state:
    st.session_state.language = None

# ======================================================
# STAGE 1 – Language selection
# ======================================================
if st.session_state.language is None:
    st.markdown("## 🌐 Select Language / மொழியை தேர்வு செய்யவும் / भाषा चुनें")

    selected = st.radio(
        TEXT["en"]["select_language"],
        list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )

    if st.button("Continue"):
        st.session_state.language = LANGUAGES[selected]
        st.rerun()

    st.stop()

# ======================================================
# STAGE 2 – Dashboard
# ======================================================
lang = st.session_state.language
T = TEXT[lang]

st.title(T["title"])

# ======================================================
# Load model & data
# ======================================================
@st.cache_resource
def load_model():
    return joblib.load("models/rf_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/processed_data.csv")

rf_model = load_model()
df = load_data()
X = df.drop("class", axis=1)

explainer = shap.TreeExplainer(rf_model)

# ======================================================
# Sidebar
# ======================================================
st.sidebar.header(T["controls"])

max_samples = st.sidebar.slider(T["samples"], 10, 150, 50)
delay = st.sidebar.slider(T["delay"], 0.1, 2.0, 0.5)
show_shap = st.sidebar.checkbox("🔍 Show SHAP Explanation")

st.sidebar.subheader("📲 Alert Settings")
enable_whatsapp = st.sidebar.checkbox("Enable WhatsApp Alert", value=True)
enable_sms = st.sidebar.checkbox("Enable SMS Alert", value=True)

st.sidebar.header(T["switch_language"])
reverse_lang = {v: k for k, v in LANGUAGES.items()}
current_label = reverse_lang[st.session_state.language]

new_label = st.sidebar.selectbox(
    "",
    list(LANGUAGES.keys()),
    index=list(LANGUAGES.keys()).index(current_label),
    label_visibility="collapsed"
)

if LANGUAGES[new_label] != st.session_state.language:
    st.session_state.language = LANGUAGES[new_label]
    st.rerun()

start = st.sidebar.button(T["start"])

# ======================================================
# UI placeholders
# ======================================================
status_box = st.empty()
prob_box = st.empty()
alert_box = st.empty()
data_box = st.empty()
shap_box = st.empty()

# ======================================================
# Streaming + SHAP + Alerts
# ======================================================
last_alert_sent = -1
ALERT_COOLDOWN = 5

if start:
    for i in range(max_samples):
        sample = X.iloc[i]
        sample_df = pd.DataFrame([sample], columns=X.columns)

        pred = rf_model.predict(sample_df)[0]
        prob = rf_model.predict_proba(sample_df)[0][1]

        if pred == 1:
            status_box.error(T["status_fault"])
            alert_box.error(T["fault"])

            if i - last_alert_sent >= ALERT_COOLDOWN:
                alert_message = ALERT_TEXT[lang]

                if enable_whatsapp:
                    send_whatsapp_alert(alert_message)

                if enable_sms:
                    send_sms_alert(alert_message)

                last_alert_sent = i
        else:
            status_box.success(T["status_safe"])
            alert_box.success(T["safe"])

        prob_box.metric("Fault Probability", f"{prob:.2f}")
        data_box.dataframe(sample_df.iloc[:, :10])

        # ================= SHAP =================
        if show_shap:
            shap_box.subheader(T["shap_title"])

            shap_out = explainer.shap_values(sample_df)
            values = np.array(shap_out[0]).reshape(-1)

            min_len = min(len(values), len(X.columns))
            shap_df = pd.DataFrame({
                "Feature": X.columns[:min_len],
                "SHAP Value": values[:min_len]
            })

            shap_df["abs"] = shap_df["SHAP Value"].abs()
            shap_df = shap_df.sort_values("abs", ascending=False).head(10)

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.barh(shap_df["Feature"], shap_df["SHAP Value"])
            ax.invert_yaxis()
            ax.set_xlabel("SHAP impact")
            ax.set_title("Top Feature Contributions")

            shap_box.pyplot(fig)

        time.sleep(delay)

    st.warning(T["finished"])
