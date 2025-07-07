import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def extract_keypoints(results):
    keypoints = []
    if results.pose_landmarks:
        for lm in results.pose_landmarks.landmark:
            keypoints.extend([lm.x, lm.y, lm.z])
    while len(keypoints) < 99:
        keypoints.append(0.0)
    return keypoints
