/* ═══════════════════════════════════════════════════════════
   RepoHealth AI — Main Script  (fully corrected v3)
   ═══════════════════════════════════════════════════════════

   Backend API field reference (github_api.py):
     repository.name               ← full_name e.g. "pallets/flask"
     repository.description
     repository.stars              ← NOT stars_count
     repository.forks              ← NOT forks_count
     repository.open_issues        ← NOT open_issues_count
     repository.contributors       ← NOT contributors_count
     repository.total_commits
     repository.recent_commits
     repository.repository_age     ← in YEARS (not days)
     repository.days_since_last_update
     repository.url

   predict.py confidence:          ← already 0–100 (e.g. 94.0)
   sustainability.py score:        ← 0–100 integer
   explainable_ai.py keys:
     good_features[]               ← {feature, value, reason, impact, badge}
     improvements_needed[]         ← {feature, value, reason, severity}
     recommended_features[]        ← {name, category, priority, description, impact}
     study_topics[]                ← {topic, category, description, why_relevant, key_skills[]}
     overview                      ← string narrative
     what_has_been_added[]         ← {title, detail, status, icon}
═══════════════════════════════════════════════════════════ */

'use strict';

/* ─── Inject SVG gradient defs for gauges ─────────────────── */
(function injectSVGDefs() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '0'); svg.setAttribute('height', '0');
  svg.style.position = 'absolute';
  svg.innerHTML = `<defs>
    <linearGradient id="gaugeHealth" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#10b981"/><stop offset="100%" stop-color="#34d399"/>
    </linearGradient>
    <linearGradient id="gaugeSust" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f59e0b"/><stop offset="100%" stop-color="#fbbf24"/>
    </linearGradient>
    <linearGradient id="gaugeConf" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6366f1"/><stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>`;
  document.body.appendChild(svg);
})();

/* ─── Repo counter ────────────────────────────────────────── */
let totalAnalyzed = parseInt(localStorage.getItem('rh_total') || '0');
document.getElementById('totalAnalyzed').textContent = totalAnalyzed;

function bumpAnalyzed() {
  totalAnalyzed++;
  localStorage.setItem('rh_total', totalAnalyzed);
  const el = document.getElementById('totalAnalyzed');
  if (el) { el.textContent = totalAnalyzed; el.style.transform = 'scale(1.3)'; setTimeout(() => el.style.transform = '', 300); }
}

/* ─── DEMO data — matches actual API shape exactly ──────────
   confidence is 0–100 (matching predict.py output)
   repository keys match github_api.py output
   explanation keys match explainable_ai.py output
   ────────────────────────────────────────────────────────── */
