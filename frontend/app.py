import os
import requests
import numpy as np
import pandas as pd
import streamlit as st
# =========================
# 1) Streamlit base config
# =========================
st.set_page_config(
    page_title="Stress Forecast",
    page_icon="🫀",
    layout="wide"
)

# =========================
# 2) CSS theme
# =========================
try:
    with open("assets/styles.css") as f:st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
 # App still works without custom CSS
    pass

# =========================
# 3) Backend config
# =========================
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def call_backend(stress_series: np.ndarray, horizon: int):
    payload = {
        "features": stress_series.tolist(),
        "horizon": int(horizon)
    }
    try:
        resp = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if "forecast" in data and isinstance(data["forecast"], list):
            return data
        return None
    except Exception as e:
        st.sidebar.warning(f"Backend not reachable, using local forecast. ({e})")
        return None 

# =========================
# 4) Header (Fitbit style)
# =========================
st.markdown("""
<div class="app-header">
    <div class="app-title">Stress • Today</div>
    <div class="app-sub">Stress tracking & short-term forecast</div>
</div>
""", unsafe_allow_html=True)

# =========================
# 5) Sidebar controls
# =========================
st.sidebar.header("Controls")
source = st.sidebar.radio("Data source", ["Sample", "Upload CSV"], horizontal=True)
horizon = st.sidebar.slider("Forecast horizon (minutes)", 5, 60, 15, step=5)

# =========================
# 6) Data loading
# =========================
def load_sample(n: int = 300, seed: int = 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    stress = np.cumsum(rng.normal(0, 0.08, size=n)) + 0.5
    return pd.DataFrame({"t": t, "stress_level": stress})

if source == "Sample":
    df = load_sample()
else:
    up = st.sidebar.file_uploader(
        "Upload CSV (must contain an EDA-like column)",
        type="csv"
    )
    if up is None:
        st.info("Upload a CSV to continue, or switch to Sample.")
        st.stop()
    
    raw = pd.read_csv(up)
    
    stress_levels = []
    for i in range(len(raw)):
        row_features = raw.iloc[i].to_list()
        payload = {"features": row_features}
        try:
            resp = requests.post(f"{BACKEND_URL}/predict", json=payload)
            resp.raise_for_status()
            predicted_level = resp.json().get("predicted_level", 0)
        except Exception as e:
            st.warning(f"Backend prediction failed for row{i}, using 0. ({e})")
        stress_levels.append(predicted_level)

    # Try to guess EDA column
    #candidate_names = {"eda", "gsr", "electrodermal"}
    #eda_col = None
    df = pd.DataFrame({
        "t": np.arange(len(stress_levels)),
        "stress_level": stress_levels
    })

# Make sure we have enough points
if len(df) < 10:
    st.error("Need at least 10 EDA points to analyze.")
    st.stop()

# =========================
# 7) KPI cards
# =========================
col1, col2, col3 = st.columns(3)
current_stress = float(df["stress_level"].iloc[-1])

with col1:
    st.metric("Current Stress Level", f"{current_stress:.2f}")

if len(df) >=2:
    delta_1h = df["stress_level"].iloc[-1] - df["stress_level"].iloc[-2]
else:
    delta_1h = 0.0

with col2:
    st.metric("1-hour change (approx.)", f"{delta_1h:+.2f}")

lvl_raw = (current_stress - df["stress_level"].min()) / (df["stress_level"].max() - df["stress_level"].min() + 1e-6)
if lvl_raw < 0.33:
    baseline_level = "Low"
elif lvl_raw < 0.66:
    baseline_level = "Moderate"
else:
    baseline_level = "High"

with col3:
    st.metric("Baseline stress level", baseline_level)

# =========================
# 8) Local fallback forecast
# =========================
def simple_forecast(series: np.ndarray, horizon: int) -> np.ndarray:
    """
    Super simple baseline: linear trend over last 30 points.
    Used only if backend is unavailable.
    """
    last = float(series[-1])
    idx_start = max(len(series) - 30, 0)
    denom = max(min(30, len(series) - 1), 1)
    trend = (series[-1] - series[idx_start]) / denom
    return last + np.linspace(0, trend * 0.8, horizon)

# =========================
# 9) Call backend (or fallback)
# =========================
stress_series = df["stress_level"].to_numpy()
backend_result = call_backend(stress_series, horizon)

if backend_result is not None:
    forecast_vals = np.array(backend_result.get("forecast", []), dtype=float)
    level = backend_result.get("level", baseline_level)
    prob = float(backend_result.get("probability", 0.0))
    msg = backend_result.get("message", "").strip()
else:
    forecast_vals = simple_forecast(stress_series, horizon)
    level = baseline_level
    prob = 0.0
    msg = "Local baseline forecast (backend offline)."

future_t = np.arange(df["t"].iloc[-1] + 1, df["t"].iloc[-1] + 1 + len(forecast_vals))

# =========================
# 10) Charts row
# =========================
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Stress history")
    st.line_chart(df, x="t", y="stress_level", height=280)

with c2:
    st.subheader("Forecast")
    forecast_df = pd.DataFrame({"t": future_t, "Forecast stress": forecast_vals})
    st.line_chart(forecast_df, x="t", y="Forecast stress", height=280)
    st.markdown("---")
    st.markdown(f"**Model stress level:** {level}")
    if backend_result is not None:
        st.markdown(f"**Predicted stress risk:** {prob * 100:.0f}%")
    if msg:
        st.caption(msg)

# =========================
# 11) Footer
# =========================
st.markdown(
    '<div class="app-footer">Stress Forecast Prototype • Frontend (Streamlit) + Backend (FastAPI)</div>',
    unsafe_allow_html=True
)
