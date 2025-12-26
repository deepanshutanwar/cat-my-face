# Cat My Face 😸

**Cat My Face** is a fun and technically rich **real-time face detection and AR overlay project** using a **Raspberry Pi and Pi Camera Module**.  
Human faces are detected using OpenCV Haar Cascades, and cat images from a **4×4 sprite matrix** are dynamically overlaid on detected faces.  

This project demonstrates **real-time computer vision on edge hardware** and hands-on experience with Python, OpenCV, and PiCamera2.

---

## 📁 Project Structure

Cat-My-Face/
├── haarcascades/ # Pretrained Haar Cascade classifiers for face detection
├── input_cats/ # 4x4 cat sprite image used for overlays
├── presentation/ # Presentation document for class/demo
├── raspi_code/ # Python code to run on Raspberry Pi
└── README.md

---

## 🛠️ Hardware Used

- **Raspberry Pi 5**  
- **Camera Module OV5647**  
  [Link to product](https://www.sunfounder.com/products/ov5647-camera-module?srsltid=AfmBOopnsYTXFG3fYWW95o4sIoKnK53QmIVJsBUFC1GxGaBhkpQniV0z)

> The system is fully offline and runs in real-time, demonstrating edge computing capabilities.

---

## 📌 Features

- Real-time face detection using OpenCV Haar Cascades
- 16 cat images from a 4×4 sprite matrix
- Alpha blending and background removal for clean overlays
- Keyboard controls for switching cat overlays
- Multiple faces detection and overlay in a single frame
- Fully runs on Raspberry Pi without cloud dependency

---

## 🧠 Technical Overview

1. **Face Detection**
   - Uses OpenCV’s Haar Cascade (`haarcascade_frontalface_alt2.xml`)
   - Multi-face detection supported
   - Grayscale processing for faster computation

2. **Camera Pipeline**
   - Uses Picamera2 API for live feed
   - RGB frames converted to BGR for OpenCV processing

3. **Cat Overlay**
   - Cat images stored in a 4×4 matrix (`input_cats`)
   - Extracted dynamically using array slicing
   - Overlay size automatically scales to detected face

4. **Background Removal & Alpha Blending**
   - White/near-white pixels are removed
   - Smooth blending with alpha channel

5. **Overlay Application**
   - Resizes cat images to match face dimensions
   - Boundary-safe blending to avoid crashes near edges

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| → (Right Arrow) | Next cat overlay |
| ← (Left Arrow)  | Previous cat overlay |
| Q | Quit application |

---

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Cat-My-Face.git
cd Cat-My-Face/raspi_code
