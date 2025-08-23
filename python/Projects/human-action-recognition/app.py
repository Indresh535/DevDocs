import os
import cv2
import joblib
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from utils import extract_keypoints
from train_model import train_model
from action_recognition import process_video
import mediapipe as mp
import psutil
import time

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype='video/mp4')

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/recognize", methods=["GET", "POST"])
def recognize():
    prediction_knn = None
    prediction_svm = None
    comparison_result = None
    metrics = None

    # Train models
    train_metrics = train_model()

    if request.method == "POST":
        file = request.files["video"]
        if file:
            video_path = os.path.join(app.config["UPLOAD_FOLDER"], "input.mp4")
            output_path = os.path.join(app.config["UPLOAD_FOLDER"], "output.mp4")
            file.save(video_path)

            # Process video with both models
            results = process_video(video_path, output_path)

            prediction_knn = results['prediction_knn']
            prediction_svm = results['prediction_svm']
            comparison_result = "Match ✅" if prediction_knn == prediction_svm else "Mismatch ❌"

            # Combine training and prediction metrics
            metrics = {
                'knn': {
                    'accuracy': train_metrics['knn']['accuracy'],
                    'training_time': train_metrics['knn']['training_time'],
                    'prediction_time': results['knn_prediction_time'],
                    'cpu_usage': train_metrics['knn']['cpu_usage']
                },
                'svm': {
                    'accuracy': train_metrics['svm']['accuracy'],
                    'training_time': train_metrics['svm']['training_time'],
                    'prediction_time': results['svm_prediction_time'],
                    'cpu_usage': train_metrics['svm']['cpu_usage']
                }
            }

    return render_template("predict.html", prediction_knn=prediction_knn,
                           prediction_svm=prediction_svm,
                           comparison_result=comparison_result,
                           metrics=metrics,
                           time=int(time.time()))

if __name__ == "__main__":
    app.run(debug=True)