const DEMOS = {
  flask: {
    repository: {
      name: 'pallets/flask',
      description: 'The Python micro framework for building web applications.',
      stars: 68000, forks: 16000, open_issues: 4,
      contributors: 680, total_commits: 4900, recent_commits: 100,
      repository_age: 14, days_since_last_update: 1, url: 'https://github.com/pallets/flask'
    },
    health: 'Healthy', confidence: 94.0,
    sustainability_score: 74, sustainability_category: 'Highly Sustainable',
    explanation: {
      overview: "pallets/flask is classified as HEALTHY with 94.0% confidence. It demonstrates strong community engagement (68,000 stars, 16,000 forks), active contributor involvement (680 contributors), and high ongoing development velocity.",
      what_has_been_added: [
        { title: 'Recent Code Contributions', detail: '100 commits pushed in the recent activity window.', status: 'Active' },
        { title: 'Latest Update Recency', detail: 'Updated 1 day ago.', status: 'Fresh' },
        { title: 'Community & Contributor Network', detail: 'Accumulated 680 contributors, 68,000 stars, and 16,000 forks.', status: 'Vibrant' }
      ],
      good_features: [
        { feature: 'High Development Velocity', value: '100 recent commits', reason: 'Frequent commits indicate active development and continuous improvement.', badge: 'Strong Velocity' },
        { feature: 'Diverse Contributor Base', value: '680 contributors', reason: 'Multi-contributor project mitigates single-maintainer risks.', badge: 'Community Backed' },
        { feature: 'Streamlined Issue Backlog', value: '4 open issues', reason: 'Low issue count reflects effective triage and responsive maintenance.', badge: 'Well Maintained' },
        { feature: 'Established Project Longevity', value: '14 years active', reason: 'Long lifespan demonstrates sustainable community adoption.', badge: 'Mature Project' }
      ],
      improvements_needed: [
        { feature: 'Release Cadence Optimization', value: 'Review schedule', reason: 'Could benefit from more frequent minor releases.', severity: 'Low' },
        { feature: 'Documentation Depth', value: 'Expand guides', reason: 'Advanced use cases could use more complete documentation.', severity: 'Low' }
      ],
      recommended_features: [
        { name: 'GitHub Discussions', category: 'Community', priority: 'High', description: 'Enable Discussions for Q&A community support.', impact: 'Reduces issue tracker noise.' },
        { name: 'Security Advisories', category: 'Security', priority: 'High', description: 'Enable private vulnerability reporting.', impact: 'Protects maintainers and users.' },
        { name: 'Dependabot Alerts', category: 'Security', priority: 'Medium', description: 'Auto-detect vulnerable dependencies.', impact: 'Proactive security posture.' }
      ],
      study_topics: [
        { topic: 'WSGI & ASGI Architecture', category: 'Web', description: 'How Flask uses Werkzeug WSGI toolkit.', why_relevant: 'Core of Flask internals.', key_skills: ['WSGI', 'Werkzeug', 'ASGI'] },
        { topic: 'Jinja2 Templating Engine', category: 'Frontend', description: 'Server-side template rendering.', why_relevant: 'Primary Flask templating.', key_skills: ['Jinja2', 'Template inheritance', 'Filters'] },
        { topic: 'Blueprint Architecture', category: 'Design', description: 'Modular Flask application structure.', why_relevant: 'Scalable app organization.', key_skills: ['Blueprints', 'Application factories'] }
      ]
    }
  },
  fastapi: {
    repository: {
      name: 'tiangolo/fastapi', description: 'FastAPI framework, high performance, easy to learn.',
      stars: 79000, forks: 13000, open_issues: 620,
      contributors: 580, total_commits: 3100, recent_commits: 80,
      repository_age: 5, days_since_last_update: 2, url: 'https://github.com/tiangolo/fastapi'
    },
    health: 'Healthy', confidence: 97.0,
    sustainability_score: 91, sustainability_category: 'Highly Sustainable',
    explanation: {
      overview: "tiangolo/fastapi is classified as HEALTHY with 97.0% confidence. 79,000 stars and rapid growth make it one of the fastest-growing Python frameworks.",
      what_has_been_added: [
        { title: 'Recent Code Contributions', detail: '80 commits recently.', status: 'Active' },
        { title: 'Latest Update Recency', detail: 'Updated 2 days ago.', status: 'Fresh' },
        { title: 'Community Network', detail: '580 contributors, 79,000 stars.', status: 'Vibrant' }
      ],
      good_features: [
        { feature: 'Explosive Star Growth', value: '79,000 stars', reason: 'One of the fastest-growing Python frameworks.', badge: 'Trending' },
        { feature: 'High ML Confidence', value: '97% confidence', reason: 'Model is highly certain of healthy classification.', badge: 'High Confidence' }
      ],
      improvements_needed: [
        { feature: 'Open Issue Volume', value: '620 open issues', reason: 'High issue count could overwhelm maintainers.', severity: 'Medium' },
        { feature: 'Wiki Not Enabled', value: 'No wiki', reason: 'Documentation could be centralized in a wiki.', severity: 'Low' }
      ],
      recommended_features: [
        { name: 'GitHub Discussions', category: 'Community', priority: 'High', description: 'Divert Q&A from issues to Discussions.', impact: 'Reduces issue count significantly.' }
      ],
      study_topics: [
        { topic: 'ASGI Servers (Uvicorn, Hypercorn)', category: 'Web', description: 'Async Python server infrastructure.', why_relevant: 'FastAPI runs on ASGI.', key_skills: ['Uvicorn', 'async/await', 'ASGI'] },
        { topic: 'Pydantic v2 Data Validation', category: 'Data', description: 'Runtime type enforcement.', why_relevant: 'Core of FastAPI validation.', key_skills: ['Pydantic', 'Type hints', 'Validators'] }
      ]
    }
  },
  react: {
    repository: {
      name: 'facebook/react', description: 'A JavaScript library for building user interfaces.',
      stars: 229000, forks: 47000, open_issues: 890,
      contributors: 1700, total_commits: 17000, recent_commits: 95,
      repository_age: 11, days_since_last_update: 1, url: 'https://github.com/facebook/react'
    },
    health: 'Healthy', confidence: 99.0,
    sustainability_score: 96, sustainability_category: 'Highly Sustainable',
    explanation: {
      overview: "facebook/react is classified as HEALTHY with 99.0% confidence. With 229,000 stars and Meta backing, React is one of the most widely used UI libraries globally.",
      what_has_been_added: [
        { title: 'Recent Contributions', detail: '95 recent commits.', status: 'Active' },
        { title: 'Update Recency', detail: 'Updated 1 day ago.', status: 'Fresh' },
        { title: 'Community', detail: '1700 contributors, 229,000 stars.', status: 'Vibrant' }
      ],
      good_features: [
        { feature: 'Massive Community', value: '229k stars, 1700 contributors', reason: 'Largest JavaScript UI ecosystem globally.', badge: 'Industry Standard' },
        { feature: 'Corporate Backing', value: 'Meta (Facebook)', reason: 'Ensures long-term maintenance and investment.', badge: 'Enterprise Backed' }
      ],
      improvements_needed: [
        { feature: 'Issue Backlog', value: '890 open issues', reason: 'Large volume requires dedicated triage team.', severity: 'Medium' }
      ],
      recommended_features: [
        { name: 'Beginner-Friendly Issue Labels', category: 'Community', priority: 'Medium', description: 'Tag good-first-issue consistently.', impact: 'Grows contributor base.' }
      ],
      study_topics: [
        { topic: 'React Fiber Architecture', category: 'Internals', description: 'React concurrent rendering engine.', why_relevant: 'Underpins all React scheduling.', key_skills: ['Fiber', 'Reconciliation', 'Scheduler'] },
        { topic: 'React Server Components', category: 'Modern React', description: 'Server-side React rendering model.', why_relevant: 'Future of React architecture.', key_skills: ['RSC', 'Streaming', 'Suspense'] }
      ]
    }
  },
  pandas: {
    repository: {
      name: 'pandas-dev/pandas', description: 'Flexible and powerful data analysis / manipulation library for Python.',
      stars: 44000, forks: 18000, open_issues: 3100,
      contributors: 3100, total_commits: 32000, recent_commits: 70,
      repository_age: 15, days_since_last_update: 3, url: 'https://github.com/pandas-dev/pandas'
    },
    health: 'Healthy', confidence: 96.0,
    sustainability_score: 88, sustainability_category: 'Highly Sustainable',
    explanation: {
      overview: "pandas-dev/pandas is HEALTHY with 96% confidence. 32,000 commits across 15 years of development makes it a cornerstone of scientific Python.",
      what_has_been_added: [
        { title: 'Recent Contributions', detail: '70 recent commits.', status: 'Active' },
        { title: 'Longevity', detail: '15 years of active development.', status: 'Established' },
        { title: 'Community', detail: '3100 contributors, 44,000 stars.', status: 'Vibrant' }
      ],
      good_features: [
        { feature: 'Industry Standard', value: '44k stars, 3100 contributors', reason: 'De-facto data analysis tool in Python ecosystem.', badge: 'Industry Standard' },
        { feature: 'Massive Codebase', value: '32,000 total commits', reason: '15 years of hardened development.', badge: 'Battle Tested' }
      ],
      improvements_needed: [
        { feature: 'Open Issue Volume', value: '3100 open issues', reason: 'High backlog needs dedicated triage effort.', severity: 'High' }
      ],
      recommended_features: [
        { name: 'Better Error Messages', category: 'UX', priority: 'High', description: 'More descriptive type errors.', impact: 'Reduces Stack Overflow questions.' }
      ],
      study_topics: [
        { topic: 'DataFrame Internals & Block Manager', category: 'Internals', description: 'How pandas stores data in blocks.', why_relevant: 'Understand memory layout for performance.', key_skills: ['NumPy arrays', 'Copy-on-Write', 'Arrow backend'] }
      ]
    }
  },
  numpy: {
    repository: {
      name: 'numpy/numpy', description: 'The fundamental package for scientific computing with Python.',
      stars: 28000, forks: 9000, open_issues: 1900,
      contributors: 1600, total_commits: 34000, recent_commits: 65,
      repository_age: 20, days_since_last_update: 4, url: 'https://github.com/numpy/numpy'
    },
    health: 'Healthy', confidence: 98.0,
    sustainability_score: 93, sustainability_category: 'Highly Sustainable',
    explanation: {
      overview: "numpy/numpy is HEALTHY with 98.0% confidence. 20 years of development and NASA/NumFOCUS funding make it critical scientific infrastructure.",
      what_has_been_added: [
        { title: 'Recent Contributions', detail: '65 recent commits.', status: 'Active' },
        { title: 'Longevity', detail: '20 years — foundational scientific Python.', status: 'Established' },
        { title: 'Community', detail: '1600 contributors, 28,000 stars.', status: 'Vibrant' }
      ],
      good_features: [
        { feature: 'Scientific Foundation', value: '34k commits, 20 years', reason: 'Underpins entire scientific Python stack.', badge: 'Critical Infrastructure' },
        { feature: 'Institutional Funding', value: 'NumFOCUS + NASA', reason: 'Guaranteed long-term maintenance.', badge: 'Funded' }
      ],
      improvements_needed: [
        { feature: 'Open Issues', value: '1900 open issues', reason: 'Needs more active triage.', severity: 'Medium' }
      ],
      recommended_features: [
        { name: 'GPU Backend Support', category: 'Performance', priority: 'High', description: 'Native GPU array dispatch.', impact: 'Competes with CuPy/JAX.' }
      ],
      study_topics: [
        { topic: 'BLAS / LAPACK Linear Algebra Bindings', category: 'Internals', description: 'Optimized Fortran/C routines used by NumPy.', why_relevant: 'Core of NumPy performance.', key_skills: ['BLAS', 'LAPACK', 'Strided arrays', 'Universal functions'] }
      ]
    }
  }
};

