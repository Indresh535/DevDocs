import os
import cv2
import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import mediapipe as mp
import time
import psutil
import json
from utils import extract_keypoints


def load_metrics_from_file():
    """Load previously saved model metrics if available."""
    if os.path.exists("model_metrics.json"):
        with open("model_metrics.json", "r") as f:
            return json.load(f)
    else:
        print("Metrics file not found. Please delete model files to retrain.")
        return None


def train_model(data_dir='data/train', actions=["walk", "run", "jump", "dance"], force_retrain=False):
    """Train KNN and SVM models on the given dataset, or load if already trained."""
    
    # Skip training if models already exist and retraining is not forced
    if not force_retrain and os.path.exists("model_knn.pkl") and os.path.exists("model_svm.pkl"):
        print("Models already trained. Skipping training.")
        metrics = load_metrics_from_file()
        if metrics is None:
            raise ValueError("Model files exist but metrics are missing. Please delete model files to retrain.")
        return metrics

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    X, y = [], []
    for action in actions:
        video_path = os.path.join(data_dir, f"{action}.mp4")
        if not os.path.exists(video_path):
            print(f"Video {video_path} not found. Skipping.")
            continue

        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            keypoints = extract_keypoints(results)
            X.append(keypoints)
            y.append(action)

        cap.release()

    if not X:
        return "No data available for training."

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Train KNN
    start_time = time.time()
    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(X_train, y_train)
    knn_training_time = time.time() - start_time
    knn_accuracy = knn_model.score(X_val, y_val) * 100
    proc = psutil.Process(os.getpid())
    knn_cpu_usage = proc.cpu_percent(interval=1)

    # Train SVM
    start_time = time.time()
    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(X_train, y_train)
    svm_training_time = time.time() - start_time
    svm_accuracy = svm_model.score(X_val, y_val) * 100
    proc = psutil.Process(os.getpid())
    svm_cpu_usage = proc.cpu_percent(interval=1)

    # Save models and label encoder
    joblib.dump((knn_model, le), "model_knn.pkl")
    joblib.dump((svm_model, le), "model_svm.pkl")

    # Save metrics
    metrics = {
        'knn': {
            'accuracy': round(knn_accuracy, 2),
            'training_time': round(knn_training_time, 2),
            'cpu_usage': knn_cpu_usage
        },
        'svm': {
            'accuracy': round(svm_accuracy, 2),
            'training_time': round(svm_training_time, 2),
            'cpu_usage': svm_cpu_usage
        }
    }

    with open("model_metrics.json", "w") as f:
        json.dump(metrics, f)

    print("Training complete. Models and metrics saved.")
    return metrics
