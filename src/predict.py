import os
import numpy as np
import pandas as pd
import requests

BACKEND_URL = os.getenv("BACKEND_URL")  # e.g., http://127.0.0.1:8000/predict

def _pick_eda(df: pd.DataFrame) -> pd.Series:
    for c in df.columns:
        if c.lower().strip() in {"eda", "gsr", "electrodermal"}:
            return pd.to_numeric(df[c], errors="coerce").dropna().astype(float)
    num = df.select_dtypes(include="number")
    if not num.empty:
        return num.iloc[:, 0].astype(float)
    return pd.Series([0.4, 0.42], dtype=float)

def simulate_prediction(df: pd.DataFrame, horizon: int = 15) -> dict:
    eda = _pick_eda(df)
    last = float(eda.iloc[-1])
    base = float(eda.tail(min(60, len(eda))).mean())
    prob = float(np.clip((last - base + 0.15) * 2.0, 0.0, 1.0))
    label = "low" if prob < 0.33 else ("medium" if prob < 0.66 else "high")
    start = max(0, len(eda) - 60)
    delta = (eda.iloc[-1] - eda.iloc[start]) / max(1, (len(eda) - 1) - start)
    forecast = last + np.linspace(0.0, float(delta), horizon)
    return {"prob": prob, "label": label, "forecast": forecast.tolist()}

def call_backend(df: pd.DataFrame, horizon: int = 15) -> dict:
    if BACKEND_URL:
        try:
            eda = _pick_eda(df).tolist()
            payload = {"eda": eda, "horizon": horizon}
            r = requests.post(BACKEND_URL, json=payload, timeout=8)
            r.raise_for_status()
            data = r.json()
            if {"prob", "label", "forecast"} <= set(data.keys()):
                return data
        except Exception:
            pass
    return simulate_prediction(df, horizon)
