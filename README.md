# 🎥 Live ASCII Camera Engine (GUI)

A high-performance, real-time Desktop Application that captures live webcam feeds and renders them into TrueColor ASCII art. Built with **Python**, **OpenCV**, and **Tkinter**, this project demonstrates real-time video processing, hardware integration, and matrix manipulation.

## 🚀 Engineering Highlights

- **Real-Time Video Processing:** Captures and processes webcam frames continuously with near-zero latency using OpenCV.
- **Dynamic ASCII Rendering:** Uses an optimized 70-character density ramp and the ITU-R 601 Luma transform formula (`0.299R + 0.587G + 0.114B`) for accurate grayscale mapping.
- **Custom Tkinter GUI:** A dark-themed, widescreen dashboard displaying the standard camera feed side-by-side with the live ASCII matrix in `640x480` resolution.
- **Matrix Math Optimization:** Utilizes `numpy` arrays for fast pixel manipulation and color space conversions (BGR to RGB).

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Arda-dd/ascii-vision-gui.git](https://github.com/Arda-dd/ascii-vision-gui.git)
   cd ascii-vision-gui
Install the required dependencies:

Bash
pip install -r requirements.txt
💻 Usage
Run the graphical interface with the following command:

Bash
python gui_camera.py
Controls:
Click ▶ Start Feed to initialize the camera and fire up the ASCII rendering engine.

Click ⏹ Stop Feed to safely halt the video stream and release hardware resources.

📐 Technical Architecture
Hardware Interfacing: cv2.VideoCapture(0) pulls raw frames directly from the local webcam.

Downsampling: The frame is resized to fit a custom character grid, reducing computational load and preventing UI stretching.

Quantization & Rendering: Pixels are mapped to an ASCII gradient based on perceptual luminance. The numpy engine draws these characters onto a blank canvas in their original RGB values.

GUI Loop: Tkinter's .after() method runs a non-blocking 30ms loop to update the UI with fresh frames.