from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Stress Forecast Backend")


class StressRequest(BaseModel):
    eda: list[float]
    horizon: int = 15


class StressResponse(BaseModel):
    forecast: list[float]
    mean_prob: float
    label: str


@app.get("/")
def root():
    return {"status": "ok", "message": "stress backend alive"}


@app.post("/predict", response_model=StressResponse)
def predict(req: StressRequest):
    arr = np.array(req.eda, dtype=float)

    # simple trend-based toy model
    last = float(arr[-1])
    idx0 = max(len(arr) - 30, 0)
    trend = (arr[-1] - arr[idx0]) / max(min(30, len(arr) - 1), 1)

    steps = np.linspace(0, trend * 0.8, req.horizon)
    forecast = (last + steps).tolist()

    # normalize for "stress level"
    norm = float((last - arr.min()) / (arr.max() - arr.min() + 1e-6))
    if norm < 0.33:
        label = "low"
    elif norm < 0.66:
        label = "medium"
    else:
        label = "high"

    return StressResponse(
        forecast=forecast,
        mean_prob=norm,
        label=label,
    )