/* ─── Navigation ───────────────────────────────────────────── */
function navigate(sectionId, el) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  const sec = document.getElementById('sec-' + sectionId);
  if (sec) sec.classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  if (el) el.classList.add('active');
  document.getElementById('sidebar')?.classList.remove('open');
  window.scrollTo(0, 0);
  return false;
}

function toggleSidebar() {
  document.getElementById('sidebar')?.classList.toggle('open');
}

/* ─── Theme ───────────────────────────────────────────────── */
(function initTheme() {
  const saved = localStorage.getItem('rh_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeUI(saved);
})();

function toggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('rh_theme', next);
  updateThemeUI(next);
}

function updateThemeUI(theme) {
  const icon = document.getElementById('themeIcon');
  const label = document.getElementById('themeLabel');
  if (theme === 'dark') {
    if (icon) icon.innerHTML = '<path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>';
    if (label) label.textContent = 'Light Mode';
  } else {
    if (icon) icon.innerHTML = '<path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/>';
    if (label) label.textContent = 'Dark Mode';
  }
}

/* ─── PDF / Print Export ──────────────────────────────────── */
function exportPDF() {
  // Ensure slide has content before printing
  const slideTitle = document.getElementById('slideRepoName');
  if (!slideTitle || slideTitle.textContent === 'Repository Health Assessment') {
    loadDemoSlide();
  }
  navigate('slides', document.querySelector('[data-section=slides]'));
  setTimeout(() => window.print(), 600);
}

/* ─── Loading Overlay ─────────────────────────────────────── */
function showLoading(msg) {
  const el = document.getElementById('loadingMsg');
  if (el) el.textContent = msg;
  document.getElementById('loadingSteps').textContent = '';
  document.getElementById('loadingOverlay').style.display = 'flex';
}

