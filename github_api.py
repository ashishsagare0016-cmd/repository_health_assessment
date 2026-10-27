import requests
from datetime import datetime, timezone
from urllib.parse import urlparse


GITHUB_API = "https://api.github.com"


def parse_repository_url(repository_url):
    """
    Extract the owner and repository name from a GitHub URL.
    """

    parsed_url = urlparse(repository_url.strip())

    if parsed_url.netloc.lower() not in ["github.com", "www.github.com"]:
        raise ValueError("Please enter a valid GitHub repository URL.")

    parts = parsed_url.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repo = parts[1]

    # Remove .git if the user enters a Git clone URL
    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


def github_request(endpoint):
    """
    Send a request to the GitHub API.
    """

    url = f"{GITHUB_API}{endpoint}"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code == 404:
        raise ValueError("Repository not found. Check the GitHub URL.")

    if response.status_code == 403:
        raise ValueError(
            "GitHub API rate limit reached. Please try again later."
        )

    if response.status_code != 200:
        raise ValueError(
            f"GitHub API error. Status code: {response.status_code}"
        )

    return response.json()


def get_repository_data(repository_url):
    """
    Collect repository information required by the ML model.
    """

    owner, repo = parse_repository_url(repository_url)

    # --------------------------------------------------
    # 1. Get basic repository information
    # --------------------------------------------------

    repository = github_request(
        f"/repos/{owner}/{repo}"
    )

    # --------------------------------------------------
    # 2. Basic statistics
    # --------------------------------------------------

    stars = repository.get("stargazers_count", 0)
    forks = repository.get("forks_count", 0)
    open_issues = repository.get("open_issues_count", 0)

    created_at = repository.get("created_at")
    updated_at = repository.get("updated_at")

    # --------------------------------------------------
    # 3. Repository age
    # --------------------------------------------------

    created_date = datetime.fromisoformat(
        created_at.replace("Z", "+00:00")
    )

    now = datetime.now(timezone.utc)

    repository_age = max(
        1,
        int((now - created_date).days / 365.25)
    )

    # --------------------------------------------------
    # 4. Days since last update
    # --------------------------------------------------

    updated_date = datetime.fromisoformat(
        updated_at.replace("Z", "+00:00")
    )

    days_since_last_update = max(
        0,
        (now - updated_date).days
    )

    # --------------------------------------------------
    # 5. Get contributors
    # --------------------------------------------------

    contributors_data = github_request(
        f"/repos/{owner}/{repo}/contributors?per_page=100"
    )

    contributors = len(contributors_data)

    # --------------------------------------------------
    # 6. Get recent commits
    # --------------------------------------------------

    commits_data = github_request(
        f"/repos/{owner}/{repo}/commits?per_page=100"
    )

    recent_commits = len(commits_data)

    # --------------------------------------------------
    # 7. Get total commit count
    # --------------------------------------------------

    total_commits = 0

    commits_url = (
        f"{GITHUB_API}/repos/{owner}/{repo}/commits"
        "?per_page=1"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    commits_response = requests.get(
        commits_url,
        headers=headers,
        timeout=15
    )

    if commits_response.status_code == 200:

        link_header = commits_response.headers.get("Link", "")

        if 'rel="last"' in link_header:

            last_part = link_header.split('rel="last"')[0]

            if "page=" in last_part:
                page_number = last_part.split("page=")[-1]
                page_number = page_number.split(">")[0]
                page_number = page_number.strip("&")

                try:
                    total_commits = int(page_number)
                except ValueError:
                    total_commits = len(commits_data)

        else:
            total_commits = len(commits_data)

    # --------------------------------------------------
    # 8. Prepare result
    # --------------------------------------------------

    repository_data = {
        "name": repository.get("full_name"),
        "description": repository.get("description"),
        "stars": stars,
        "forks": forks,
        "open_issues": open_issues,
        "contributors": contributors,
        "total_commits": total_commits,
        "recent_commits": recent_commits,
        "repository_age": repository_age,
        "days_since_last_update": days_since_last_update,
        "url": repository.get("html_url")
    }

    return repository_data


# ------------------------------------------------------
# TESTING
# ------------------------------------------------------

if __name__ == "__main__":

    test_url = input(
        "Enter a public GitHub repository URL: "
    )

    try:

        data = get_repository_data(test_url)

        print("\n===================================")
        print("GITHUB REPOSITORY INFORMATION")
        print("===================================")

        for key, value in data.items():
            print(f"{key}: {value}")

        print("\nGitHub API test completed successfully!")

    except Exception as error:

        print("\nERROR:")
        print(error)