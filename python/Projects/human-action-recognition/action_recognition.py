import cv2
import mediapipe as mp
import numpy as np
import joblib
import time
from utils import extract_keypoints


# Initialize MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Load models
knn_model, le = joblib.load("model_knn.pkl")
svm_model, _ = joblib.load("model_svm.pkl")

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    predictions_knn = []
    predictions_svm = []
    knn_times = []
    svm_times = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        keypoints = extract_keypoints(results)
        X = np.array(keypoints).reshape(1, -1)

        # KNN prediction
        start_time = time.time()
        action_knn = le.inverse_transform(knn_model.predict(X))[0]
        knn_times.append(time.time() - start_time)
        predictions_knn.append(action_knn)

        # SVM prediction
        start_time = time.time()
        action_svm = le.inverse_transform(svm_model.predict(X))[0]
        svm_times.append(time.time() - start_time)
        predictions_svm.append(action_svm)

        # Annotate
        cv2.putText(frame, f"KNN: {action_knn}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"SVM: {action_svm}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        out.write(frame)

    cap.release()
    out.release()

    # Calculate average prediction times
    avg_knn_time = sum(knn_times) / len(knn_times) if knn_times else 0
    avg_svm_time = sum(svm_times) / len(svm_times) if svm_times else 0

    return {
        'prediction_knn': max(set(predictions_knn), key=predictions_knn.count),
        'prediction_svm': max(set(predictions_svm), key=predictions_svm.count),
        'knn_prediction_time': round(avg_knn_time, 4),
        'svm_prediction_time': round(avg_svm_time, 4)
    }