function updateLoadingStep(step) {
  const el = document.getElementById('loadingSteps');
  if (el) el.textContent = step;
}

function hideLoading() {
  document.getElementById('loadingOverlay').style.display = 'none';
}

/* ─── Gauge Animation ─────────────────────────────────────── */
// pct = 0..100
function setGauge(fillId, valId, pct, label) {
  const circumference = 314; // 2 * π * 50
  const clamped = Math.max(0, Math.min(100, pct));
  const offset = circumference - (clamped / 100) * circumference;
  const fill = document.getElementById(fillId);
  if (fill) fill.style.strokeDashoffset = offset;
  const val = document.getElementById(valId);
  if (val) val.textContent = label;
}

/* ─── Hero (Dashboard Quick Analyze) ─────────────────────── */
function setHeroInput(url) {
  const el = document.getElementById('heroRepoInput');
  if (el) el.value = url;
}

function quickAnalyze() {
  const url = (document.getElementById('quickSearchInput')?.value || '').trim();
  if (!url) return;
  setHeroInput(url);
  navigate('dashboard', document.querySelector('[data-section=dashboard]'));
  heroAnalyze();
}

async function heroAnalyze() {
  const url = (document.getElementById('heroRepoInput')?.value || '').trim();
  if (!url) return;

  showLoading('Analyzing repository…');
  updateLoadingStep('Connecting to GitHub API…');

  try {
    let data;
    const demoKey = getDemoKey(url);
    if (demoKey) {
      await sleep(1200);
      data = DEMOS[demoKey];
    } else {
      updateLoadingStep('Running ML inference…');
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repository_url: url })
      });
      data = await res.json();
      if (data.error) throw new Error(data.error);
    }
    hideLoading();
    bumpAnalyzed();
    displayHeroResult(data);
    addTerminalLine('ML', 'Analysis complete',
      `${data.repository?.name} → ${data.health} | Conf: ${fmtConf(data.confidence)} | Sust: ${data.sustainability_score}`,
      'green');
  } catch (e) {
    hideLoading();
    addTerminalLine('ERR', 'Analysis failed', e.message, 'amber');
    alert('Error: ' + e.message);
  }
}

function displayHeroResult(data) {
  const repo = data.repository || {};
  document.getElementById('hrRepoName').textContent    = repo.name || '—';
  document.getElementById('hrRepoUrl').textContent     = repo.url  || '';
  document.getElementById('hrHealth').textContent      = data.health || '—';
  document.getElementById('hrConfidence').textContent  = fmtConf(data.confidence);
  document.getElementById('hrSustainability').textContent = (data.sustainability_score ?? '—') + (data.sustainability_score != null ? '%' : '');
  document.getElementById('hrCategory').textContent    = data.sustainability_category || '—';
  const badge = document.getElementById('hrHealthBadge');
  if (badge) { badge.textContent = data.health || '—'; badge.className = 'health-badge ' + healthBadgeClass(data.health); }
  const r = document.getElementById('heroResult');
  if (r) { r.style.display = 'block'; r.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
}

/* ─── Audit Section ───────────────────────────────────────── */
function setAuditInput(url) {
  const el = document.getElementById('auditInput');
  if (el) el.value = url;
}

async function runAudit() {
  const url = (document.getElementById('auditInput')?.value || '').trim();
  const errEl = document.getElementById('auditError');
  if (errEl) errEl.style.display = 'none';

  if (!url) { showErrEl(errEl, 'Please enter a GitHub repository URL.'); return; }

  setAuditBtn(true);
  showLoading('Running full health audit…');
  updateLoadingStep('Fetching GitHub data…');

  try {
    let data;
    const demoKey = getDemoKey(url);
    if (demoKey) {
      await sleep(800);
      updateLoadingStep('Running ML inference…');
      await sleep(700);
      data = DEMOS[demoKey];
    } else {
      updateLoadingStep('Calling ML model…');
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repository_url: url })
      });
      data = await res.json();
      if (data.error) throw new Error(data.error);
    }
    hideLoading();
    setAuditBtn(false);
    bumpAnalyzed();
    renderAuditResults(data);
    syncSlide(data);
    addTerminalLine('ML', 'Audit complete',
      `${data.repository?.name} → ${data.health} (${fmtConf(data.confidence)})`, 'green');
  } catch (e) {
    hideLoading();
    setAuditBtn(false);
    showErrEl(errEl, e.message);
    addTerminalLine('ERR', 'Audit error', e.message, 'amber');
  }
}

function setAuditBtn(loading) {
  const txt = document.getElementById('auditBtnText');
  const spin = document.getElementById('auditSpinner');
  if (txt)  txt.style.display  = loading ? 'none'  : '';
  if (spin) spin.style.display = loading ? 'block' : 'none';
}

