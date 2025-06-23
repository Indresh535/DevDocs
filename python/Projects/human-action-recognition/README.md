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
pip install opencv-python mediapipe scikit-learn numpy joblib
