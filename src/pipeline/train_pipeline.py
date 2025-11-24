from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import pickle

from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.pipeline.train_pipeline import TrainPipeline


# Create Flask App
application = Flask(__name__)
app = application


# ============================
# HOME PAGE
# ============================
@app.route("/")
def home_page():
    return render_template("index.html")


# ============================
# PREDICTION ROUTE
# ============================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get data from form
        data = CustomData(
            age=float(request.form["age"]),
            sex=float(request.form["sex"]),
            cp=float(request.form["cp"]),
            trestbps=float(request.form["trestbps"]),
            chol=float(request.form["chol"]),
            fbs=float(request.form["fbs"]),
            restecg=float(request.form["restecg"]),
            thalach=float(request.form["thalach"]),
            exang=float(request.form["exang"]),
            oldpeak=float(request.form["oldpeak"]),
            slope=float(request.form["slope"]),
            ca=float(request.form["ca"]),
            thal=float(request.form["thal"]),
        )

        # Convert to DataFrame
        final_input = data.get_data_as_dataframe()

        # Predict using pipeline
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_input)[0]

        # Convert output
        result = "Heart Disease Detected" if pred == 1 else "No Heart Disease"

        return render_template("index.html", prediction_text=result)

    except Exception as e:
        return str(e)


# ============================
# TRAIN MODEL ROUTE
# ============================
@app.route("/train", methods=["GET"])
def train_model():
    try:
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
        return "Training Completed Successfully!"
    except Exception as e:
        return f"Training Failed: {str(e)}"


# ============================
# RUN FLASK APP
# ============================
if __name__ == "__main__":
    app.run(debug=True)