function renderAuditResults(data) {
  const repo = data.repository || {};

  // Gauges
  // confidence from API is 0–100 already; sustainability_score is 0–100
  const confPct  = Math.min(100, data.confidence || 0);
  const sustPct  = Math.min(100, data.sustainability_score || 0);
  const healthPct = data.health === 'Healthy' ? 82 + Math.random() * 16
                  : data.health === 'Moderate' ? 45 + Math.random() * 25
                  : 10 + Math.random() * 25;

  setGauge('healthGaugeFill', 'healthGaugeVal', healthPct, data.health || '—');
  setGauge('sustGaugeFill',   'sustGaugeVal',   sustPct,   (data.sustainability_score ?? '—') + (data.sustainability_score != null ? '%' : ''));
  setGauge('confGaugeFill',   'confGaugeVal',   confPct,   fmtConf(data.confidence));

  // Repo meta
  setText('auditRepoName', repo.name || '—');
  setText('auditRepoDesc', repo.description || '');

  const hb = document.getElementById('auditHealthBadge');
  if (hb) { hb.textContent = data.health || '—'; hb.className = 'repo-health-badge ' + healthBadgeClass(data.health); }

  const sb = document.getElementById('auditSustBadge');
  if (sb) {
    sb.textContent = data.sustainability_category || '—';
    sb.className = 'repo-sust-badge';
    sb.style.cssText = 'border-color:rgba(245,158,11,0.3);color:#fbbf24;background:rgba(245,158,11,0.1);font-size:12px;font-weight:700;padding:5px 14px;border-radius:99px;border:1px solid;';
  }

  // Telemetry — using correct backend field names
  setText('tStars',    fmt(repo.stars));
  setText('tForks',    fmt(repo.forks));
  setText('tCommits',  fmt(repo.total_commits));
  setText('tContribs', fmt(repo.contributors));
  setText('tIssues',   fmt(repo.open_issues));
  // repository_age is in YEARS — show as "X yr(s)"
  setText('tAge', repo.repository_age != null ? repo.repository_age + ' yr' + (repo.repository_age !== 1 ? 's' : '') : '—');

  // Fix tAge label to "Age (yrs)"
  const ageLbl = document.querySelector('#tAge')?.closest('.tele-item')?.querySelector('.tele-label');
  if (ageLbl) ageLbl.textContent = 'Age (yrs)';

  const results = document.getElementById('auditResults');
  if (results) {
    results.style.display = 'flex';
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

/* ─── XAI Section ─────────────────────────────────────────── */
async function runXAI() {
  const url = (document.getElementById('xaiInput')?.value || '').trim();
  if (!url) return;

  setXAIBtn(true);
  showLoading('Generating AI explanation…');

  try {
    let explanation;
    const demoKey = getDemoKey(url);
    if (demoKey) {
      await sleep(1400);
      explanation = DEMOS[demoKey].explanation;
    } else {
      const res = await fetch('/api/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repository_url: url })
      });
      const d = await res.json();
      if (d.error) throw new Error(d.error);
      explanation = d;
    }
    hideLoading();
    setXAIBtn(false);
    renderXAI(explanation);
  } catch (e) {
    hideLoading();
    setXAIBtn(false);
    alert('XAI Error: ' + e.message);
  }
}

function setXAIBtn(loading) {
  const txt = document.getElementById('xaiBtnText');
  const spin = document.getElementById('xaiSpinner');
  if (txt)  txt.style.display  = loading ? 'none'  : '';
  if (spin) spin.style.display = loading ? 'block' : 'none';
}

function renderXAI(exp) {
  const grid = document.getElementById('xaiGrid');
  if (!grid) return;
  grid.style.display = 'grid';

  // Overview / Activity
  const act = document.getElementById('xaiActivity');
  if (act) act.innerHTML = `
    <h3 style="font-size:14px;font-weight:700;margin-bottom:12px;color:var(--text-primary)">
      <span style="color:var(--cyan)">&#9660;</span> Overview &amp; Activity
    </h3>
    <p style="color:var(--text-secondary);font-size:13px;line-height:1.7">${escapeHtml(exp.overview || '—')}</p>
    ${(exp.what_has_been_added || []).map(w => `
      <div style="margin-top:10px;padding:8px 12px;background:var(--bg-panel);border-radius:8px;border-left:3px solid var(--cyan)">
        <div style="font-size:12px;font-weight:700;color:var(--text-primary)">${escapeHtml(w.title || '')}</div>
        <div style="font-size:12px;color:var(--text-secondary);margin-top:2px">${escapeHtml(w.detail || '')}</div>
        <span style="font-size:10px;font-weight:700;padding:1px 7px;border-radius:99px;background:rgba(6,182,212,0.12);color:var(--cyan);margin-top:4px;display:inline-block">${escapeHtml(w.status || '')}</span>
      </div>`).join('')}`;

  // Strengths — good_features is array of {feature, value, reason, badge}
  const str = document.getElementById('xaiStrengths');
  if (str) str.innerHTML = `
    <h3 style="font-size:14px;font-weight:700;margin-bottom:12px;color:var(--text-primary)">
      <span style="color:var(--emerald)">&#10003;</span> Strengths
    </h3>
    <ul class="xai-list">
      ${(exp.good_features || []).map(f => `
        <li style="border-color:var(--emerald)">
          <div style="font-size:12px;font-weight:700;color:var(--text-primary)">${escapeHtml(f.feature || '')} <span style="font-size:10px;background:rgba(16,185,129,0.12);color:var(--emerald);padding:1px 7px;border-radius:99px;font-weight:700">${escapeHtml(f.badge || '')}</span></div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px">${escapeHtml(f.value || '')} — ${escapeHtml(f.reason || '')}</div>
        </li>`).join('') || '<li>No strengths identified.</li>'}
    </ul>`;

  // Improvements — improvements_needed is array of {feature, value, reason, severity}
  const imp = document.getElementById('xaiImprovements');
  if (imp) imp.innerHTML = `
    <h3 style="font-size:14px;font-weight:700;margin-bottom:12px;color:var(--text-primary)">
      <span style="color:var(--amber)">&#9651;</span> Areas for Improvement
    </h3>
    <ul class="xai-list">
      ${(exp.improvements_needed || []).map(f => `
        <li style="border-color:var(--amber)">
          <div style="font-size:12px;font-weight:700;color:var(--text-primary)">${escapeHtml(f.feature || '')} <span style="font-size:10px;background:rgba(245,158,11,0.12);color:var(--amber);padding:1px 7px;border-radius:99px;font-weight:700">${escapeHtml(f.severity || '')}</span></div>
          <div style="font-size:11px;color:var(--text-muted);margin-top:2px">${escapeHtml(f.value || '')} — ${escapeHtml(f.reason || '')}</div>
        </li>`).join('') || '<li>No improvements needed.</li>'}
    </ul>`;

  // Features + Topics — recommended_features and study_topics
  const feat = document.getElementById('xaiFeatures');
  if (feat) feat.innerHTML = `
    <h3 style="font-size:14px;font-weight:700;margin-bottom:12px;color:var(--text-primary)">
      <span style="color:var(--indigo-light)">&#9670;</span> Recommended Features &amp; Study Topics
    </h3>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div>
        <div style="font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px">Recommended Features</div>
        <ul class="xai-list">
          ${(exp.recommended_features || []).map(f => `
            <li style="border-color:var(--indigo)">
              <div style="font-size:12px;font-weight:700;color:var(--text-primary)">${escapeHtml(f.name || '')}
                <span style="font-size:10px;background:rgba(99,102,241,0.12);color:var(--indigo-light);padding:1px 7px;border-radius:99px">${escapeHtml(f.priority || '')}</span>
              </div>
              <div style="font-size:11px;color:var(--text-muted);margin-top:2px">${escapeHtml(f.impact || f.description || '')}</div>
            </li>`).join('') || '<li>—</li>'}
        </ul>
      </div>
      <div>
        <div style="font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px">Study Topics</div>
        <ul class="xai-list">
          ${(exp.study_topics || []).map(t => `
            <li style="border-color:var(--purple)">
              <div style="font-size:12px;font-weight:700;color:var(--text-primary)">${escapeHtml(t.topic || '')}</div>
              <div style="font-size:11px;color:var(--text-muted);margin-top:2px">${escapeHtml(t.why_relevant || t.description || '')}</div>
              ${t.key_skills ? `<div style="margin-top:4px;display:flex;flex-wrap:wrap;gap:4px">${t.key_skills.map(s => `<span style="font-size:10px;background:rgba(139,92,246,0.1);color:var(--purple-light);padding:1px 7px;border-radius:99px">${escapeHtml(s)}</span>`).join('')}</div>` : ''}
            </li>`).join('') || '<li>—</li>'}
        </ul>
      </div>
    </div>`;

  grid.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ─── Compare Section ─────────────────────────────────────── */
async function runCompare() {
  const urlA = (document.getElementById('compareA')?.value || '').trim();
  const urlB = (document.getElementById('compareB')?.value || '').trim();
  if (!urlA || !urlB) { alert('Please enter both repository URLs.'); return; }

  setCompareBtn(true);
  showLoading('Comparing repositories…');

  try {
    let dataA, dataB;
    const dkA = getDemoKey(urlA), dkB = getDemoKey(urlB);
    if (dkA && dkB) {
      await sleep(1800);
      dataA = DEMOS[dkA]; dataB = DEMOS[dkB];
    } else {
      const res = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_a: urlA, repo_b: urlB })
      });
      const d = await res.json();
      if (d.error) throw new Error(d.error);
      // API returns repo_a / repo_b objects, each with data/health/confidence/etc.
      dataA = { repository: d.repo_a.data, health: d.repo_a.health, confidence: d.repo_a.confidence, sustainability_score: d.repo_a.sustainability_score, sustainability_category: d.repo_a.sustainability_category };
      dataB = { repository: d.repo_b.data, health: d.repo_b.health, confidence: d.repo_b.confidence, sustainability_score: d.repo_b.sustainability_score, sustainability_category: d.repo_b.sustainability_category };
    }
    hideLoading();
    setCompareBtn(false);
    renderCompare(dataA, dataB);
  } catch (e) {
    hideLoading();
    setCompareBtn(false);
    alert('Compare error: ' + e.message);
  }
}

