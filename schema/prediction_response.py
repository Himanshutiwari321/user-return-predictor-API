from pydantic import BaseModel

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probability_return: float
    threshold: float
    class_probabilities: dict