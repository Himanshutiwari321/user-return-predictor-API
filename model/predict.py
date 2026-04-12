import pickle
import pandas as pd
from utils.transforms import IQRCapper

with open("model/return_model.pkl", "rb") as f:
    artifacts = pickle.load(f)

model = artifacts["model"]
threshold = artifacts["threshold"]
features = artifacts["features"]

MODEL_VERSION = "1.0.0"

label_map = {
    0: "User Will Not Return",
    1: "User Will Return"
}

def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])[features]

    probabilities = model.predict_proba(df)[0]

    class_1_index = list(model.classes_).index(1)
    positive_prob = probabilities[class_1_index]


    pred = 1 if positive_prob >= threshold else 0

    confidence = max(probabilities)

    class_probs = {
        label_map[int(cls)]: round(float(prob), 4)
        for cls, prob in zip(model.classes_, probabilities)
    }

    return {
        "prediction": label_map[pred],
        "confidence": round(float(confidence), 4),
        "probability_return": round(float(positive_prob), 4),
        "threshold": threshold,
        "class_probabilities": class_probs,
    }


# Testing
print(features)

sample_input = {
    "Page Views": 8,
    "Session Duration": 3.629279,
    "Traffic Source": "Paid",
    "Time on Page": 2.071925,
    "Previous Visits": 0
}

result = predict_output(sample_input)
print(result)




	