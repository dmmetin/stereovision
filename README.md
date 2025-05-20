# Dance3D-Triangulation

A project to capture dance movements in 3D using stereo vision with IP Webcam and Mediapipe. This repository contains scripts to record synchronized video streams from two phones and triangulate 2D landmarks into 3D positions.

## Project Overview

This project aims to capture and analyze dance movements in 3D using stereo vision. It leverages IP Webcam for video capture and Mediapipe for pose estimation. The process involves:  
1. Recording two synchronized video streams from two phones using IP Webcam.  
2. Extracting 2D landmarks from each video using Mediapipe Pose.  
3. Triangulating the 2D landmarks to reconstruct 3D positions frame by frame.  

This is a first approximation of stereo triangulation, with simplified calibration (assumes parallel camera axes). Future improvements will include precise calibration and additional visualization steps.

## Repository Structure

- `record_two_phone_streams.py`: Records synchronized video streams from two phones using IP Webcam.  
- `triangulate_mediapipe.py`: Extracts 2D landmarks with Mediapipe and triangulates them into 3D positions, saving the result as a NumPy tensor.  
- `README.md`: Project documentation.  
- `LICENSE`: Apache 2.0 license file.  
- `.gitignore`: Ignores unnecessary files (e.g., videos, NumPy tensors).

## Requirements

- **Python 3.x**  
- **Dependencies**:
  ```
  pip install opencv-python mediapipe numpy
  ```
- **IP Webcam**: Install the IP Webcam app on two phones (available on Android/iOS).  
- **Hardware**: Two phones with IP Webcam, positioned 180 cm apart (baseline distance). Ensure both phones are on the same local network.

## Usage

### Step 1: Set Up IP Webcam for Video Capture
1. Install the IP Webcam app on both phones.
2. Launch the app on each phone and start the video server.
3. Note the URLs provided by the app (e.g., `http://192.168.1.19:8080/video` for Phone 1, `http://192.168.1.115:8080/video` for Phone 2).
4. Update the `STREAM_URL_1` and `STREAM_URL_2` variables in `record_two_phone_streams.py` with these URLs.

### Step 2: Record Synchronized Videos
Run the recording script:
```bash
python record_two_phone_streams.py
```
- Press `s` to start recording both streams.
- Press `q` to stop and save the videos.
- Output: Two MP4 files with timestamps (e.g., `VIDEO1_30_20250520030000.mp4` and `VIDEO2_30_20250520030000.mp4`).

**Tips for IP Webcam Setup**:
- Position the phones 180 cm apart to form the baseline for stereo vision.
- Ensure both phones are on the same Wi-Fi network for stable streaming.
- Place the phones on tripods for stability, and align them as parallel as possible to simplify triangulation.

### Step 3: Triangulate Landmarks to 3D
Run the triangulation script:
```bash
python triangulate_mediapipe.py
```
- The script processes the two recorded videos, extracts 2D landmarks using Mediapipe Pose, and triangulates them into 3D positions.
- Output: A NumPy tensor (`mediapipe_landmarks_3d.npz`) containing the 3D coordinates for each frame.

**Note on Triangulation**:
- This is a first approximation with simplified calibration (focal length `f=1000` pixels, baseline `180 cm`, assumed parallel axes).
- For precise 3D measurements, calibrate the focal length and baseline in consistent units (e.g., both in mm), and account for camera rotation if the setup is not perfectly parallel.

## Future Work
- Next post on X this weekend: Setup with Korg Volca FM and Ableton for creating original electro-funk soundtracks for dance clips.
- Future improvements: Precise camera calibration, integration of biological concepts (e.g., DNA-inspired geometries, dipole moments), and advanced 3D visualization.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

### Copyright
© 2025 David Marc Métin. All rights reserved.

### Underlying Licenses
This project uses the following libraries, which have their own licenses:  
- **OpenCV**: Apache 2.0 License  
- **Mediapipe**: Apache 2.0 License  
- **NumPy**: BSD 3-Clause License  

## Acknowledgments
Inspired by discussions with Grok (xAI).