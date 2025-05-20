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
from datetime import datetime

# URLs of the two phones (update with your IP Webcam URLs)
STREAM_URL_1 = "http://192.168.1.19:8080/video"
STREAM_URL_2 = "http://192.168.1.115:8080/video"
FRAME_WIDTH = 1080
FRAME_HEIGHT = 1080
FPS = 30

def record_two_phone_streams():
    cap1 = cv2.VideoCapture(STREAM_URL_1)
    cap2 = cv2.VideoCapture(STREAM_URL_2)
    if not cap1.isOpened() or not cap2.isOpened():
        print("Error: Could not open one or both streams")
        return

    window1 = "Phone 1"
    window2 = "Phone 2"
    cv2.namedWindow(window1)
    cv2.namedWindow(window2)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out1 = None
    out2 = None
    recording = False

    print("Press 's' to start recording both, 'q' to quit and save.")

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if not ret1 or not ret2:
            print("Error: Failed to capture one or both streams")
            break

        frame1 = cv2.resize(frame1, (FRAME_WIDTH, FRAME_HEIGHT))
        frame2 = cv2.resize(frame2, (FRAME_WIDTH, FRAME_HEIGHT))
        cv2.imshow(window1, frame1)
        cv2.imshow(window2, frame2)

        if recording:
            out1.write(frame1)
            out2.write(frame2)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and not recording:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            out1 = cv2.VideoWriter(f"VIDEO1_{FPS}_{timestamp}.mp4", fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
            out2 = cv2.VideoWriter(f"VIDEO2_{FPS}_{timestamp}.mp4", fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
            recording = True
            print("Started recording both streams")
        elif key == ord('q'):
            print("Stopping recording")
            break

    if recording:
        out1.release()
        out2.release()
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_two_phone_streams()