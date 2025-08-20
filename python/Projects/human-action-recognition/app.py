import os
import cv2
import joblib
import numpy as np
from flask import Flask, render_template, request
from train_model import train_model
from action_recognition import process_video
import mediapipe as mp
import psutil


app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
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

    return render_template("index.html", prediction_knn=prediction_knn,
                           prediction_svm=prediction_svm,
                           comparison_result=comparison_result,
                           metrics=metrics)

if __name__ == "__main__":
    app.run(debug=True)




# import os
# import cv2
# import joblib
# import numpy as np
# from flask import Flask, render_template, request
# from utils import extract_keypoints
# from train_model import train_model
# import mediapipe as mp

# app = Flask(__name__)
# UPLOAD_FOLDER = "static"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# @app.route("/", methods=["GET", "POST"])
# def index():
#     prediction_knn = None
#     prediction_svm = None
#     comparison_result = None

#     # Train both models
#     train_model()

#     if request.method == "POST":
#         file = request.files["video"]
#         if file:
#             video_path = os.path.join(app.config["UPLOAD_FOLDER"], "input.mp4")
#             output_path = os.path.join(app.config["UPLOAD_FOLDER"], "output.mp4")
#             file.save(video_path)

#             # Load models
#             knn_model, le = joblib.load("model_knn.pkl")
#             svm_model, _ = joblib.load("model_svm.pkl")

#             # Setup MediaPipe
#             mp_pose = mp.solutions.pose
#             pose = mp_pose.Pose()
#             drawing = mp.solutions.drawing_utils

#             cap = cv2.VideoCapture(video_path)
#             width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#             height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#             fps = cap.get(cv2.CAP_PROP_FPS)

#             out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
#             predictions_knn = []
#             predictions_svm = []

#             while cap.isOpened():
#                 ret, frame = cap.read()
#                 if not ret:
#                     break

#                 image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 results = pose.process(image)
#                 keypoints = extract_keypoints(results)
#                 X = np.array(keypoints).reshape(1, -1)

#                 action_knn = le.inverse_transform(knn_model.predict(X))[0]
#                 action_svm = le.inverse_transform(svm_model.predict(X))[0]

#                 predictions_knn.append(action_knn)
#                 predictions_svm.append(action_svm)

#                 # Annotate
#                 cv2.putText(frame, f"KNN: {action_knn}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#                 cv2.putText(frame, f"SVM: {action_svm}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
#                 drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
#                 out.write(frame)

#             cap.release()
#             out.release()

#             # Majority prediction
#             prediction_knn = max(set(predictions_knn), key=predictions_knn.count)
#             prediction_svm = max(set(predictions_svm), key=predictions_svm.count)

#             comparison_result = "Match ✅" if prediction_knn == prediction_svm else "Mismatch ❌"

#     return render_template("index.html", prediction_knn=prediction_knn,
#                            prediction_svm=prediction_svm,
#                            comparison_result=comparison_result)


# if __name__ == "__main__":
#     app.run(debug=True)

