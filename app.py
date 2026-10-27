from flask import Flask, render_template, request, jsonify

from github_api import get_repository_data
from predict import predict_repository_health
from explainable_ai import explain_prediction
from sustainability import calculate_sustainability_score


app = Flask(__name__)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Advanced Page
# --------------------------------------------------

@app.route("/advanced")
def advanced():
    return render_template("advanced.html")


# --------------------------------------------------
# Repository Analysis API
# --------------------------------------------------

@app.route("/api/analyze", methods=["POST"])
def analyze_repository():

    try:

        # Get JSON data from JavaScript
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400

        repository_url = data.get(
            "repository_url",
            ""
        ).strip()

        if not repository_url:

            return jsonify({
                "error": "Please enter a GitHub repository URL."
            }), 400


        # ------------------------------------------
        # Step 1: Fetch GitHub repository data
        # ------------------------------------------

        repository_data = get_repository_data(
            repository_url
        )


        # ------------------------------------------
        # Step 2: Machine Learning prediction
        # ------------------------------------------

        health_result = predict_repository_health(
            repository_data
        )


        # ------------------------------------------
        # Step 3: Sustainability calculation
        # ------------------------------------------

        sustainability_result = (
            calculate_sustainability_score(
                repository_data
            )
        )


        # ------------------------------------------
        # Step 4: Generate Explainable AI Analysis
        # ------------------------------------------

        explanation_result = explain_prediction(
            repository_data,
            health_result
        )


        # ------------------------------------------
        # Step 5: Send result to frontend
        # ------------------------------------------

        result = {

            "repository": repository_data,

            "health": health_result["health"],

            "confidence": health_result["confidence"],

            "sustainability_score":
                sustainability_result["score"],

            "sustainability_category":
                sustainability_result["category"],

            "explanation": explanation_result
        }


        return jsonify(result)


    except Exception as e:

        print("\n====================================")
        print("ANALYSIS ERROR")
        print("====================================")
        print(str(e))
        print("====================================\n")

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Explainable AI API
# --------------------------------------------------

@app.route("/api/explain", methods=["POST"])
def explain_repository():

    try:

        # Get JSON data from JavaScript
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400


        # Get repository URL (support both 'url' and 'repository_url')
        repo_url = (
            data.get("url") or data.get("repository_url") or ""
        ).strip()

        if not repo_url:

            return jsonify({
                "error": "Repository URL is required."
            }), 400


        # ------------------------------------------
        # Step 1: Fetch GitHub repository data
        # ------------------------------------------

        repo_data = get_repository_data(
            repo_url
        )


        # ------------------------------------------
        # Step 2: Machine Learning prediction
        # ------------------------------------------

        prediction = predict_repository_health(
            repo_data
        )


        # ------------------------------------------
        # Step 3: Generate explanation
        # ------------------------------------------

        explanation = explain_prediction(
            repo_data,
            prediction
        )


        # ------------------------------------------
        # Step 4: Send explanation to frontend
        # ------------------------------------------

        return jsonify(explanation)


    except Exception as e:

        print("\n====================================")
        print("EXPLAINABLE AI ERROR")
        print("====================================")
        print(str(e))
        print("====================================\n")

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Repository Comparison API
# --------------------------------------------------

@app.route("/api/compare", methods=["POST"])
def compare_repositories_api():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400

        repo_a_url = (data.get("repo_a") or data.get("url_a") or "").strip()
        repo_b_url = (data.get("repo_b") or data.get("url_b") or "").strip()

        if not repo_a_url or not repo_b_url:
            return jsonify({
                "error": "Please enter both Repository A and Repository B URLs."
            }), 400

        repo_a_data = get_repository_data(repo_a_url)
        repo_b_data = get_repository_data(repo_b_url)

        health_a = predict_repository_health(repo_a_data)
        health_b = predict_repository_health(repo_b_data)

        sust_a = calculate_sustainability_score(repo_a_data)
        sust_b = calculate_sustainability_score(repo_b_data)

        explanation_a = explain_prediction(repo_a_data, health_a)
        explanation_b = explain_prediction(repo_b_data, health_b)

        return jsonify({
            "repo_a": {
                "data": repo_a_data,
                "health": health_a["health"],
                "confidence": health_a["confidence"],
                "sustainability_score": sust_a["score"],
                "sustainability_category": sust_a["category"],
                "explanation": explanation_a
            },
            "repo_b": {
                "data": repo_b_data,
                "health": health_b["health"],
                "confidence": health_b["confidence"],
                "sustainability_score": sust_b["score"],
                "sustainability_category": sust_b["category"],
                "explanation": explanation_b
            }
        })

    except Exception as e:

        print("\n====================================")
        print("REPOSITORY COMPARISON ERROR")
        print("====================================")
        print(str(e))
        print("====================================\n")

        return jsonify({
            "error": str(e)
        }), 500



# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    print("\n======================================")
    print("REPOSITORY HEALTH ASSESSMENT SYSTEM")
    print("======================================")

    print("Starting Flask application...")

    print(
        "Open: http://127.0.0.1:5000"
    )

    print("======================================\n")


    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )