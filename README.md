# Telekinetic Volume Control

This is a MediaPipe pipeline for controlling the computer volume using hand gestures. The pipeline uses a webcam or video file as input, detects the hand and fingers in the image, and maps the finger movements to volume adjustments on the computer.

## Requirements

- MediaPipe
- A webcam or video file for input
- A computer running a supported operating system (Windows, Mac, Linux)

## Usage

1. Install MediaPipe following the instructions on the [MediaPipe website](https://mediapipe.readthedocs.io/en/latest/install.html).

2. Clone this repository and navigate to the home directory.

3. Run the pipeline using the following command:
```bash
python volumeControl.py
