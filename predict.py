import joblib
import pandas as pd


MODEL_PATH = "models/repository_health_model.pkl"


def predict_repository_health(repository_data):
    """
    Predict the health category of a GitHub repository.
    """

    # Load trained model
    model = joblib.load(MODEL_PATH)

    # Features used during model training
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

    # Create DataFrame from GitHub repository data
    input_data = pd.DataFrame(
        [repository_data],
        columns=features
    )

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    classes = model.classes_

    confidence = max(probabilities) * 100

    return {
        "health": prediction,
        "confidence": round(confidence, 2)
    }


if __name__ == "__main__":

    # Test data
    test_repository = {
        "stars": 74885,
        "forks": 17037,
        "open_issues": 4,
        "contributors": 100,
        "total_commits": 5557,
        "recent_commits": 100,
        "repository_age": 16,
        "days_since_last_update": 0
    }

    result = predict_repository_health(test_repository)

    print("\n===================================")
    print("REPOSITORY HEALTH PREDICTION")
    print("===================================")

    print("Health:", result["health"])
    print("Confidence:", str(result["confidence"]) + "%")