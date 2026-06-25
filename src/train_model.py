import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv(r"C:\Users\Lenovo\Documents\project ml\A1\gesture_data.csv")
print("✅ Data loaded")
print(f"Total rows: {len(df)}")
print(f"Gestures: {df['gesture'].unique()}\n")

# Function to segment windows
def segment_windows(df, window_size=50, overlap=0.5):
    step = int(window_size * (1 - overlap))
    windows = []
    labels = []
    trial_ids = []
    
    for gesture in df['gesture'].unique():
        for trial in df[df['gesture'] == gesture]['trial_id'].unique():
            trial_data = df[(df['gesture'] == gesture) & (df['trial_id'] == trial)]
            data = trial_data[['ax', 'ay', 'az']].values
            
            if len(data) < window_size:
                continue
                
            for start in range(0, len(data) - window_size + 1, step):
                window = data[start:start + window_size]
                windows.append(window)
                labels.append(gesture)
                trial_ids.append(f"{gesture}_{trial}")
    
    return np.array(windows), np.array(labels), np.array(trial_ids)

# Function to extract features
def extract_features(windows):
    features = []
    for window in windows:
        feat = []
        for axis in range(3):
            data = window[:, axis]
            feat.extend([
                np.mean(data),
                np.std(data),
                np.min(data),
                np.max(data),
                np.ptp(data)
            ])
        sma = np.mean(np.abs(window[:, 0]) + np.abs(window[:, 1]) + np.abs(window[:, 2]))
        feat.append(sma)
        features.append(feat)
    return np.array(features)

# Create windows and features
print("="*50)
print("CREATING WINDOWS")
print("="*50)
windows, labels, trial_ids = segment_windows(df, window_size=50, overlap=0.5)
print(f"Windows created: {len(windows)}")

print("\n" + "="*50)
print("EXTRACTING FEATURES")
print("="*50)
X = extract_features(windows)
print(f"Feature matrix shape: {X.shape}")

# Split by TRIAL (no data leakage)
print("\n" + "="*50)
print("TRAIN/TEST SPLIT (by trial)")
print("="*50)

# Get unique trials
unique_trials = np.unique(trial_ids)
np.random.seed(42)
np.random.shuffle(unique_trials)

# 70% train, 30% test
split_idx = int(0.7 * len(unique_trials))
train_trials = unique_trials[:split_idx]
test_trials = unique_trials[split_idx:]

print(f"Training trials: {len(train_trials)}")
print(f"Testing trials: {len(test_trials)}")

# Create train/test indices
train_idx = [i for i, tid in enumerate(trial_ids) if tid in train_trials]
test_idx = [i for i, tid in enumerate(trial_ids) if tid in test_trials]

X_train = X[train_idx]
X_test = X[test_idx]
y_train = labels[train_idx]
y_test = labels[test_idx]

print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Normalize for k-NN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================
# MODEL 1: k-NN (k=3)
# ============================================
print("\n" + "="*50)
print("MODEL 1: k-NEAREST NEIGHBOURS (k=3)")
print("="*50)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_scaled, y_train)
y_pred_knn = knn.predict(X_test_scaled)

acc_knn = accuracy_score(y_test, y_pred_knn)
print(f"\n✅ Accuracy: {acc_knn * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_knn))

# ============================================
# MODEL 2: RANDOM FOREST
# ============================================
print("\n" + "="*50)
print("MODEL 2: RANDOM FOREST")
print("="*50)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

acc_rf = accuracy_score(y_test, y_pred_rf)
print(f"\n✅ Accuracy: {acc_rf * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_rf))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred_rf)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=np.unique(labels), 
            yticklabels=np.unique(labels))
plt.title('Confusion Matrix - Random Forest')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
plt.close()
print("\n✅ Confusion matrix saved as 'confusion_matrix.png'")

# Feature importance
feature_names = []
for axis in ['ax', 'ay', 'az']:
    for stat in ['mean', 'std', 'min', 'max', 'ptp']:
        feature_names.append(f"{axis}_{stat}")
feature_names.append('SMA')

importance = rf.feature_importances_
indices = np.argsort(importance)[::-1]

plt.figure(figsize=(10, 6))
plt.bar(range(10), importance[indices[:10]])
plt.xticks(range(10), [feature_names[i] for i in indices[:10]], rotation=45)
plt.title('Top 10 Feature Importances - Random Forest')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150)
plt.close()
print("✅ Feature importance saved as 'feature_importance.png'")

# Summary
print("\n" + "="*50)
print("FINAL SUMMARY")
print("="*50)
print(f"k-NN Accuracy:     {acc_knn * 100:.2f}%")
print(f"Random Forest Acc: {acc_rf * 100:.2f}%")
print(f"\n✅ Best model: {'Random Forest' if acc_rf > acc_knn else 'k-NN'}")

input("\nPress Enter to exit...")