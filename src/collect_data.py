import json
import time
import csv
from websocket import create_connection

ESP32_IP = "192.168.43.153"
URI = f"ws://{ESP32_IP}:8080/sensor/connect?type=android.sensor.accelerometer"

# Define your gestures
GESTURES = ["rest", "rotate_cw", "double_tap", "figure8", "circle"]
SAMPLES_PER_GESTURE = 30   # 30 trials per gesture
DURATION_SEC = 1            # 1 second = 50 frames at 50 Hz

def collect_gesture(gesture_name, trial_num):
    """Collect 1 second of data for a single trial"""
    print(f"\n>>> {gesture_name} - Trial {trial_num + 1}/{SAMPLES_PER_GESTURE}")
    input("Press ENTER and THEN perform the gesture...")
    
    ws = create_connection(URI, timeout=5)
    
    data_points = []
    start_time = time.time()
    deadline = start_time + DURATION_SEC
    
    while time.time() < deadline:
        msg = ws.recv()
        data = json.loads(msg)
        ts = data["timestamp"]
        ax, ay, az = data["values"]
        data_points.append([ts, ax, ay, az])
    
    ws.close()
    print(f"  ✓ Collected {len(data_points)} frames (target: 50)")
    return data_points

def collect_all():
    # Create CSV file with headers
    filename = "gesture_data.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ts_ns", "ax", "ay", "az", "gesture", "trial_id"])
    
    total_trials = len(GESTURES) * SAMPLES_PER_GESTURE
    current = 0
    
    for gesture in GESTURES:
        print(f"\n{'='*50}")
        print(f"COLLECTING: {gesture}")
        print(f"{'='*50}")
        
        for trial in range(SAMPLES_PER_GESTURE):
            current += 1
            print(f"\n[{current}/{total_trials}]")
            
            points = collect_gesture(gesture, trial)
            
            # Save to CSV
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                for ts, ax, ay, az in points:
                    writer.writerow([ts, ax, ay, az, gesture, trial])
            
            # Rest between trials
            if trial < SAMPLES_PER_GESTURE - 1:
                print("  Rest 1 second before next trial...")
                time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"✓ DATA COLLECTION COMPLETE!")
    print(f"  File saved: {filename}")
    print(f"  Total samples: {total_trials} trials x ~50 frames = ~{total_trials * 50} frames")
    print(f"{'='*50}")

if __name__ == "__main__":
    print("=== GESTURE DATA COLLECTION ===")
    print(f"Gestures to collect: {GESTURES}")
    print(f"Samples per gesture: {SAMPLES_PER_GESTURE}")
    print(f"Duration per sample: {DURATION_SEC} second")
    print(f"Total trials: {len(GESTURES) * SAMPLES_PER_GESTURE}")
    print(f"\nIMPORTANT RULES:")
    print("1. Hold the board the SAME way for every gesture")
    print("2. Wait for 'Press ENTER' then perform gesture")
    print("3. Keep board still during 'Rest 1 second'")
    print("4. Use same speed each time")
    
    input("\nPress ENTER to start data collection...")
    collect_all()