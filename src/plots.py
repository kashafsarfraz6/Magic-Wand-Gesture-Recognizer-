import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(r"C:\Users\Lenovo\Documents\project ml\A1\gesture_data.csv")

# Gestures
gestures = ["rest", "rotate_cw", "double_tap", "figure8", "shake"]

# Har gesture ke liye alag plot
for gesture in gestures:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    gesture_data = df[df["gesture"] == gesture]
    trials = gesture_data["trial_id"].unique()[:3]
    
    for j, trial in enumerate(trials):
        trial_data = gesture_data[gesture_data["trial_id"] == trial].head(50)
        
        axes[j].plot(trial_data["ax"], label="ax", color="red", linewidth=1.5)
        axes[j].plot(trial_data["ay"], label="ay", color="green", linewidth=1.5)
        axes[j].plot(trial_data["az"], label="az", color="blue", linewidth=1.5)
        
        axes[j].set_title(f"{gesture} - Trial {trial}", fontsize=12)
        axes[j].set_xlabel("Frame (50 frames = 1 sec)", fontsize=10)
        axes[j].set_ylabel("Acceleration (m/s²)", fontsize=10)
        axes[j].legend(loc="upper right")
        axes[j].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{gesture}_plots.png", dpi=150)
    plt.show()
    print(f"✅ {gesture}_plots.png saved")

print("🎉 All plots done!")