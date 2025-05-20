# Copyright 2025 David Marc Métin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import mediapipe as mp
import numpy as np
import os

VIDEO_PATHS = [
    r"C:\BRAIN\DANSE\KORG_CHORE_triangulation\STREAM_URL_1_Mediapipe\mediapipe_STREAM1.mp4",
    r"C:\BRAIN\DANSE\KORG_CHORE_triangulation\STREAM_URL_2_Mediapipe\mediapipe_STREAM2.mp4"
]
OUTPUT_PATH = r"C:\BRAIN\DANSE\KORG_CHORE_triangulation"
os.makedirs(OUTPUT_PATH, exist_ok=True)

mp_pose = mp.solutions.pose

def extract_landmarks(video_path):
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
    all_landmarks = []
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        if results.pose_landmarks:
            landmarks = np.array([[lm.x * width, lm.y * height, lm.z * width, lm.visibility] for lm in results.pose_landmarks.landmark])
        else:
            landmarks = np.zeros((33, 4))
        all_landmarks.append(landmarks)
    cap.release()
    pose.close()
    return np.array(all_landmarks), width, height

def triangulate_points(pts1, pts2, P1, P2):
    # pts1, pts2: (33, 2) arrays
    points_3d = []
    for i in range(33):
        p1 = np.array([[pts1[i, 0]], [pts1[i, 1]]])
        p2 = np.array([[pts2[i, 0]], [pts2[i, 1]]])
        point_4d = cv2.triangulatePoints(P1, P2, p1, p2)
        point_3d = point_4d[:3, 0] / point_4d[3, 0]
        points_3d.append(np.round(point_3d).astype(int))
    return np.array(points_3d)

if __name__ == "__main__":
    # 1. Extraction des landmarks pour chaque vidéo
    lm1, width, height = extract_landmarks(VIDEO_PATHS[0])
    lm2, _, _ = extract_landmarks(VIDEO_PATHS[1])
    frames = min(lm1.shape[0], lm2.shape[0])

    # 2. Définition des matrices de projection (à adapter selon ta géométrie réelle)
    f = 1000  # focale en pixels (à calibrer)
    cx, cy = width // 2, height // 2
    baseline = 180  # distance entre caméras en cm (adapter si besoin)
    P1 = np.array([[f, 0, cx, 0],
                   [0, f, cy, 0],
                   [0, 0, 1, 0]], dtype=np.float64)
    P2 = np.array([[f, 0, cx, -f * baseline],
                   [0, f, cy, 0],
                   [0, 0, 1, 0]], dtype=np.float64)

    # 3. Triangulation frame par frame
    points_3d = []
    for i in range(frames):
        pts1 = lm1[i, :, :2]  # (33, 2)
        pts2 = lm2[i, :, :2]  # (33, 2)
        points_3d.append(triangulate_points(pts1, pts2, P1, P2))
    points_3d = np.array(points_3d)  # (frames, 33, 3)

    # 4. Sauvegarde du tenseur 3D
    np.savez(os.path.join(OUTPUT_PATH, "mediapipe_landmarks_3d.npz"), points_3d=points_3d)
    print(f"Tenseur 3D sauvegardé : shape {points_3d.shape}")