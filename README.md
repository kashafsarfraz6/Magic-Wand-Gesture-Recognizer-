# 🎯 Magic Wand Gesture Recognizer

A machine learning-based gesture recognition system that uses an **ESP32 DevKit V1** and **MPU6050 accelerometer** to recognize hand gestures in real time.

The project combines **IoT, Machine Learning, Feature Engineering, and Real-Time Inference** to classify gestures from live accelerometer data streamed over WebSocket.

---

## 🚀 Project Overview

This system collects accelerometer data from an MPU6050 sensor connected to an ESP32, extracts statistical features, trains machine learning models, and performs real-time gesture recognition.

### Recognized Gestures

* Rest
* Rotate CW
* Double Tap
* Figure-8
* Shake

---

## 🏗 Hardware Components

* ESP32 DevKit V1
* MPU6050 Accelerometer Sensor
* Mini Breadboard
* Jumper Wires
* USB-C Cable

---

## ⚙️ Machine Learning Pipeline

### 1. Data Collection

* Sampling Rate: 50 Hz
* 30 trials per gesture
* 5 gesture classes
* 7,500 raw sensor frames collected

### 2. Feature Engineering

Extracted features include:

* Mean
* Standard Deviation
* Minimum
* Maximum
* Peak-to-Peak Range
* Signal Magnitude Area (SMA)

Total Features: **16**

### 3. Model Training

Implemented and evaluated:

* K-Nearest Neighbours (k=3)
* Random Forest (100 Trees)

### 4. Real-Time Inference

* Sliding Window Approach
* 50% Window Overlap
* Live ESP32 WebSocket Stream
* Real-Time Gesture Prediction

---

## 📊 Results

| Model         | Accuracy | Macro F1 |
| ------------- | -------- | -------- |
| KNN           | 95.00%   | 93.58%   |
| Random Forest | 95.00%   | 95.91%   |

🏆 **Selected Model:** Random Forest

---

## ⚡ Performance

* Real-Time Prediction
* End-to-End Latency: 10–20 ms
* Prediction Rate: ~2 predictions/sec
* 5 Gesture Classes Supported

---

## 🛠 Tech Stack

### Programming

* Python

### Machine Learning

* Scikit-Learn
* NumPy
* Pandas

### Hardware & IoT

* ESP32
* MPU6050
* WebSocket Communication

### Visualization

* Matplotlib

---

## 📂 Project Structure

```text
Magic-Wand-Gesture-Recognizer/
│
├── collect_shake.py
├── feature_extraction.py
├── train_model.py
├── live_inference.py
├── plots.py
│
├── data/
│
├── docs/
│   └── Assignment1_Report_ml.pdf
│
└── README.md
```

## 🎓 Academic Context

This project was developed as part of a Machine Learning assignment at the Institute of Space and Technology (IST), demonstrating the complete workflow from sensor data acquisition to real-time machine learning deployment.

## 👥 Contributors

* Kashaf Sarfraz
* Filza Rehman
* Saman Zafar

## 📄 Documentation

Detailed implementation, methodology, and results are available in the project report located in the `docs` folder.
