def explain_prediction(repo_data, prediction_result):
    """
    Generate comprehensive Explainable AI report for a GitHub repository.
    Includes:
    - Repository analysis & prediction rationale
    - What has been added / Recent development activity
    - Good features (Strengths) & Features to improve (Weaknesses)
    - Recommended additional features to add to the repository
    - Concepts and technologies to study further
    """

    stars = repo_data.get("stars", 0)
    forks = repo_data.get("forks", 0)
    open_issues = repo_data.get("open_issues", 0)
    contributors = repo_data.get("contributors", 0)
    total_commits = repo_data.get("total_commits", 0)
    recent_commits = repo_data.get("recent_commits", 0)
    repository_age = repo_data.get("repository_age", 0)
    days_since_update = repo_data.get("days_since_last_update", 0)
    repo_name = repo_data.get("name", "Repository")

    health_status = prediction_result.get("health", "Unknown")
    confidence = prediction_result.get("confidence", 0)

    # 1. Overview Narrative
    if health_status == "Healthy":
        overview = (
            f"The repository '{repo_name}' is classified as HEALTHY with {confidence}% confidence. "
            f"It demonstrates strong community engagement ({stars:,} stars, {forks:,} forks), active contributor involvement ({contributors} contributors), "
            f"and high ongoing development velocity ({recent_commits} recent commits)."
        )
    elif health_status == "Moderate":
        overview = (
            f"The repository '{repo_name}' is classified as MODERATE with {confidence}% confidence. "
            f"While it maintains baseline activity, certain key areas such as issue management ({open_issues} open issues) or update frequency "
            f"({days_since_update} days since last update) require attention to sustain long-term repository health."
        )
    else:
        overview = (
            f"The repository '{repo_name}' is classified as AT-RISK / LOW SUSTAINABILITY with {confidence}% confidence. "
            f"Key maintenance indicators show low recent commit activity ({recent_commits} recent commits), limited contributor participation ({contributors} contributors), "
            f"or delayed updates ({days_since_update} days inactive)."
        )

    # 2. What Has Been Added / Recent Activity Breakdown
    what_has_been_added = []

    what_has_been_added.append({
        "title": "Recent Code Contributions",
        "detail": f"{recent_commits} commit(s) pushed in the recent activity window.",
        "status": "Active" if recent_commits >= 20 else "Low Activity",
        "icon": "⚡"
    })

    if days_since_update == 0:
        update_text = "Updated today!"
    elif days_since_update == 1:
        update_text = "Updated 1 day ago."
    else:
        update_text = f"Updated {days_since_update} days ago."

    what_has_been_added.append({
        "title": "Latest Update Recency",
        "detail": update_text,
        "status": "Fresh" if days_since_update <= 30 else "Stale",
        "icon": "🕒"
    })

    what_has_been_added.append({
        "title": "Community & Contributor Network",
        "detail": f"Accumulated {contributors} contributor(s), {stars:,} star(s), and {forks:,} fork(s).",
        "status": "Vibrant" if contributors >= 10 or stars >= 100 else "Growing",
        "icon": "👥"
    })

    what_has_been_added.append({
        "title": "Cumulative Codebase History",
        "detail": f"{total_commits:,} total commit(s) logged across {repository_age} year(s) of development.",
        "status": "Established" if total_commits >= 300 else "Initial Phase",
        "icon": "📚"
    })

    # 3. Good Features (Strengths)
    good_features = []

    if recent_commits >= 30:
        good_features.append({
            "feature": "High Development Velocity",
            "value": f"{recent_commits} recent commits",
            "reason": "Frequent code commits indicate active development, rapid bug fixes, and continuous improvement.",
            "impact": "Positive",
            "badge": "Strong Velocity"
        })

    if contributors >= 15:
        good_features.append({
            "feature": "Diverse Contributor Base",
            "value": f"{contributors} active contributors",
            "reason": "A multi-contributor project mitigates single-maintainer bottleneck risks ('bus factor') and fosters open community involvement.",
            "impact": "Positive",
            "badge": "Community Backed"
        })

    if open_issues <= 20:
        good_features.append({
            "feature": "Streamlined Issue Backlog",
            "value": f"{open_issues} open issues",
            "reason": "Low open issue count reflects effective issue triage, responsive maintenance, and quick resolutions.",
            "impact": "Positive",
            "badge": "Efficient Triage"
        })

    if stars >= 500:
        good_features.append({
            "feature": "Strong Community Interest",
            "value": f"{stars:,} stars",
            "reason": "High star count proves strong developer adoption, project popularity, and community trust.",
            "impact": "Positive",
            "badge": "Popular Repo"
        })

    if forks >= 50:
        good_features.append({
            "feature": "High Extensibility & Fork Activity",
            "value": f"{forks:,} forks",
            "reason": "Forks show that developers are actively cloning, modifying, and building downstream features from this codebase.",
            "impact": "Positive",
            "badge": "Highly Forked"
        })

    if days_since_update <= 14:
        good_features.append({
            "feature": "Active Maintenance",
            "value": update_text,
            "reason": "The repository is actively maintained with recent updates, ensuring compatibility and dependency patches.",
            "impact": "Positive",
            "badge": "Up To Date"
        })

    if total_commits >= 500:
        good_features.append({
            "feature": "Substantial Commit History",
            "value": f"{total_commits:,} commits",
            "reason": "A mature commit history reflects long-term stability and sustained development effort.",
            "impact": "Positive",
            "badge": "Mature Codebase"
        })

    if not good_features:
        good_features.append({
            "feature": "Repository Foundation",
            "value": f"{repository_age} year(s) online",
            "reason": "The project has established a public presence on GitHub and provides a foundation for future development.",
            "impact": "Positive",
            "badge": "Active Foundation"
        })

    # 4. Features / Aspects to Improve (Weaknesses)
    improvements_needed = []

    if open_issues > 30:
        severity = "High" if open_issues > 100 else "Medium"
        improvements_needed.append({
            "feature": "High Open Issue Backlog",
            "value": f"{open_issues} open issues",
            "severity": severity,
            "reason": "Accumulating open issues without resolution can frustrate users and signal maintainer burnout or slow bug handling.",
            "recommendation": "Implement issue labeling, automated issue staleness bots, and triage workflows to prioritize critical bugs."
        })

    if recent_commits < 15:
        severity = "High" if recent_commits < 5 else "Medium"
        improvements_needed.append({
            "feature": "Low Recent Commit Velocity",
            "value": f"{recent_commits} recent commits",
            "severity": severity,
            "reason": "Slow commit pace may indicate stagnant development, reduced maintainer bandwidth, or project hiatus.",
            "recommendation": "Schedule regular sprint cycles or open 'good first issue' tags to invite community feature additions."
        })

    if days_since_update > 45:
        severity = "High" if days_since_update > 120 else "Medium"
        improvements_needed.append({
            "feature": "Lapsing Maintenance & Update Recency",
            "value": f"{days_since_update} days since update",
            "severity": severity,
            "reason": "Long gaps between updates increase security risks from outdated third-party dependencies.",
            "recommendation": "Set up automated dependency updates (e.g. Dependabot) and maintain regular release cadence."
        })

    if contributors < 5:
        improvements_needed.append({
            "feature": "Single Maintainer Risk (Bus Factor)",
            "value": f"{contributors} contributor(s)",
            "severity": "Medium",
            "reason": "Heavy reliance on 1-2 maintainers risks project abandonment if core developers become unavailable.",
            "recommendation": "Add a CONTRIBUTING.md guide, tag starter issues, and invite active pull request authors as co-maintainers."
        })

    if forks < 10 and stars > 100:
        improvements_needed.append({
            "feature": "Low Fork-to-Star Conversion",
            "value": f"{forks} forks vs {stars:,} stars",
            "severity": "Low",
            "reason": "High stars relative to low forks suggest passive interest rather than active code modification or contribution.",
            "recommendation": "Improve local development setup instructions (README, Dockerfile) to make cloning and running easy for contributors."
        })

    if not improvements_needed:
        improvements_needed.append({
            "feature": "Continuous Quality Maintenance",
            "value": "Optimal metrics",
            "severity": "Low",
            "reason": "The repository is performing well across core metrics. Focus should be on maintaining current standards.",
            "recommendation": "Expand automated integration test suites and add performance benchmarks."
        })

    # 5. Recommended Additional Features to Add
    recommended_features = [
        {
            "name": "Automated CI/CD Workflows (GitHub Actions)",
            "category": "DevOps & Automation",
            "priority": "High",
            "description": "Add `.github/workflows/ci.yml` to automatically run unit tests, linting checks, and build verification on every pull request.",
            "impact": "Prevents breaking changes from merging and ensures high code reliability."
        },
        {
            "name": "Issue & Pull Request Templates",
            "category": "Community Governance",
            "priority": "High" if open_issues > 20 else "Medium",
            "description": "Create `.github/ISSUE_TEMPLATE/` (bug report, feature request) and `PULL_REQUEST_TEMPLATE.md` to standardize submissions.",
            "impact": "Reduces back-and-forth communication and improves issue triage speed."
        },
        {
            "name": "Automated Security & Dependency Alerts (Dependabot)",
            "category": "Security",
            "priority": "High",
            "description": "Configure `dependabot.yml` for automated security vulnerability scanning and pull requests for outdated packages.",
            "impact": "Protects the codebase from supply-chain security vulnerabilities."
        },
        {
            "name": "Code Coverage & Static Analysis Badges",
            "category": "Quality Assurance",
            "priority": "Medium",
            "description": "Integrate tools like Codecov, SonarQube, or Code Climate with README badges to track test coverage transparency.",
            "impact": "Boosts contributor confidence and maintains strict coverage thresholds."
        },
        {
            "name": "Standardized Documentation Suite",
            "category": "Documentation",
            "priority": "High" if contributors < 10 else "Medium",
            "description": "Include `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `CHANGELOG.md` alongside an architectural diagram.",
            "impact": "Lowers onboarding friction for prospective open-source contributors."
        },
        {
            "name": "Containerization & One-Command Setup (Docker / DevContainer)",
            "category": "Developer Experience",
            "priority": "Medium",
            "description": "Add a `Dockerfile` and `docker-compose.yml` or `.devcontainer/` setup for deterministic local development environments.",
            "impact": "Eliminates 'works on my machine' issues for new developers."
        }
    ]

    # 6. Concepts & Technologies to Study Further
    study_topics = [
        {
            "topic": "Continuous Integration & GitHub Actions Workflow Syntax",
            "category": "DevOps & CI/CD",
            "description": "Learn YAML workflow syntax, build matrices, action triggers, caching dependencies, and secret management in GitHub Actions.",
            "why_relevant": "Essential for automating tests, linting, and deployment pipelines directly within GitHub.",
            "key_skills": ["GitHub Actions", "YAML Configuration", "Automated Testing", "Pipeline Optimization"]
        },
        {
            "topic": "Automated Software Testing & Code Coverage Patterns",
            "category": "Software Testing",
            "description": "Master unit testing, integration testing, mocking external APIs (e.g. GitHub REST API), and calculating coverage metrics.",
            "why_relevant": "Ensures stability when refactoring repository analysis logic or adding new API integrations.",
            "key_skills": ["PyTest / Jest", "API Mocking", "Test-Driven Development (TDD)", "Coverage Analysis"]
        },
        {
            "topic": "Open Source Governance & Maintenance Management",
            "category": "Project Management",
            "description": "Study open-source licensing (MIT, Apache 2.0), contributor license agreements (CLA), issue labeling standards, and semantic versioning.",
            "why_relevant": "Helps transition project from single-developer prototype to a scalable community open-source project.",
            "key_skills": ["Semantic Versioning", "License Compliance", "Community Triage", "Release Engineering"]
        },
        {
            "topic": "Software Supply Chain Security & Dependency Auditing",
            "category": "Cybersecurity",
            "description": "Learn static application security testing (SAST), Software Bill of Materials (SBOM), CVE tracking, and secret scanning.",
            "why_relevant": "Protects against vulnerable third-party dependencies and hardcoded credential leaks.",
            "key_skills": ["Dependabot / Snyk", "CodeQL Security Analysis", "Secret Scanning", "SBOM Generation"]
        },
        {
            "topic": "Explainable AI (XAI) & Model Interpretability Techniques",
            "category": "Machine Learning / Data Science",
            "description": "Explore SHAP (SHapley Additive exPlanations), LIME (Local Interpretable Model-agnostic Explanations), and feature importance scoring.",
            "why_relevant": "Underpins the math and algorithms behind explaining complex ML model predictions to human end-users.",
            "key_skills": ["SHAP / LIME", "Feature Importance", "Random Forest Interpretation", "Model Auditing"]
        },
        {
            "topic": "Software Engineering & Repository Health Metrics (CHAOSS / DORA)",
            "category": "Software Analytics",
            "description": "Study industry-standard metrics frameworks like CHAOSS (Community Health Analytics Open Source Software) and DORA (DevOps Research & Assessment).",
            "why_relevant": "Provides rigorous academic & industry foundations for evaluating repository health, deployment frequency, and lead time.",
            "key_skills": ["DORA Metrics", "CHAOSS Health Indicators", "Lead Time for Changes", "Failure Rate Analytics"]
        }
    ]

    # Legacy explanations field maintained for backwards compatibility if needed
    explanations = []
    for item in good_features:
        explanations.append({
            "feature": item["feature"],
            "value": item["value"],
            "impact": "Positive",
            "reason": item["reason"]
        })
    for item in improvements_needed:
        explanations.append({
            "feature": item["feature"],
            "value": item["value"],
            "impact": "Negative" if item["severity"] in ["High", "Medium"] else "Neutral",
            "reason": item["reason"]
        })

    return {
        "repository_name": repo_name,
        "prediction": health_status,
        "confidence": confidence,
        "overview": overview,
        "what_has_been_added": what_has_been_added,
        "good_features": good_features,
        "improvements_needed": improvements_needed,
        "recommended_features": recommended_features,
        "study_topics": study_topics,
        "explanations": explanations
    }