import pandas as pd
import time
import joblib
import sys

print("🚀 REAL-TIME STREAMING SCRIPT STARTED", flush=True)

# ====================================
# Load model
# ====================================
try:
    rf_model = joblib.load("../models/rf_model.pkl")
    print("✅ Model loaded successfully", flush=True)
except Exception as e:
    print("❌ Failed to load model:", e, flush=True)
    sys.exit(1)

# ====================================
# Load data
# ====================================
try:
    df = pd.read_csv("../data/processed/processed_data.csv")
    print("✅ Data loaded successfully", flush=True)
except Exception as e:
    print("❌ Failed to load data:", e, flush=True)
    sys.exit(1)

X = df.drop("class", axis=1)

print("📊 Total available samples:", len(X), flush=True)

# ====================================
# DEMO CONFIGURATION 🔥
# ====================================

MAX_SAMPLES = 150    # 👈 demo sample limit
DELAY = 0.5          # 👈 time delay (seconds)

# ====================================
# Real-time stream generator
# ====================================
def stream_data(X, delay):
    for i in range(len(X)):
        yield i, X.iloc[i]
        time.sleep(delay)

# ====================================
# MODE SELECTION (COMMENT / UNCOMMENT)
# ====================================

"""
MODE 1️⃣ : DEMO MODE (LIMITED SAMPLES)
✔ Streams only MAX_SAMPLES
✔ Allows MULTIPLE brake fault alerts
✔ Best for review & viva
"""

print("\n🚦 Starting real-time brake fault monitoring (DEMO MODE)...\n", flush=True)

for i, sample in stream_data(X, DELAY):

    if i >= MAX_SAMPLES:
        print("\n🛑 Demo completed (sample limit reached)", flush=True)
        break

    sample_df = pd.DataFrame([sample], columns=X.columns)

    pred = rf_model.predict(sample_df)[0]
    prob = rf_model.predict_proba(sample_df)[0][1]

    if pred == 1:
        print(f"⚠️ ALERT [{i}] Brake Fault Detected | Probability = {prob:.2f}", flush=True)
    else:
        print(f"✅ SAFE  [{i}] No Fault | Probability = {prob:.2f}", flush=True)

print("\n✅ Demo streaming finished", flush=True)


"""
===============================================================
MODE 2️⃣ : FULL STREAMING MODE (UNLIMITED – REAL SYSTEM)
❗ COMMENT OUT MODE 1 ABOVE
❗ UNCOMMENT BELOW CODE ONLY WHEN REQUIRED
===============================================================

print("\\n🚦 Starting FULL real-time streaming (ALL DATA)...\\n", flush=True)

for i, sample in stream_data(X, DELAY):

    sample_df = pd.DataFrame([sample], columns=X.columns)

    pred = rf_model.predict(sample_df)[0]
    prob = rf_model.predict_proba(sample_df)[0][1]

    if pred == 1:
        print(f"⚠️ ALERT [{i}] Brake Fault Detected | Probability = {prob:.2f}", flush=True)
    else:
        print(f"✅ SAFE  [{i}] No Fault | Probability = {prob:.2f}", flush=True)
"""