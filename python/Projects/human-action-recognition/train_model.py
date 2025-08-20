import os
import cv2
import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from utils import extract_keypoints
import mediapipe as mp
import time
import psutil

def train_model(data_dir='data/train', actions=["walk", "run", "jump", "dance"]):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    X, y = [], []
    for action in actions:
        video_path = os.path.join(data_dir, f"{action}.mp4")
        if not os.path.exists(video_path):
            print(f"Video {video_path} not found.")
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
    knn_cpu_usage = psutil.cpu_percent(interval=1)

    # Train SVM
    start_time = time.time()
    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(X_train, y_train)
    svm_training_time = time.time() - start_time
    svm_accuracy = svm_model.score(X_val, y_val) * 100
    svm_cpu_usage = psutil.cpu_percent(interval=1)

    # Save models and label encoder
    joblib.dump((knn_model, le), "model_knn.pkl")
    joblib.dump((svm_model, le), "model_svm.pkl")

    metrics = {
        'knn': {'accuracy': round(knn_accuracy, 2), 'training_time': round(knn_training_time, 2), 'cpu_usage': knn_cpu_usage},
        'svm': {'accuracy': round(svm_accuracy, 2), 'training_time': round(svm_training_time, 2), 'cpu_usage': svm_cpu_usage}
    }

    return metrics

# import cv2
# import mediapipe as mp
# import numpy as np
# import os
# from sklearn.neighbors import KNeighborsClassifier
# import joblib

# # Setup
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()
# DATA_DIR = "data"

# actions = ["walk", "run", "jump", "dance"]
# X = []
# y = []

# def extract_keypoints(results):
#     keypoints = []
#     if results.pose_landmarks:
#         for lm in results.pose_landmarks.landmark:
#             keypoints.extend([lm.x, lm.y, lm.z])
#     return keypoints if keypoints else [0]*99

# # Loop over each action's video
# for action in actions:
#     cap = cv2.VideoCapture(f"{action}.mp4")
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(image)
#         keypoints = extract_keypoints(results)
#         X.append(keypoints)
#         y.append(action)
#     cap.release()

# # Train model
# print("Training model...")
# model = KNeighborsClassifier(n_neighbors=3)
# model.fit(X, y)
# joblib.dump(model, "action_model.pkl")
# print("Model saved as action_model.pkl")
