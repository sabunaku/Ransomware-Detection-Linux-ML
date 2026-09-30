import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# ========= LOAD DATA ============
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "final_dataset_shuffled.csv"

df = pd.read_csv(DATA_PATH)

# Remove PID (not useful)
df = df.drop(columns=["PID"])

# Remove total_triplets if it exists
if "total_triplets" in df.columns:
    df = df.drop(columns=["total_triplets"])

# ========= SPLIT FEATURES & LABEL ============
X = df.drop(columns=["LABEL"])
y = df["LABEL"]

# ========= TRAIN / TEST SPLIT ============
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

# ========= TRAIN MODELS ============
rf = RandomForestClassifier(n_estimators=200, random_state=42)
svm = SVC(probability=True, random_state=42)
dt = DecisionTreeClassifier(random_state=42)
knn = KNeighborsClassifier()

rf.fit(X_train, y_train)
svm.fit(X_train, y_train)
dt.fit(X_train, y_train)
knn.fit(X_train, y_train)

# ========= PREDICTIONS ============
models = {
    "Random Forest": rf,
    "SVM": svm,
    "Decision Tree": dt,
    "KNN": knn
}

y_preds = {name: model.predict(X_test) for name, model in models.items()}
y_probs = {name: model.predict_proba(X_test)[:, 1] for name, model in models.items()}

# ========= EVALUATION ============
for name in models.keys():
    print(f"\n=== {name} Evaluation ===")
    print("Accuracy:", accuracy_score(y_test, y_preds[name]))
    print("Precision:", precision_score(y_test, y_preds[name]))
    print("Recall:", recall_score(y_test, y_preds[name]))
    print("F1 Score:", f1_score(y_test, y_preds[name]))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_preds[name]))

# ========= CONFUSION MATRICES (VISUAL) ============

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for ax, (name, preds) in zip(axes, y_preds.items()):
    cm = confusion_matrix(y_test, preds)

    # Show matrix
    im = ax.imshow(cm, cmap="Blues")

    # Title
    ax.set_title(f"{name} Confusion Matrix")

    # Fix ticks (0 = Benign, 1 = Malware)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    ax.set_xticklabels(["Benign (0)", "Malware (1)"])
    ax.set_yticklabels(["Benign (0)", "Malware (1)"])

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    # Write values in each cell
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="black", fontsize=12, fontweight="bold")

plt.tight_layout()
plt.show()

# ========= ROC CURVES ============
plt.figure(figsize=(10, 7))

for name, probs in y_probs.items():
    fpr, tpr, _ = roc_curve(y_test, probs)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{name} AUC={roc_auc:.3f}")

plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend()
plt.show()

# ========= TOP 15 FEATURES (RF) ============
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1][:15]

plt.figure(figsize=(10, 7))
plt.bar(range(15), importances[indices])
plt.xticks(range(15), X.columns[indices], rotation=45, ha="right")
plt.title("Top 15 Most Important Features (Random Forest)")
plt.tight_layout()
plt.show()
