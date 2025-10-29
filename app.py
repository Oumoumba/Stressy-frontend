import streamlit as st
import pandas as pd
import numpy as np

# 1) MUST be first Streamlit call
st.set_page_config(page_title="Stress Forecast", page_icon="🫀", layout="wide")

# 2) Theme + CSS
try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# 3) Top header (Fitbit-like)
st.markdown("""
<div class="app-header">
  <div class="app-title">Stress • Today</div>
  <div class="app-sub">EDA tracking & short-term forecast</div>
</div>
""", unsafe_allow_html=True)

# 4) Sidebar controls (minimal for now)
st.sidebar.header("Controls")
source = st.sidebar.radio("Data", ["Sample", "Upload CSV"], horizontal=True)
horizon = st.sidebar.slider("Forecast horizon (min)", 5, 60, 15, step=5)

# 5) Load data (simple placeholder)
def load_sample(n=300, seed=1):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    eda = np.cumsum(rng.normal(0, 0.08, size=n)) + 0.5
    return pd.DataFrame({"t": t, "EDA": eda})

if source == "Sample":
    df = load_sample()
else:
    up = st.sidebar.file_uploader("Upload CSV (needs an 'EDA' column)", type="csv")
    if up is None:
        st.info("Upload a CSV to continue, or switch to Sample.")
        st.stop()
    raw = pd.read_csv(up)
    eda_col = next((c for c in raw.columns if c.lower().strip() in {"eda","gsr","electrodermal"}), raw.columns[0])
    df = pd.DataFrame({"t": np.arange(len(raw[eda_col])), "EDA": raw[eda_col].astype(float)})

# 6) KPI cards row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current EDA", f"{df['EDA'].iloc[-1]:.2f}")
with col2:
    delta = df["EDA"].iloc[-1] - df["EDA"].iloc[-60] if len(df) > 60 else 0
    st.metric("1-hr change", f"{delta:+.2f}")
with col3:
    lvl_raw = (df["EDA"].iloc[-1] - df["EDA"].min()) / (df["EDA"].max() - df["EDA"].min() + 1e-6)
    lvl = "Low" if lvl_raw < 0.33 else "Moderate" if lvl_raw < 0.66 else "High"
    st.metric("Stress level", lvl)

# 7) Charts row
c1, c2 = st.columns((2,1))
with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("EDA history")
    st.line_chart(df, x="t", y="EDA", height=280)
    st.markdown('</div>', unsafe_allow_html=True)
    st.subheader("EDA history")
    st.line_chart(df, x="t", y="EDA", height=280)

def simple_forecast(series: np.ndarray, horizon: int):
    last = float(series[-1])
    trend = (series[-1] - series[max(len(series)-30,0)]) / max(min(30, len(series)-1), 1)
    return last + np.linspace(0, trend*0.8, horizon)

pred = simple_forecast(df["EDA"].to_numpy(), horizon)
future_t = np.arange(df["t"].iloc[-1]+1, df["t"].iloc[-1]+1+horizon)
with c2:
    st.subheader("Forecast")
    st.line_chart(pd.DataFrame({"t": future_t, "Forecast": pred}), x="t", y="Forecast", height=280)

# 8) Footer
st.markdown('<div class="app-footer">Prototype • v0.1</div>', unsafe_allow_html=True)
st.markdown("""
<div class="top-nav">
  <div class="logo">🫀 Stress Forecast</div>
  <div class="nav-links">
    <a href="#">Home</a>
    <a href="#">Trends</a>
    <a href="#">Settings</a>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="footer">Prototype v0.2 • Built by Oumou</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Prototype v0.2 • Built by Oumou</div>', unsafe_allow_html=True)

