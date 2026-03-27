 Hand Tracking Painter

A real-time hand tracking application built using **Python, OpenCV, MediaPipe, and cvzone**.  
This project allows you to draw on the screen using hand gestures captured through your webcam.

---

## Features

- 🎯 Real-time hand tracking  
- ✌️ Gesture recognition  
- ✍️ Draw using index finger  
- 🎨 Multiple colors (Blue, Green, Red)  
- 🧽 Eraser tool  
- 🗑 Clear canvas  
- 📷 Webcam-based interaction  

---

## How It Works

- **Index finger up** → Drawing mode  
- **Index + middle finger up** → Selection mode  
- Select tools from the top menu:
  - Colors
  - Eraser
  - Clear screen  

---

## Tech Stack

- Python  
- OpenCV  
- MediaPipe  
- cvzone  

---

## Installation

Install required libraries:

```bash
pip install opencv-python cvzone mediapipe numpy
```
## How to Run
```bash
python hand_tracking_painter.py
```
## Notes
- Make sure your webcam is working
- Lighting should be good for better hand detection
- Press ESC to exit
