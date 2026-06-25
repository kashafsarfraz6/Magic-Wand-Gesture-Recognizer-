import asyncio
import websockets
import json
import numpy as np
import pickle
import time
from collections import deque

class GestureRecognizer:
    def __init__(self, model_path='gesture_model.pkl', window_size=50, overlap=0.5):
        with open(model_path, 'rb') as f:
            saved = pickle.load(f)
            self.model = saved['model']
            self.scaler = saved['scaler']
            self.classes = saved['classes']
        
        self.window_size = window_size
        self.step_size = int(window_size * (1 - overlap))
        self.buffer = deque(maxlen=window_size)
        
    def add_sample(self, ax, ay, az):
        self.buffer.append((ax, ay, az))
        
    def extract_features(self):
        if len(self.buffer) < self.window_size:
            return None
        
        window = np.array([(ax, ay, az) for ax, ay, az in self.buffer])
        features = []
        
        for axis in range(3):
            data = window[:, axis]
            features.extend([
                np.mean(data), np.std(data), np.min(data), np.max(data), np.ptp(data)
            ])
        
        sma = np.mean(np.abs(window[:, 0]) + np.abs(window[:, 1]) + np.abs(window[:, 2]))
        features.append(sma)
        
        return np.array(features).reshape(1, -1)
    
    def predict(self):
        if len(self.buffer) < self.window_size:
            return None, None
        
        features = self.extract_features()
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        if hasattr(self.model, 'predict_proba'):
            probs = self.model.predict_proba(features_scaled)[0]
            confidence = np.max(probs) * 100
        else:
            confidence = 100.0
        
        return prediction, confidence

async def live_inference(uri):
    recognizer = GestureRecognizer('gesture_model.pkl')
    
    print("="*60)
    print("GESTURE RECOGNIZER - LIVE INFERENCE")
    print("="*60)
    print(f"Connecting to: {uri}")
    print("Classes:", recognizer.classes)
    print("-"*60)
    
    try:
        async with websockets.connect(uri) as ws:
            print("✓ Connected! Waiting for data...")
            print("-"*60)
            
            sample_count = 0
            
            while True:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    data = json.loads(msg)
                    ax, ay, az = data["values"]
                    
                    recognizer.add_sample(ax, ay, az)
                    sample_count += 1
                    
                    if sample_count % recognizer.step_size == 0:
                        prediction, confidence = recognizer.predict()
                        
                        if prediction is not None:
                            confidence_bar = "█" * int(confidence / 10) + "░" * (10 - int(confidence / 10))
                            print(f"[{sample_count:4d}] {prediction:12s} | {confidence:5.1f}% {confidence_bar}")
                            
                except asyncio.TimeoutError:
                    print("⚠️ No data for 2 seconds...")
                    continue
                    
    except Exception as e:
        print(f"✗ Connection error: {e}")

def main():
    ESP32_IP = "192.168.43.153"
    URI = f"ws://{ESP32_IP}:8080/sensor/connect?type=android.sensor.accelerometer"
    asyncio.run(live_inference(URI))

if __name__ == "__main__":
    main()