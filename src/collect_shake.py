import json
import time
import csv
from websocket import create_connection

ESP32_IP = "192.168.43.153"
URI = f"ws://{ESP32_IP}:8080/sensor/connect?type=android.sensor.accelerometer"

GESTURE = "shake"
SAMPLES = 30
DURATION_SEC = 1

def collect_shake():
    filename = "gesture_data.csv"
    
    print("\n=== SHAKE GESTURE COLLECTION ===")
    print("Technique: Hold wand and shake left-right QUICKLY for 1 second")
    print(f"Samples to collect: {SAMPLES}\n")
    
    for trial in range(SAMPLES):
        print(f"\n[{trial+1}/{SAMPLES}] SHAKE")
        input("Press ENTER, THEN shake the wand...")
        
        ws = create_connection(URI, timeout=10)
        
        data_points = []
        deadline = time.time() + DURATION_SEC
        
        while time.time() < deadline:
            try:
                msg = ws.recv()
                data = json.loads(msg)
                ts = data["timestamp"]
                ax, ay, az = data["values"]
                data_points.append([ts, ax, ay, az, GESTURE, trial])
            except:
                continue
        
        ws.close()
        print(f"  ✓ Collected {len(data_points)} frames")
        
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data_points)
        
        if trial < SAMPLES - 1:
            print("  Wait 1 second...")
            time.sleep(1)
    
    print(f"\n✓ DONE! Shake data added to {filename}")

if __name__ == "__main__":
    collect_shake()