# Human Action Recognition 🕺🤖

This project recognizes simple human actions — **walking**, **running**, **jumping**, and **dancing** — from video input using MediaPipe for pose estimation and a machine learning model (KNN classifier) trained on pose landmarks.

---

## 📦 Features

- Pose landmark extraction using **MediaPipe**
- Real-time or video-based action classification
- Predefined actions: `walk`, `run`, `jump`, `dance`
- Easily extendable with your own videos and labels

---

## 🧰 Requirements

Install dependencies with pip:

```bash
requirements insallation python version 3.12.4

python -m venv venv

venv\Scripts\activate     

pip install flask opencv-python mediapipe scikit-learn joblib numpy

pip install -r requirements.txt

python app.py

deactivate 



🕺 Human Action Recognition with KNN & SVM 🧠
This project uses MediaPipe for pose estimation and compares two machine learning algorithms — K-Nearest Neighbors (KNN) and Support Vector Machine (SVM) — to recognize human actions like:

🏃‍♂️ Run

🚶‍♀️ Walk

🕴️ Jump

💃 Dance

It provides:

Action prediction from uploaded videos

Side-by-side comparison of KNN and SVM

Visualized performance metrics (accuracy, training time, CPU usage, etc.)

Output video with real-time annotated predictions

🔥 Features
✅ Human pose extraction using MediaPipe
✅ KNN & SVM model training
✅ Upload videos for inference
✅ Output video with predicted action overlay
✅ Side-by-side algorithm comparison:
  • Accuracy
  • Training & inference time
  • CPU usage
  • Training loss (SVM)
✅ Performance bar chart via Chart.js

🧠 Algorithms Used
Metric	KNN	SVM
Model Type	Lazy learner	Margin-based classifier
Suitable For	Simple, low-dim problems	High-dimensional data
Real-Time Performance	Fast	Slower
Accuracy	✅ Depends on k, distance	✅ Generally better
