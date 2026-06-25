import json
import time
import csv
from websocket import create_connection

ESP32_IP = "192.168.43.153"
URI = f"ws://{ESP32_IP}:8080/sensor/connect?type=android.sensor.accelerometer"

GESTURE = "figure8"
SAMPLES = 50  # 50 naye samples (total 30+50=80 ho jayenge)
DURATION_SEC = 1

def collect_figure8():
    filename = "gesture_data.csv"
    
    # Pehle dekhte hain already kitne figure8 samples hain
    import pandas as pd
    try:
        df = pd.read_csv(filename)
        existing = len(df[df['gesture'] == 'figure8']['trial_id'].unique())
        print(f"Existing figure8 trials: {existing}")
        print(f"Adding {SAMPLES} more...")
    except:
        print("Starting fresh collection")
    
    print("\n=== FIGURE-8 GESTURE COLLECTION ===")
    print("Technique: Draw figure-8 slowly in air (1 second)")
    print("Start and end at same point")
    print(f"New samples to collect: {SAMPLES}\n")
    
    # Find next trial ID
    try:
        df = pd.read_csv(filename)
        next_trial = df[df['gesture'] == 'figure8']['trial_id'].max() + 1 if len(df[df['gesture'] == 'figure8']) > 0 else 0
    except:
        next_trial = 0
    
    for trial in range(SAMPLES):
        print(f"\n[{trial+1}/{SAMPLES}] Figure-8 (Trial ID: {next_trial + trial})")
        input("Press ENTER, THEN draw figure-8 slowly...")
        
        ws = create_connection(URI, timeout=10)
        
        data_points = []
        deadline = time.time() + DURATION_SEC
        
        while time.time() < deadline:
            try:
                msg = ws.recv()
                data = json.loads(msg)
                ts = data["timestamp"]
                ax, ay, az = data["values"]
                data_points.append([ts, ax, ay, az, GESTURE, next_trial + trial])
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
    
    print(f"\n✓ DONE! Added {SAMPLES} figure-8 samples to {filename}")

if __name__ == "__main__":
    collect_figure8()