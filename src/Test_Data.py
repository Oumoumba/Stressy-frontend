import joblib
import numpy as np

# Load the trained model
model = joblib.load('best_stress_model.pkl')
scaler = joblib.load('scaler.pkl')
# Get input data from command line arguments
input_data = {
    'snoring range': 85.76,
    'respiration rate': 23.54,
    'body temperature': 90.77,
    'limb movement': 13.92,
    'blood oxygen': 88.77,
    'eye movement': 96.92,
    'hours of sleep': 0.77,
    'heart rate': 68.84,
    
    'body temperature_missing': 0,
    'limb movement_missing': 0,
    'blood oxygen_missing': 0,
    'eye movement_missing': 0,
    'hours of sleep_missing': 0,
    'heart rate_missing': 0
}

# Prepare input features based on the expected order (14 features in total)
features = np.array([[input_data['snoring range'],
                      input_data['respiration rate'],
                      input_data['body temperature'],
                      input_data['limb movement'],
                      input_data['blood oxygen'],
                      input_data['eye movement'],
                      input_data['hours of sleep'],
                      input_data['heart rate'],
                     ]])
missing_features = np.array([[input_data['body temperature_missing'],
                              input_data['limb movement_missing'],
                              input_data['blood oxygen_missing'],
                              input_data['eye movement_missing'],
                              input_data['hours of sleep_missing'],
                              input_data['heart rate_missing']]])
features = scaler.transform(features)
fFeatures = np.concatenate([features, missing_features], axis=1)
# Make prediction
prediction = model.predict(fFeatures)

# Output the prediction
print("Predicted Stress Level:", prediction[0])
