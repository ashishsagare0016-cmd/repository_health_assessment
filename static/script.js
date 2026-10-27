// ==================================================
// PAGE NAVIGATION
// ==================================================

function showSection(sectionId, btnElement) {
    // Hide all sections
    const sections = document.querySelectorAll(".page-section");
    sections.forEach(sec => {
        sec.classList.remove("active-section");
        sec.style.display = "none";
    });

    // Deactivate all nav buttons
    const navButtons = document.querySelectorAll(".nav-button");
    navButtons.forEach(btn => btn.classList.remove("active"));

    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add("active-section");
        targetSection.style.display = "block";
    }

    // Activate clicked button
    if (btnElement) {
        btnElement.classList.add("active");
    }
}


// ==================================================
// SECTION 1: REPOSITORY ANALYSIS
// ==================================================

async function analyzeRepository() {

    const url = document.getElementById("repositoryUrl").value.trim();
    const loading = document.getElementById("analysisLoading");
    const result = document.getElementById("analysisResult");
    const errorBox = document.getElementById("analysisError");
    const errorText = document.getElementById("analysisErrorText");

    if (!url) {
        errorBox.style.display = "block";
        errorText.textContent = "Please enter a GitHub repository URL.";
        return;
    }

    loading.style.display = "block";
    result.style.display = "none";
    errorBox.style.display = "none";

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ repository_url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed.");
        }

        const repository = data.repository;

        document.getElementById("repositoryName").textContent = repository.name || "-";
        document.getElementById("repositoryStars").textContent = (repository.stars ?? 0).toLocaleString();
        document.getElementById("repositoryForks").textContent = (repository.forks ?? 0).toLocaleString();
        document.getElementById("repositoryIssues").textContent = (repository.open_issues ?? 0).toLocaleString();
        document.getElementById("repositoryContributors").textContent = (repository.contributors ?? 0).toLocaleString();
        document.getElementById("repositoryCommits").textContent = (repository.total_commits ?? 0).toLocaleString();

        document.getElementById("healthStatus").textContent = data.health || "-";
        document.getElementById("healthConfidence").textContent = data.confidence + "%";
        document.getElementById("sustainabilityScore").textContent = data.sustainability_score;
        document.getElementById("sustainabilityCategory").textContent = data.sustainability_category;

        // Render 🔥 Explainable AI Breakdown in Main Analysis View
        if (data.explanation) {
            renderExplainableAIResults(data.explanation, "analysisExplainContainer");
            const explainContainer = document.getElementById("analysisExplainContainer");
            if (explainContainer) explainContainer.style.display = "block";
        }

        result.style.display = "block";

    } catch (error) {
        errorBox.style.display = "block";
        errorText.textContent = "Analysis failed: " + error.message;
    } finally {
        loading.style.display = "none";
    }
}


// ==================================================
// SECTION 2: EXPLAINABLE AI
// ==================================================

