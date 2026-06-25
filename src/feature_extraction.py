import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('gesture_data.csv')
print(f"Total rows: {len(df)}")
print(f"Gestures: {df['gesture'].unique()}")
print(f"Trials per gesture:\n{df.groupby('gesture')['trial_id'].nunique()}")

def segment_windows(df, window_size=50, overlap=0.5):
    """Segment into overlapping windows (50 samples = 1 second at 50Hz)"""
    step = int(window_size * (1 - overlap))  # 25 samples for 50% overlap
    windows = []
    labels = []
    trial_ids = []
    
    for gesture in df['gesture'].unique():
        for trial in df[df['gesture'] == gesture]['trial_id'].unique():
            trial_data = df[(df['gesture'] == gesture) & (df['trial_id'] == trial)]
            data = trial_data[['ax', 'ay', 'az']].values
            
            if len(data) < window_size:
                print(f"Warning: {gesture} trial {trial} has only {len(data)} samples")
                continue
                
            for start in range(0, len(data) - window_size + 1, step):
                window = data[start:start + window_size]
                windows.append(window)
                labels.append(gesture)
                trial_ids.append(f"{gesture}_{trial}")
    
    return np.array(windows), np.array(labels), np.array(trial_ids)

def extract_features(windows):
    """Extract features from each window"""
    features = []
    
    for window in windows:
        feat = []
        for axis in range(3):  # ax, ay, az
            data = window[:, axis]
            feat.extend([
                np.mean(data),      # mean
                np.std(data),       # standard deviation
                np.min(data),       # minimum
                np.max(data),       # maximum
                np.ptp(data)        # peak-to-peak (max - min)
            ])
        
        # Signal Magnitude Area (SMA)
        sma = np.mean(np.abs(window[:, 0]) + np.abs(window[:, 1]) + np.abs(window[:, 2]))
        feat.append(sma)
        
        features.append(feat)
    
    return np.array(features)

# Process data
print("\n" + "="*50)
print("SEGMENTING WINDOWS")
print("="*50)
windows, labels, trial_ids = segment_windows(df, window_size=50, overlap=0.5)
print(f"Windows created: {len(windows)}")

print("\n" + "="*50)
print("EXTRACTING FEATURES")
print("="*50)
X = extract_features(windows)
print(f"Feature matrix shape: {X.shape}")

# Feature names
feature_names = []
for axis in ['ax', 'ay', 'az']:
    for stat in ['mean', 'std', 'min', 'max', 'ptp']:
        feature_names.append(f"{axis}_{stat}")
feature_names.append('SMA')
print(f"Features: {feature_names}")

print("\n" + "="*50)
print("SAVING FEATURES")
print("="*50)
np.save('X_features.npy', X)
np.save('y_labels.npy', labels)
np.save('trial_ids.npy', trial_ids)

print(f"X shape: {X.shape}")
print(f"y shape: {labels.shape}")
print(f"Unique labels: {np.unique(labels)}")