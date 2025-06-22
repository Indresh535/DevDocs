import cv2
import mediapipe as mp
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
DATA_DIR = "data"

actions = ["walk", "run", "jump", "dance"]
X = []
y = []

def extract_keypoints(results):
    keypoints = []
    if results.pose_landmarks:
        for lm in results.pose_landmarks.landmark:
            keypoints.extend([lm.x, lm.y, lm.z])
    return keypoints if keypoints else [0]*99

# Loop over each action's video
for action in actions:
    cap = cv2.VideoCapture(f"{action}.mp4")
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

# Train model
print("Training model...")
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)
joblib.dump(model, "action_model.pkl")
print("Model saved as action_model.pkl")
