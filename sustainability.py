def calculate_sustainability_score(repository_data):
    """
    Calculate a sustainability score from 0 to 100.
    """

    stars = repository_data["stars"]
    forks = repository_data["forks"]
    open_issues = repository_data["open_issues"]
    contributors = repository_data["contributors"]
    total_commits = repository_data["total_commits"]
    recent_commits = repository_data["recent_commits"]
    repository_age = repository_data["repository_age"]
    days_since_last_update = repository_data["days_since_last_update"]

    # --------------------------------------------------
    # 1. Community score
    # --------------------------------------------------

    community_score = min(
        20,
        (stars / 10000) * 10 +
        (forks / 2000) * 5 +
        (contributors / 100) * 5
    )

    # --------------------------------------------------
    # 2. Development activity score
    # --------------------------------------------------

    activity_score = min(
        25,
        (total_commits / 5000) * 15 +
        (recent_commits / 100) * 10
    )

    # --------------------------------------------------
    # 3. Maintenance score
    # --------------------------------------------------

    if days_since_last_update <= 7:
        maintenance_score = 25

    elif days_since_last_update <= 30:
        maintenance_score = 20

    elif days_since_last_update <= 90:
        maintenance_score = 15

    elif days_since_last_update <= 180:
        maintenance_score = 8

    else:
        maintenance_score = 3

    # --------------------------------------------------
    # 4. Longevity score
    # --------------------------------------------------

    longevity_score = min(
        15,
        repository_age * 2
    )

    # --------------------------------------------------
    # 5. Issue management score
    # --------------------------------------------------

    if open_issues <= 10:
        issue_score = 15

    elif open_issues <= 50:
        issue_score = 12

    elif open_issues <= 100:
        issue_score = 8

    elif open_issues <= 200:
        issue_score = 5

    else:
        issue_score = 2

    # --------------------------------------------------
    # 6. Final score
    # --------------------------------------------------

    score = (
        community_score +
        activity_score +
        maintenance_score +
        longevity_score +
        issue_score
    )

    score = min(
        100,
        max(0, round(score))
    )

    # --------------------------------------------------
    # 7. Sustainability category
    # --------------------------------------------------

    if score >= 80:
        category = "Highly Sustainable"

    elif score >= 60:
        category = "Sustainable"

    elif score >= 40:
        category = "Moderately Sustainable"

    else:
        category = "Low Sustainability"

    return {
        "score": score,
        "category": category
    }


# ------------------------------------------------------
# TESTING
# ------------------------------------------------------

if __name__ == "__main__":

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

    result = calculate_sustainability_score(
        test_repository
    )

    print("\n===================================")
    print("REPOSITORY SUSTAINABILITY")
    print("===================================")

    print(
        "Sustainability Score:",
        str(result["score"]) + "/100"
    )

    print(
        "Category:",
        result["category"]
    )