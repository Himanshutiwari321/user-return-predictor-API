from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from src.predict import predict_output, artifacts, MODEL_VERSION 
app = FastAPI()

@app.get('/')
def home():
    return {'message': 'User Return Prediction API'}

@app.get('/health')
def health_check():
    return {
        'status': 'ok',
        'version': MODEL_VERSION,
        'model_loaded': artifacts is not None
    }

@app.post('/predict', response_model=PredictionResponse)
def predict_user_return(data: UserInput):
    user_input = {
        "Page Views": data.page_views,
        "Session Duration": data.session_duration,
        "Traffic Source": data.traffic_source,
        "Time on Page": data.time_on_page,
        "Previous Visits": data.previous_visits
    }
    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'response': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))