# Color-Vision-Chatbot-Testing-System

This project aims to support individuals in identifying and understanding their color vision capabilities through two key components: a **color blindness test interface** and a **color-identifying chatbot**. The system uses OpenCV, Tkinter, and machine learning concepts to create an interactive visual aid and assessment tool.

---

## 📁 Project Structure

- `final_chabot.py`: The main chatbot interface built with NLP logic and Tkinter GUI to interact with users about color vision topics.
- `identify_c.py`: Uses real-time webcam feed to identify and highlight objects of specific colors.
- `test.py`: An interactive color blindness test using labeled image datasets to assess user accuracy.
- `dataset`: It contains the images which is used for color indentification test.

---

## 🚀 Features

### 🧠 Color Vision Chatbot
- Built with natural language responses.
- Provides general guidance about color vision and related deficiencies.
- Offers support and direction based on user queries.

### 🎥 Real-Time Color Detection
- Uses OpenCV to detect specific colors (red, green, blue, etc.) from live webcam feed.
- Displays bounding boxes and labels around identified objects.
- Handles a wide range of color shades.

### 🧪 Color Blindness Testing Tool
- Presents users with randomly ordered color-labeled images.
- Users input what number/label they see.
- Calculates accuracy and gives feedback: normal vision, mild, or severe color blindness.

---

## 🛠️ Tech Stack

- **Languages**: Python
- **Libraries**: OpenCV, NumPy, PIL, tkinter, random, os, cv2
- **Environment**: Desktop application (Tkinter UI + webcam integration)

---

## 📊 Accuracy Logic (Color Blindness Test)
- Accuracy > 80%: Normal Color Vision (likely)
- 50% < Accuracy ≤ 80%: Possible Mild Color Blindness
- Accuracy ≤ 50%: Possible Moderate/Severe Color Blindness

---

## 🧪 How to Run

1. Clone or download the repository.
2. Install dependencies (if not already installed):
   ```bash
   pip install opencv-python pillow
