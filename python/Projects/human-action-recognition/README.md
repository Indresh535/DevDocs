# Human Action Recognition Project

## Overview
This project implements a **Human Action Recognition** system using two machine learning algorithms: **K-Nearest Neighbors (KNN)** and **Support Vector Machine (SVM)**. It processes video inputs to classify human actions such as walking, running, jumping, and dancing. The system uses a Flask-based web interface to upload videos, display predictions from both models, and compare their performance based on metrics like accuracy, training time, prediction time, and CPU usage. The project leverages **MediaPipe** for pose estimation and **scikit-learn** for machine learning.

## Features
- **Dual Algorithms**: Uses KNN and SVM for action classification, allowing comparison of their predictions.
- **Performance Metrics**:
  - **Accuracy**: Evaluated on a validation set.
  - **Training Time**: Time taken to train each model.
  - **Prediction Time**: Average time per frame for predictions.
  - **CPU Usage**: Monitored during training using `psutil`.
- **Web Interface**: A user-friendly Flask-based UI (`index.html`) to upload videos, view annotated output, and display model predictions and metrics.
- **Modular Design**: Code is organized into separate modules for training (`train_model.py`), video processing (`action_recognition.py`), and utilities (`utils.py`).

## Project Structure
```
project/
├── data/
│   └── train/
│       ├── walk.mp4
│       ├── run.mp4
│       ├── jump.mp4
│       ├── dance.mp4
├── static/
│   ├── input.mp4
│   ├── output.mp4
├── templates/
│   └── index.html
├── action_recognition.py
├── app.py
├── train_model.py
├── utils.py
├── requirements.txt
├── README.md
```

- **data/train/**: Contains training videos for each action (e.g., `walk.mp4`, `run.mp4`).
- **static/**: Stores input and output videos for the web interface.
- **templates/index.html**: Flask template for the web UI, displaying predictions and metrics.
- **action_recognition.py**: Processes videos and annotates frames with predictions from both models.
- **app.py**: Main Flask application to handle video uploads and render results.
- **train_model.py**: Trains KNN and SVM models, computes metrics, and saves models.
- **utils.py**: Utility functions for extracting keypoints using MediaPipe.
- **requirements.txt**: Lists required Python packages.
- **README.md**: This file, describing the project.

## Requirements
- Python 3.8+
- Packages listed in `requirements.txt`:
  - `opencv-python==4.11.0.86`
  - `mediapipe==0.10.21`
  - `scikit-learn==1.7.0`
  - `numpy==2.3.1`
  - `joblib==1.5.1`
  - `flask==3.0.3`
  - `psutil==6.1.0`

## Installation
1. **Clone the Repository** (if applicable) or create the project structure as shown above.
2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Prepare Training Data**:
   - Place training videos (`walk.mp4`, `run.mp4`, `jump.mp4`, `dance.mp4`) in the `data/train/` directory.
   - Ensure videos are in MP4 format and contain clear human actions for pose estimation.

## Usage
1. **Run the Application**:
   ```bash
   python app.py
   ```
2. **Access the Web Interface**:
   - Open `http://127.0.0.1:5000` in a web browser.
   - Upload a video file to classify the action.
   - View predictions from KNN and SVM, a comparison result (Match/Mismatch), and performance metrics.
   - Watch the annotated output video with pose landmarks and predictions.
3. **Deactivate Virtual Environment**:
   ```bash
   deactivate
   ```

## How It Works
1. **Training**:
   - `train_model.py` processes training videos in `data/train/` using MediaPipe to extract pose keypoints.
   - Keypoints are used to train KNN (`KNeighborsClassifier`) and SVM (`SVC` with linear kernel).
   - Models are saved as `model_knn.pkl` and `model_svm.pkl`.
   - Metrics (accuracy, training time, CPU usage) are computed during training.
2. **Prediction**:
   - `action_recognition.py` processes uploaded videos frame-by-frame, extracting keypoints and making predictions with both models.
   - Predictions are annotated on the output video (`static/output.mp4`).
   - Average prediction times are calculated for each model.
3. **Web Interface**:
   - `app.py` handles video uploads, triggers processing, and renders results in `index.html`.
   - The UI displays predictions, comparison results, and a metrics table.

## Performance Metrics
- **Accuracy**: Percentage of correct predictions on a 20% validation set.
- **Training Time**: Time (in seconds) to train each model.
- **Prediction Time**: Average time (in seconds) per frame for predictions.
- **CPU Usage**: Percentage CPU usage during training, measured via `psutil`.

## Notes
- **Training Loss**: KNN does not use a traditional loss function. For SVM, hinge loss could be added for deeper analysis (not implemented for simplicity).
- **Data Requirements**: Ensure sufficient and diverse training videos for robust model performance.
- **Performance Tuning**:
  - KNN: Adjust `n_neighbors` for better accuracy vs. speed.
  - SVM: Experiment with kernel types (e.g., `rbf`) or regularization parameter `C` for optimization.
- **Extensibility**: Add new actions by updating the `actions` list in `train_model.py` and providing corresponding training videos.
- **Limitations**:
  - SVM may be slower for large datasets due to its computational complexity.
  - MediaPipe pose estimation requires clear visibility of human subjects in videos.

## Future Improvements
- Add support for more actions or multi-person detection.
- Implement cross-validation for more robust accuracy metrics.
- Include real-time video processing via webcam.
- Enhance UI with visualizations (e.g., confusion matrix, prediction confidence).

## License
This project is for educational purposes and does not include a specific license. Ensure compliance with the licenses of dependencies (e.g., MediaPipe, scikit-learn).