function setCompareBtn(loading) {
  const txt = document.getElementById('compareBtnText');
  const spin = document.getElementById('compareSpinner');
  if (txt)  txt.style.display  = loading ? 'none'  : '';
  if (spin) spin.style.display = loading ? 'block' : 'none';
}

function renderCompare(a, b) {
  const ra = a.repository || {}, rb = b.repository || {};
  setText('cNameA', ra.name || 'Repo A');
  setText('cNameB', rb.name || 'Repo B');

  // confidence from API is 0–100
  const confA = a.confidence || 0, confB = b.confidence || 0;

  const metrics = [
    { label: 'Health',         vA: a.health,   vB: b.health,   numA: a.health === 'Healthy' ? 3 : a.health === 'Moderate' ? 2 : 1, numB: b.health === 'Healthy' ? 3 : b.health === 'Moderate' ? 2 : 1 },
    { label: 'Confidence',     vA: fmtConf(confA), vB: fmtConf(confB), numA: confA, numB: confB },
    { label: 'Sustainability', vA: (a.sustainability_score ?? '—') + '%', vB: (b.sustainability_score ?? '—') + '%', numA: a.sustainability_score || 0, numB: b.sustainability_score || 0 },
    { label: 'Category',       vA: a.sustainability_category || '—', vB: b.sustainability_category || '—', numA: 0, numB: 0 },
    { label: 'Stars',          vA: fmt(ra.stars),          vB: fmt(rb.stars),          numA: ra.stars || 0,          numB: rb.stars || 0 },
    { label: 'Forks',          vA: fmt(ra.forks),          vB: fmt(rb.forks),          numA: ra.forks || 0,          numB: rb.forks || 0 },
    { label: 'Total Commits',  vA: fmt(ra.total_commits),  vB: fmt(rb.total_commits),  numA: ra.total_commits || 0,  numB: rb.total_commits || 0 },
    { label: 'Contributors',   vA: fmt(ra.contributors),   vB: fmt(rb.contributors),   numA: ra.contributors || 0,   numB: rb.contributors || 0 },
    { label: 'Open Issues',    vA: fmt(ra.open_issues),    vB: fmt(rb.open_issues),    numA: ra.open_issues || 0,    numB: rb.open_issues || 0, lowerWins: true },
    { label: 'Age (yrs)',      vA: (ra.repository_age || '—') + (ra.repository_age ? ' yrs' : ''), vB: (rb.repository_age || '—') + (rb.repository_age ? ' yrs' : ''), numA: ra.repository_age || 0, numB: rb.repository_age || 0 },
  ];

  let winsA = 0, winsB = 0;
  const tbody = document.getElementById('compareTableBody');
  if (!tbody) return;

  tbody.innerHTML = metrics.map(m => {
    let clA = '', clB = '';
    if (m.numA !== undefined && m.numB !== undefined && m.numA !== m.numB) {
      const winA = m.lowerWins ? m.numA < m.numB : m.numA > m.numB;
      const winB = m.lowerWins ? m.numB < m.numA : m.numB > m.numA;
      if (winA) { clA = 'cell-win'; winsA++; }
      if (winB) { clB = 'cell-win'; winsB++; }
    }
    return `<tr>
      <td class="cell-metric">${m.label}</td>
      <td class="${clA}">${m.vA || '—'}</td>
      <td class="${clB}">${m.vB || '—'}</td>
    </tr>`;
  }).join('');

  const winBar = document.getElementById('compareWinner');
  if (winBar) {
    if (winsA > winsB) {
      winBar.textContent = `WINNER: ${ra.name || 'Repo A'} — ${winsA} vs ${winsB} metrics won`;
      winBar.style.cssText = 'background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.3);color:#818cf8;padding:14px 24px;border-radius:10px;font-size:15px;font-weight:700;text-align:center;margin-bottom:16px;';
    } else if (winsB > winsA) {
      winBar.textContent = `WINNER: ${rb.name || 'Repo B'} — ${winsB} vs ${winsA} metrics won`;
      winBar.style.cssText = 'background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);color:#34d399;padding:14px 24px;border-radius:10px;font-size:15px;font-weight:700;text-align:center;margin-bottom:16px;';
    } else {
      winBar.textContent = `TIE — ${winsA} metrics each`;
      winBar.style.cssText = 'background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);color:#fbbf24;padding:14px 24px;border-radius:10px;font-size:15px;font-weight:700;text-align:center;margin-bottom:16px;';
    }
  }

  const res = document.getElementById('compareResults');
  if (res) { res.style.display = 'block'; res.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
}

/* ─── Sandbox Simulator ───────────────────────────────────── */
function updateSandbox() {
  const stars    = +document.getElementById('sStars').value;
  const forks    = +document.getElementById('sForks').value;
  const commits  = +document.getElementById('sCommits').value;
  const contribs = +document.getElementById('sContribs').value;
  const issues   = +document.getElementById('sIssues').value;
  const age      = +document.getElementById('sAge').value;
  const wiki     = +document.getElementById('sWiki').value;
  const license  = +document.getElementById('sLicense').value;

  setText('lStars',    fmt(stars));
  setText('lForks',    fmt(forks));
  setText('lCommits',  fmt(commits));
  setText('lContribs', fmt(contribs));
  setText('lIssues',   fmt(issues));
  setText('lAge',      fmt(age));
  setText('lWiki',     wiki   ? 'Yes' : 'No');
  setText('lLicense',  license ? 'Yes' : 'No');

  // Heuristic health pillars
  const activity    = Math.min(100, (commits / 500) * 50 + (forks / 1000) * 30 + (contribs / 100) * 20);
  const community   = Math.min(100, (stars / 10000) * 40 + (contribs / 200) * 40 + (forks / 2000) * 20);
  const maintenance = Math.min(100, Math.max(0, 80 - (issues / Math.max(commits, 1)) * 200 + wiki * 10 + license * 10));
  const popularity  = Math.min(100, (stars / 20000) * 60 + (forks / 5000) * 40);
  const governance  = Math.min(100, license * 50 + wiki * 30 + Math.min(20, age / 100));

  const overall = (activity * 0.25 + community * 0.25 + maintenance * 0.2 + popularity * 0.2 + governance * 0.1);
  const health  = overall > 65 ? 'Healthy' : overall > 40 ? 'Moderate' : 'Unhealthy';
  const conf    = Math.min(99, 55 + overall * 0.4).toFixed(1);

  const sbH = document.getElementById('sbHealth');
  if (sbH) {
    sbH.textContent = health;
    sbH.style.background = health === 'Healthy'
      ? 'linear-gradient(90deg,#10b981,#34d399)'
      : health === 'Moderate'
      ? 'linear-gradient(90deg,#f59e0b,#fbbf24)'
      : 'linear-gradient(90deg,#ef4444,#f87171)';
  }
  setText('sbConf', `Confidence: ${conf}%`);

  setPillar('activity',    activity);
  setPillar('community',   community);
  setPillar('maintenance', maintenance);
  setPillar('popularity',  popularity);
  setPillar('governance',  governance);
}

function setPillar(name, score) {
  const bar   = document.getElementById('pbar-' + name);
  const label = document.getElementById('pscore-' + name);
  if (bar)   bar.style.width       = Math.round(score) + '%';
  if (label) label.textContent     = Math.round(score) + '%';
}

// Init sandbox on page load
updateSandbox();

/* ─── Executive Slide Deck ────────────────────────────────── */
const slideDate = document.getElementById('slideDate');
if (slideDate) slideDate.textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

function syncSlide(data) {
  const repo = data.repository || {};
  setText('slideRepoName', repo.name || 'Repository Analysis');
  setText('slideHealth',   data.health || '—');
  setText('slideSust',     (data.sustainability_score ?? '—') + (data.sustainability_score != null ? '%' : ''));
  setText('slideConf',     fmtConf(data.confidence));
  setText('slideCategory', data.sustainability_category || '—');

  const exp = data.explanation || {};
  // Use good_features for strengths, improvements_needed for improvements
  const strList  = (exp.good_features || []).map(f => `<li>${escapeHtml(f.feature || '')}: ${escapeHtml(f.value || '')}</li>`).join('');
  const impList  = (exp.improvements_needed || []).map(f => `<li>${escapeHtml(f.feature || '')}</li>`).join('');
  const recList  = (exp.recommended_features || []).map(f => `<li>${escapeHtml(f.name || '')}</li>`).join('');

  const slideStr = document.getElementById('slideStrengths');
  const slideImp = document.getElementById('slideImprovements');
  const slideRec = document.getElementById('slideRecommended');
  if (slideStr) slideStr.innerHTML = strList || '<li>Run an audit to populate</li>';
  if (slideImp) slideImp.innerHTML = impList || '<li>Run an audit to populate</li>';
  if (slideRec) slideRec.innerHTML = recList || '<li>Run an audit to populate</li>';
}

function loadDemoSlide() {
  syncSlide(DEMOS['flask']);
}

/* ─── Terminal live stream ────────────────────────────────── */
function addTerminalLine(type, label, msg, color) {
  const body = document.getElementById('terminalBody');
  if (!body) return;
  const now  = new Date();
  const time = [now.getHours(), now.getMinutes(), now.getSeconds()].map(n => String(n).padStart(2, '0')).join(':');
  const colorClass = color ? `t-${color}` : '';
  const typeClasses = { ML: 't-ml', ERR: 't-sys', XAI: 't-xai', API: 't-api' };
  const typeClass = typeClasses[type] || 't-sys';
  const line = document.createElement('div');
  line.className = 'term-line';
  line.innerHTML = `<span class="t-time">${time}</span><span class="${typeClass}">${type}</span><span class="t-text ${colorClass}">${escapeHtml(msg)}</span>`;
  line.style.opacity = '0';
  body.appendChild(line);
  setTimeout(() => { line.style.transition = 'opacity 0.3s'; line.style.opacity = '1'; }, 30);
  body.scrollTop = body.scrollHeight;
  if (body.children.length > 30) body.removeChild(body.children[0]);
}

/* ─── Ambient Canvas Particle Network ────────────────────── */
(function initAmbientCanvas() {
  const canvas = document.getElementById('ambientCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    particles = [];
    const count = Math.min(60, Math.floor((W * H) / 20000));
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * W, y: Math.random() * H,
        r: 0.8 + Math.random() * 1.8,
        vx: (Math.random() - 0.5) * 0.22,
        vy: (Math.random() - 0.5) * 0.22,
        alpha: 0.08 + Math.random() * 0.2,
        color: Math.random() > 0.5 ? '#6366f1' : '#06b6d4'
      });
    }
  }

  function frame() {
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const d  = Math.sqrt(dx * dx + dy * dy);
        if (d < 130) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(99,102,241,${0.05 * (1 - d / 130)})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
      if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.alpha;
      ctx.fill();
      ctx.globalAlpha = 1;
    });
    requestAnimationFrame(frame);
  }

  window.addEventListener('resize', resize);
  resize();
  frame();
})();

/* ─── Helpers ─────────────────────────────────────────────── */
function getDemoKey(url) {
  const u = url.toLowerCase();
  if (u.includes('flask'))                         return 'flask';
  if (u.includes('fastapi'))                       return 'fastapi';
  if (u.includes('react') && !u.includes('native')) return 'react';
  if (u.includes('pandas'))                        return 'pandas';
  if (u.includes('numpy'))                         return 'numpy';
  return null;
}

// Format confidence — API returns 0–100 (e.g. 94.0), display as "94.0%"
function fmtConf(c) {
  if (c == null) return '—';
  // If somehow a decimal 0-1 snuck in, multiply
  const val = c <= 1 ? c * 100 : c;
  return val.toFixed(1) + '%';
}

function fmt(n) {
  if (n == null || n === undefined) return '—';
  if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
  if (n >= 1000)    return (n / 1000).toFixed(1) + 'k';
  return String(Math.round(n));
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function healthBadgeClass(health) {
  if (health === 'Healthy')   return 'badge-healthy';
  if (health === 'Moderate')  return 'badge-moderate';
  return 'badge-unhealthy';
}

function showErrEl(el, msg) {
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
}

function escapeHtml(str) {
  return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
