import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

DATASET_PATH = "dataset/repositories.csv"
MODEL_PATH = "models/repository_health_model.pkl"

data = pd.read_csv(DATASET_PATH)

print("\nDataset loaded successfully!")
print("Number of records:", len(data))
print("\nDataset columns:")
print(data.columns.tolist())


# --------------------------------------------------
# 2. Select features and target
# --------------------------------------------------

features = [
    "stars",
    "forks",
    "open_issues",
    "contributors",
    "total_commits",
    "recent_commits",
    "repository_age",
    "days_since_last_update"
]

X = data[features]
y = data["health"]


# --------------------------------------------------
# 3. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)


print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# --------------------------------------------------
# 4. Create Random Forest model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# --------------------------------------------------
# 5. Train model
# --------------------------------------------------

print("\nTraining Random Forest model...")

model.fit(X_train, y_train)

print("Model training completed!")


# --------------------------------------------------
# 6. Make predictions
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# 7. Evaluate model
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"\nAccuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 8. Save trained model
# --------------------------------------------------

joblib.dump(model, MODEL_PATH)

print("\n==============================")
print("MODEL SAVED SUCCESSFULLY")
print("==============================")

print(f"Model saved at: {MODEL_PATH}")