async function runExplainableAI() {

    const urlInput = document.getElementById("explainRepoUrl");
    const url = urlInput ? urlInput.value.trim() : "";
    const resultDiv = document.getElementById("explainResult");

    if (!url) {
        resultDiv.innerHTML = `
            <div class="error-message">
                <p>⚠️ Please enter a valid GitHub repository URL.</p>
            </div>
        `;
        return;
    }

    resultDiv.innerHTML = `
        <div class="loading-box" style="display: block;">
            <div class="spinner"></div>
            <p>🧠 Generating Explainable AI analysis and breakdown...</p>
        </div>
    `;

    try {
        const response = await fetch("/api/explain", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ repository_url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Explainable AI analysis failed.");
        }

        renderExplainableAIResults(data);

    } catch (error) {
        resultDiv.innerHTML = `
            <div class="error-message">
                <p>⚠️ Explainable AI Failed: ${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}

function renderExplainableAIResults(data, targetContainerId = "explainResult") {
    const resultDiv = document.getElementById(targetContainerId);
    if (!resultDiv) return;

    const healthClass = (data.prediction === "Healthy") ? "status-healthy" :
                        (data.prediction === "Moderate") ? "status-moderate" : "status-at-risk";

    let html = `
        <!-- 1. Prediction Overview Header -->
        <div class="prediction-box">
            <div class="xai-header">
                <h2>📊 Repository Health Explanation: <span class="repo-title">${escapeHtml(data.repository_name || 'Repository')}</span></h2>
                <div class="xai-badge-row">
                    <span class="xai-badge ${healthClass}">Status: ${escapeHtml(data.prediction)}</span>
                    <span class="xai-badge badge-confidence">Model Confidence: ${data.confidence}%</span>
                </div>
            </div>
            <p class="xai-overview-text">${escapeHtml(data.overview || '')}</p>
        </div>

        <!-- 2. What Has Been Added / Recent Activity Breakdown -->
        <div class="xai-section">
            <h3 class="xai-section-title">✨ What Has Been Added & Recent Activity</h3>
            <div class="xai-grid">
                ${(data.what_has_been_added || []).map(item => `
                    <div class="xai-card activity-card">
                        <div class="card-icon-header">
                            <span class="card-icon">${item.icon || '📌'}</span>
                            <span class="card-status-pill ${getStatusPillClass(item.status)}">${escapeHtml(item.status)}</span>
                        </div>
                        <h4>${escapeHtml(item.title)}</h4>
                        <p>${escapeHtml(item.detail)}</p>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- 3. Good Features (Strengths) -->
        <div class="xai-section">
            <h3 class="xai-section-title text-success">🟢 Good Features & Strengths</h3>
            <div class="xai-list">
                ${(data.good_features || []).map(item => `
                    <div class="xai-item good-item">
                        <div class="item-header">
                            <span class="item-title">${escapeHtml(item.feature)}</span>
                            <span class="badge-tag tag-positive">${escapeHtml(item.badge || 'Strength')}</span>
                        </div>
                        <div class="item-value">Metric Value: <strong>${escapeHtml(String(item.value))}</strong></div>
                        <p class="item-reason">${escapeHtml(item.reason)}</p>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- 4. Features / Aspects to Improve (Weaknesses) -->
        <div class="xai-section">
            <h3 class="xai-section-title text-warning">🟡 Features & Areas to Improve</h3>
            <div class="xai-list">
                ${(data.improvements_needed || []).map(item => `
                    <div class="xai-item improve-item">
                        <div class="item-header">
                            <span class="item-title">${escapeHtml(item.feature)}</span>
                            <span class="badge-tag tag-severity-${(item.severity || 'Medium').toLowerCase()}">Severity: ${escapeHtml(item.severity)}</span>
                        </div>
                        <div class="item-value">Current Value: <strong>${escapeHtml(String(item.value))}</strong></div>
                        <p class="item-reason"><strong>Why it needs attention:</strong> ${escapeHtml(item.reason)}</p>
                        <div class="item-recommendation"><strong>🛠️ Action Plan:</strong> ${escapeHtml(item.recommendation)}</div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- 5. Recommended Additional Features to Add -->
        <div class="xai-section">
            <h3 class="xai-section-title text-primary">💡 Recommended Additional Features to Add</h3>
            <div class="xai-grid">
                ${(data.recommended_features || []).map(feat => `
                    <div class="xai-card feature-rec-card">
                        <div class="rec-card-header">
                            <span class="category-pill">${escapeHtml(feat.category)}</span>
                            <span class="priority-tag priority-${(feat.priority || 'Medium').toLowerCase()}">${escapeHtml(feat.priority)} Priority</span>
                        </div>
                        <h4>${escapeHtml(feat.name)}</h4>
                        <p class="rec-desc">${escapeHtml(feat.description)}</p>
                        <div class="rec-impact"><strong>Impact:</strong> ${escapeHtml(feat.impact)}</div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- 6. Concepts & Technologies to Study Further -->
        <div class="xai-section">
            <h3 class="xai-section-title text-info">🎓 Concepts & Technologies to Study Further</h3>
            <div class="xai-grid study-grid">
                ${(data.study_topics || []).map(topic => `
                    <div class="xai-card study-card">
                        <div class="study-card-header">
                            <span class="study-category-badge">${escapeHtml(topic.category)}</span>
                        </div>
                        <h4>${escapeHtml(topic.topic)}</h4>
                        <p class="study-desc">${escapeHtml(topic.description)}</p>
                        <p class="study-relevance"><strong>Relevance to this Repo:</strong> ${escapeHtml(topic.why_relevant)}</p>
                        <div class="skills-tags">
                            ${(topic.key_skills || []).map(skill => `<span class="skill-pill">${escapeHtml(skill)}</span>`).join('')}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    resultDiv.innerHTML = html;
}


// ==================================================
// SECTION 3: REPOSITORY COMPARISON
// ==================================================

async function compareRepositories() {

    const repoAUrl = document.getElementById("repoA").value.trim();
    const repoBUrl = document.getElementById("repoB").value.trim();
    const resultDiv = document.getElementById("comparisonResult");

    if (!repoAUrl || !repoBUrl) {
        resultDiv.innerHTML = `
            <div class="error-message">
                <p>⚠️ Please enter both Repository A and Repository B URLs.</p>
            </div>
        `;
        return;
    }

    resultDiv.innerHTML = `
        <div class="loading-box" style="display: block;">
            <div class="spinner"></div>
            <p>⚖️ Running comparative analytics between repositories...</p>
        </div>
    `;

    try {
        const response = await fetch("/api/compare", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ repo_a: repoAUrl, repo_b: repoBUrl })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Comparison failed.");
        }

        const a = data.repo_a;
        const b = data.repo_b;

        const nameA = escapeHtml(a.data.name || 'Repository A');
        const nameB = escapeHtml(b.data.name || 'Repository B');

        // Determine metric winners
        const winSust = (a.sustainability_score > b.sustainability_score) ? 'a' : (b.sustainability_score > a.sustainability_score) ? 'b' : 'tie';
        const winStars = (a.data.stars > b.data.stars) ? 'a' : (b.data.stars > a.data.stars) ? 'b' : 'tie';
        const winForks = (a.data.forks > b.data.forks) ? 'a' : (b.data.forks > a.data.forks) ? 'b' : 'tie';
        const winIssues = (a.data.open_issues < b.data.open_issues) ? 'a' : (b.data.open_issues < a.data.open_issues) ? 'b' : 'tie';
        const winContrib = (a.data.contributors > b.data.contributors) ? 'a' : (b.data.contributors > a.data.contributors) ? 'b' : 'tie';
        const winCommits = (a.data.total_commits > b.data.total_commits) ? 'a' : (b.data.total_commits > a.data.total_commits) ? 'b' : 'tie';
        const winRecent = (a.data.recent_commits > b.data.recent_commits) ? 'a' : (b.data.recent_commits > a.data.recent_commits) ? 'b' : 'tie';
        const winRecency = (a.data.days_since_last_update < b.data.days_since_last_update) ? 'a' : (b.data.days_since_last_update < a.data.days_since_last_update) ? 'b' : 'tie';

        let html = `
            <!-- 1. Winner Summary & Verdict -->
            <div class="comparison-score">
                <div class="verdict-header">
                    <h2>⚖️ Repository Comparison Verdict</h2>
                    <span class="verdict-badge">${winSust === 'a' ? '🏆 ' + nameA + ' Leads' : winSust === 'b' ? '🏆 ' + nameB + ' Leads' : '🤝 Equal Match'}</span>
                </div>
                <p class="verdict-text">${getComparisonVerdict(a, b)}</p>
            </div>

            <!-- 2. Category Leader Badges -->
            <div class="xai-grid" style="margin-top: 25px; margin-bottom: 25px;">
                <div class="xai-card">
                    <div class="card-icon-header">
                        <span class="card-icon">🌟</span>
                        <span class="card-status-pill pill-positive">${winStars === 'a' ? nameA : winStars === 'b' ? nameB : 'Tie'}</span>
                    </div>
                    <h4>Community Interest Leader</h4>
                    <p>${winStars === 'a' ? nameA + ' leads with ' + a.data.stars.toLocaleString() + ' stars.' : winStars === 'b' ? nameB + ' leads with ' + b.data.stars.toLocaleString() + ' stars.' : 'Both repos have equal stars.'}</p>
                </div>

                <div class="xai-card">
                    <div class="card-icon-header">
                        <span class="card-icon">⚡</span>
                        <span class="card-status-pill pill-positive">${winRecent === 'a' ? nameA : winRecent === 'b' ? nameB : 'Tie'}</span>
                    </div>
                    <h4>Development Pace Leader</h4>
                    <p>${winRecent === 'a' ? nameA + ' leads with ' + a.data.recent_commits + ' recent commits.' : winRecent === 'b' ? nameB + ' leads with ' + b.data.recent_commits + ' recent commits.' : 'Both repos have equal recent activity.'}</p>
                </div>

                <div class="xai-card">
                    <div class="card-icon-header">
                        <span class="card-icon">👥</span>
                        <span class="card-status-pill pill-positive">${winContrib === 'a' ? nameA : winContrib === 'b' ? nameB : 'Tie'}</span>
                    </div>
                    <h4>Community Contributor Base</h4>
                    <p>${winContrib === 'a' ? nameA + ' has ' + a.data.contributors + ' contributors.' : winContrib === 'b' ? nameB + ' has ' + b.data.contributors + ' contributors.' : 'Both repos have equal contributors.'}</p>
                </div>

                <div class="xai-card">
                    <div class="card-icon-header">
                        <span class="card-icon">🌱</span>
                        <span class="card-status-pill pill-positive">${winSust === 'a' ? nameA : winSust === 'b' ? nameB : 'Tie'}</span>
                    </div>
                    <h4>Sustainability Score</h4>
                    <p>${winSust === 'a' ? nameA + ' scores ' + a.sustainability_score + '/100.' : winSust === 'b' ? nameB + ' scores ' + b.sustainability_score + '/100.' : 'Both repos have identical sustainability scores.'}</p>
                </div>
            </div>

            <!-- 3. Side-by-Side Detailed Metric Table -->
            <h3 class="xai-section-title" style="margin-top: 30px;">📊 Side-by-Side Metric Comparison</h3>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Metric / Indicator</th>
                        <th>${nameA}</th>
                        <th>${nameB}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Health Category</strong></td>
                        <td><span class="xai-badge ${a.health === 'Healthy' ? 'status-healthy' : 'status-moderate'}">${escapeHtml(a.health)} (${a.confidence}%)</span></td>
                        <td><span class="xai-badge ${b.health === 'Healthy' ? 'status-healthy' : 'status-moderate'}">${escapeHtml(b.health)} (${b.confidence}%)</span></td>
                    </tr>
                    <tr>
                        <td><strong>Sustainability Score</strong></td>
                        <td class="${winSust === 'a' ? 'winner-cell' : ''}">${winSust === 'a' ? '🏆 ' : ''}<strong>${a.sustainability_score}/100</strong> (${escapeHtml(a.sustainability_category)})</td>
                        <td class="${winSust === 'b' ? 'winner-cell' : ''}">${winSust === 'b' ? '🏆 ' : ''}<strong>${b.sustainability_score}/100</strong> (${escapeHtml(b.sustainability_category)})</td>
                    </tr>
                    <tr>
                        <td><strong>GitHub Stars</strong></td>
                        <td class="${winStars === 'a' ? 'winner-cell' : ''}">${winStars === 'a' ? '🏆 ' : ''}${(a.data.stars ?? 0).toLocaleString()}</td>
                        <td class="${winStars === 'b' ? 'winner-cell' : ''}">${winStars === 'b' ? '🏆 ' : ''}${(b.data.stars ?? 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td><strong>Forks</strong></td>
                        <td class="${winForks === 'a' ? 'winner-cell' : ''}">${winForks === 'a' ? '🏆 ' : ''}${(a.data.forks ?? 0).toLocaleString()}</td>
                        <td class="${winForks === 'b' ? 'winner-cell' : ''}">${winForks === 'b' ? '🏆 ' : ''}${(b.data.forks ?? 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td><strong>Open Issues</strong></td>
                        <td class="${winIssues === 'a' ? 'winner-cell' : ''}">${winIssues === 'a' ? '🏆 ' : ''}${(a.data.open_issues ?? 0).toLocaleString()}</td>
                        <td class="${winIssues === 'b' ? 'winner-cell' : ''}">${winIssues === 'b' ? '🏆 ' : ''}${(b.data.open_issues ?? 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td><strong>Active Contributors</strong></td>
                        <td class="${winContrib === 'a' ? 'winner-cell' : ''}">${winContrib === 'a' ? '🏆 ' : ''}${(a.data.contributors ?? 0).toLocaleString()}</td>
                        <td class="${winContrib === 'b' ? 'winner-cell' : ''}">${winContrib === 'b' ? '🏆 ' : ''}${(b.data.contributors ?? 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td><strong>Recent Commits</strong></td>
                        <td class="${winRecent === 'a' ? 'winner-cell' : ''}">${winRecent === 'a' ? '🏆 ' : ''}${(a.data.recent_commits ?? 0).toLocaleString()}</td>
                        <td class="${winRecent === 'b' ? 'winner-cell' : ''}">${winRecent === 'b' ? '🏆 ' : ''}${(b.data.recent_commits ?? 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td><strong>Total Commit History</strong></td>
                        <td class="${winCommits === 'a' ? 'winner-cell' : ''}">${winCommits === 'a' ? '🏆 ' : ''}${(a.data.total_commits ?? 0).toLocaleString()}</td>
                        <td class="${winCommits === 'b' ? 'winner-cell' : ''}">${winCommits === 'b' ? '🏆 ' : ''}${(b.data.total_commits ?? 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td><strong>Days Since Update</strong></td>
                        <td class="${winRecency === 'a' ? 'winner-cell' : ''}">${winRecency === 'a' ? '🏆 ' : ''}${a.data.days_since_last_update} days</td>
                        <td class="${winRecency === 'b' ? 'winner-cell' : ''}">${winRecency === 'b' ? '🏆 ' : ''}${b.data.days_since_last_update} days</td>
                    </tr>
                </tbody>
            </table>

            <!-- 4. Side-by-Side Strengths Breakdown -->
            <h3 class="xai-section-title text-success" style="margin-top: 35px;">🟢 Side-by-Side Strengths Comparison</h3>
            <div class="comparison-inputs" style="grid-template-columns: 1fr 1fr; margin-bottom: 25px;">
                <div class="xai-item good-item">
                    <h4>🟢 ${nameA} Strengths</h4>
                    <ul class="comp-list">
                        ${(a.explanation?.good_features || []).map(g => `<li><strong>${escapeHtml(g.feature)}:</strong> ${escapeHtml(g.reason)}</li>`).join('')}
                    </ul>
                </div>
                <div class="xai-item good-item">
                    <h4>🟢 ${nameB} Strengths</h4>
                    <ul class="comp-list">
                        ${(b.explanation?.good_features || []).map(g => `<li><strong>${escapeHtml(g.feature)}:</strong> ${escapeHtml(g.reason)}</li>`).join('')}
                    </ul>
                </div>
            </div>

            <!-- 5. Side-by-Side Areas to Improve -->
            <h3 class="xai-section-title text-warning" style="margin-top: 25px;">🟡 Side-by-Side Areas to Improve</h3>
            <div class="comparison-inputs" style="grid-template-columns: 1fr 1fr; margin-bottom: 25px;">
                <div class="xai-item improve-item">
                    <h4>🟡 ${nameA} Areas to Improve</h4>
                    <ul class="comp-list">
                        ${(a.explanation?.improvements_needed || []).map(i => `<li><strong>${escapeHtml(i.feature)}:</strong> ${escapeHtml(i.reason)}</li>`).join('')}
                    </ul>
                </div>
                <div class="xai-item improve-item">
                    <h4>🟡 ${nameB} Areas to Improve</h4>
                    <ul class="comp-list">
                        ${(b.explanation?.improvements_needed || []).map(i => `<li><strong>${escapeHtml(i.feature)}:</strong> ${escapeHtml(i.reason)}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;

        resultDiv.innerHTML = html;

    } catch (error) {
        resultDiv.innerHTML = `
            <div class="error-message">
                <p>⚠️ Comparison Failed: ${escapeHtml(error.message)}</p>
            </div>
        `;
    }
}

function getComparisonVerdict(a, b) {
    const nameA = escapeHtml(a.data.name || 'Repository A');
    const nameB = escapeHtml(b.data.name || 'Repository B');

    if (a.sustainability_score > b.sustainability_score + 10) {
        return `<strong>${nameA}</strong> demonstrates significantly stronger overall repository health and sustainability (Score: <strong>${a.sustainability_score}/100</strong> vs <strong>${b.sustainability_score}/100</strong>) due to higher community adoption, frequent commit activity, and active contributor maintenance.`;
    } else if (b.sustainability_score > a.sustainability_score + 10) {
        return `<strong>${nameB}</strong> demonstrates significantly stronger overall repository health and sustainability (Score: <strong>${b.sustainability_score}/100</strong> vs <strong>${a.sustainability_score}/100</strong>) due to higher community adoption, frequent commit activity, and active contributor maintenance.`;
    } else {
        return `Both <strong>${nameA}</strong> and <strong>${nameB}</strong> show comparable repository health scores (<strong>${a.sustainability_score}/100</strong> vs <strong>${b.sustainability_score}/100</strong>). Choose based on specific ecosystem compatibility and feature alignment.`;
    }
}


// ==================================================
// UTILITY FUNCTIONS
// ==================================================

function getStatusPillClass(status) {
    if (!status) return 'pill-neutral';
    const s = status.toLowerCase();
    if (s.includes('active') || s.includes('fresh') || s.includes('vibrant') || s.includes('established')) {
        return 'pill-positive';
    } else if (s.includes('low') || s.includes('stale')) {
        return 'pill-negative';
    }
    return 'pill-neutral';
}

function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}