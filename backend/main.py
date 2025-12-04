from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Stress Forecast Backend")
model = joblib.load("best_stress_model.pkl")
scaler = joblib.load("scaler.pkl")

class StressRequest(BaseModel):
    features: list[float]


class StressResponse(BaseModel):
    predicted_level: int
    


@app.get("/")
def root():
    return {"status": "ok", "message": "stress backend alive"}


@app.post("/predict", response_model=StressResponse)
def predict(req: StressRequest):
    features = np.array(req.features).reshape(1, -1)

    main_features = features[:, :8]
    missing_features = features[:, 8:]

    main_features_scaled = scaler.transform(main_features)

    input_features = np.hstack([main_features_scaled, missing_features])

    print("Number of features:", input_features.shape[1])
    predicted_level = int(model.predict(input_features)[0])
    
    # Return only the predicted stress level
    return StressResponse(predicted_level=predicted_level)
