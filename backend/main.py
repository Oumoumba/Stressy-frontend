from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Stress Forecast Backend")
model = joblib.load("best_stress_model.pkl")

class StressRequest(BaseModel):
    features: list[float]


class StressResponse(BaseModel):
    predicted_level: int
    


@app.get("/")
def root():
    return {"status": "ok", "message": "stress backend alive"}


@app.post("/predict", response_model=StressResponse)
def predict(req: StressRequest):
    predicted_level = int(model.predict([req.features])[0])
    
    # Return only the predicted stress level
    return StressResponse(predicted_level=predicted_level)
