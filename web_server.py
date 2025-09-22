from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import joblib
import mlflow.sklearn
import random

#http://localhost:1234/predict/?sepal_length=5.7&sepal_width=3.8&petal_length=1.7&petal_width=0.3

app = FastAPI()

#mlflow.set_tracking_uri("http://127.0.0.1:8080")
mlflow.set_tracking_uri("http://host.docker.internal:8080")


model_name = "tracking-quickstart"
current_version = "latest"
next_version = current_version

def load_model(version: str):
    model_uri = f"models:/{model_name}/{version}"
    return mlflow.sklearn.load_model(model_uri)

current_model = load_model(current_version)
next_model = current_model

class ml_response:
    def __init__(self, pred):
        self.y_pred = pred

@app.post("/test/")
def test():
    return {"response" :"connected"}

@app.post("/predict/")
async def predict(p: float = 0.8, sepal_length: float = 6.1, sepal_width: float = 2.8, petal_length: float = 4.7, petal_width: float = 1.2):
    X = [[sepal_length, sepal_width, petal_length, petal_width]]
    
    if random.random() < p:
        prediction = current_model.predict(X)
        model_used = "current"
    else:
        prediction = next_model.predict(X)
        model_used = "next"
    return {"y_pred": prediction.tolist(), "model_used": model_used}

@app.post("/update-model/")
async def update_model(version: str = "latest"):
    global next_model
    global next_version
    next_model = load_model(version)
    next_version = version
    return {"status": "next model updated", "status": f"current_version: {current_version}, next_version: {next_version}"}

@app.post("/accept-next-model/")
async def accept_next_model():
    global current_model
    global current_version
    current_model = next_model
    current_version = next_version
    return {"status": f"current_version: {current_version}, next_version: {next_version}"}