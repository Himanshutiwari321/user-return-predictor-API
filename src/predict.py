import sys
import pickle
import pandas as pd
from src.transforms import IQRCapper
import src.transforms
sys.modules['src.transforms'] = src.transforms 

with open("src/return_model.pkl", "rb") as f:
    artifacts = pickle.load(f)

model = artifacts["model"]
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

    pred = model.predict(df)[0]
      
    confidence = max(probabilities)

    class_probs = {
        label_map[int(cls)]: round(float(prob), 4)
        for cls, prob in zip(model.classes_, probabilities)
    }

    return {
        "prediction": label_map[pred],
        "confidence": round(float(confidence), 4),
        "probability_return": round(float(positive_prob), 4),
        "class_probabilities": class_probs,
    }







	