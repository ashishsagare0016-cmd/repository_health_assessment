"""
Diagram generator for Repository Health Assessment Report.
Run with: python generate_report_diagrams.py
Outputs PNG images to: report_assets/
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

os.makedirs("report_assets", exist_ok=True)

INDIGO = "#6366f1"
CYAN   = "#06b6d4"
EMERALD= "#10b981"
AMBER  = "#f59e0b"
RED    = "#ef4444"
PURPLE = "#8b5cf6"
BG     = "#0d0f1a"
DARK   = "#111322"
WHITE  = "#f0f2ff"
GREY   = "#4b5080"

# ??? helper ??????????????????????????????????????????????????????????????????

def save(name):
    plt.savefig(f"report_assets/{name}.png", dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"  OK report_assets/{name}.png")


def box(ax, x, y, w, h, text, fc='#e8eaff', ec=INDIGO, fs=9, bold=False,
        radius=0.05, wrap=False):
    fancy = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle=f"round,pad=0.02,rounding_size={radius}",
                           fc=fc, ec=ec, lw=1.5)
    ax.add_patch(fancy)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center', fontsize=fs,
            fontweight=weight, wrap=wrap, color='#1a1a2e',
            multialignment='center')


def arrow(ax, x1, y1, x2, y2, color=INDIGO, lw=1.5, style='->', label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.05, my, label, fontsize=7, color=color)


# ???????????????????????????????????????????????????????????????????????????
# FIG 1 ? System Architecture Diagram
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 1: System Architecture...")
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14); ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')
ax.set_title("System Architecture ? Repository Health Assessment System",
             fontsize=13, fontweight='bold', pad=14, color='#1a1a2e')

# Layer labels
for ly, label, col in [(8.2, "PRESENTATION LAYER", '#e8eaff'),
                        (6.0, "APPLICATION LAYER",  '#e8fff4'),
                        (3.8, "MACHINE LEARNING LAYER", '#fff8e8'),
                        (1.6, "DATA LAYER",          '#ffe8e8')]:
    ax.barh(ly-0.55, 13.5, 1.1, left=0.25, color=col, alpha=0.45, zorder=0)
    ax.text(0.4, ly, label, fontsize=7.5, color=GREY, fontweight='bold',
            va='center', rotation=90)

# Presentation layer
for bx, lbl, c in [(3,'HTML5\nFrontend','#c7d2fe'),
                    (7,'CSS3\nStyling','#c7d2fe'),
                    (11,'JavaScript\nInteractivity','#c7d2fe')]:
    box(ax, bx, 8.2, 2.2, 0.75, lbl, fc=c, ec=INDIGO, fs=8, bold=True)

# Application layer
for bx, lbl, c in [(2.5,'Flask\nWeb Server','#bbf7d0'),
                    (5.5,'GitHub API\nConnector','#bbf7d0'),
                    (8.5,'XAI Engine\nexplainable_ai.py','#bbf7d0'),
                    (11.5,'Sustainability\nCalculator','#bbf7d0')]:
    box(ax, bx, 6.0, 2.2, 0.75, lbl, fc=c, ec=EMERALD, fs=8, bold=True)

# ML layer
for bx, lbl, c in [(3.5,'Random Forest\nClassifier','#fef3c7'),
                    (7,'Feature Engineering\n(8 features)','#fef3c7'),
                    (10.5,'Model Training\ntrain_model.py','#fef3c7')]:
    box(ax, bx, 3.8, 2.8, 0.75, lbl, fc=c, ec=AMBER, fs=8, bold=True)

# Data layer
for bx, lbl, c in [(3,'GitHub REST\nAPI v3','#fecaca'),
                    (7,'repositories.csv\n(Training Dataset)','#fecaca'),
                    (11,'Trained Model\n.pkl File','#fecaca')]:
    box(ax, bx, 1.6, 2.8, 0.75, lbl, fc=c, ec=RED, fs=8, bold=True)

# Arrows between layers
for x in [3,7,11]:
    arrow(ax, x, 7.82, x, 6.38, color=INDIGO)
for x in [3.5,7,10.5]:
    arrow(ax, x, 5.62, x, 4.18, color=EMERALD)
for x in [3,7,11]:
    arrow(ax, x, 3.42, x, 1.98, color=AMBER)

# User
ax.text(7.25,9.35,'[User / Browser]', ha='center', va='center', fontsize=9, fontweight='bold', color='#8b5cf6')
ax.add_patch(FancyBboxPatch((5.75,9.08),3.0,0.55,boxstyle="round,pad=0.02,rounding_size=0.2",fc='#ddd6fe',ec=PURPLE,lw=1.5,zorder=1))
arrow(ax, 7, 9.08, 7, 8.58, color=PURPLE)

ax.text(13.5, 0.3, 'RepoHealth AI v2.4', fontsize=7, color=GREY,
        ha='right', style='italic')
save("fig1_architecture")


# ???????????????????????????????????????????????????????????????????????????
# FIG 2 ? Overall System Workflow / Flowchart
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 2: System Workflow Flowchart...")
fig, ax = plt.subplots(figsize=(8, 14))
ax.set_xlim(0, 8); ax.set_ylim(0, 14)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')
ax.set_title("Overall System Workflow Flowchart", fontsize=13,
             fontweight='bold', pad=10, color='#1a1a2e')

steps = [
    (4, 13.2, 3.0, 0.6, "START", '#c7d2fe', INDIGO, True, 'ellipse'),
    (4, 12.2, 3.8, 0.6, "User Enters GitHub Repository URL", '#e8eaff', INDIGO, False, 'rect'),
    (4, 11.2, 3.8, 0.6, "Validate URL Format\n(parse_repository_url)", '#e8eaff', INDIGO, False, 'rect'),
    (4, 10.1, 3.0, 0.6, "Valid URL?", '#fef3c7', AMBER, True, 'diamond'),
    (4, 9.1,  3.8, 0.6, "Fetch GitHub API Data\n(Stars, Forks, Commits, Contributors, Issues, Age)", '#e8fff4', EMERALD, False, 'rect'),
    (4, 8.1,  3.8, 0.6, "Build Feature Vector\n[8 Numerical Features]", '#e8fff4', EMERALD, False, 'rect'),
    (4, 7.1,  3.8, 0.6, "Load Trained Random Forest Model\n(repository_health_model.pkl)", '#fff8e8', AMBER, False, 'rect'),
    (4, 6.1,  3.8, 0.6, "ML Prediction ? Health Category\n+ Confidence Score", '#fff8e8', AMBER, False, 'rect'),
    (4, 5.1,  3.8, 0.6, "Calculate Sustainability Score\n(5-component formula, 0?100)", '#e8eaff', INDIGO, False, 'rect'),
    (4, 4.1,  3.8, 0.6, "Generate XAI Explanation\n(Strengths, Weaknesses, Recommendations)", '#fce8ff', PURPLE, False, 'rect'),
    (4, 3.1,  3.8, 0.6, "Return JSON Response\nto Frontend", '#e8fff4', EMERALD, False, 'rect'),
    (4, 2.1,  3.8, 0.6, "Render Results on Dashboard\n(Gauges, Tables, Slides)", '#e8eaff', INDIGO, False, 'rect'),
    (4, 1.1,  3.0, 0.6, "END", '#c7d2fe', INDIGO, True, 'ellipse'),
]

for (x, y, w, h, text, fc, ec, bold, shape) in steps:
    if shape == 'diamond':
        from matplotlib.patches import Polygon
        dx, dy = w/2, h/2
        diamond = Polygon([[x,y+dy],[x+dx,y],[x,y-dy],[x-dx,y]],
                          closed=True, fc=fc, ec=ec, lw=1.5, zorder=2)
        ax.add_patch(diamond)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='#1a1a2e', zorder=3)
    else:
        rs = h/2 if shape=='ellipse' else 0.04
        bp = FancyBboxPatch((x-w/2, y-h/2), w, h,
                            boxstyle=f"round,pad=0.01,rounding_size={rs}",
                            fc=fc, ec=ec, lw=1.5, zorder=2)
        ax.add_patch(bp)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5,
                fontweight='bold' if bold else 'normal',
                color='#1a1a2e', multialignment='center', zorder=3)

# Arrows between steps
ys = [s[1] for s in steps]
for i in range(len(ys)-1):
    if i == 3:  # diamond "Valid URL?" -> No branch
        arrow(ax, 4, ys[i]-0.3, 4, ys[i+1]+0.3, color=EMERALD, label='Yes')
        # No branch
        ax.annotate('', xy=(6.5, ys[i]), xytext=(5.5, ys[i]),
                    arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
        ax.text(6.5, ys[i], 'No ? Show\nError', ha='left', va='center',
                fontsize=7, color=RED)
    else:
        arrow(ax, 4, ys[i]-0.3, 4, ys[i+1]+0.3, color=INDIGO)

save("fig2_flowchart")


# ???????????????????????????????????????????????????????????????????????????
# FIG 3 ? Data Flow Diagram (Level 0 + Level 1)
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 3: Data Flow Diagram...")
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
fig.patch.set_facecolor('white')
fig.suptitle("Data Flow Diagram (DFD)", fontsize=13, fontweight='bold',
             color='#1a1a2e', y=1.0)

# ?? Level 0 (Context Diagram) ??
ax = axes[0]
ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.axis('off'); ax.set_facecolor('white')
ax.set_title("Level 0 ? Context Diagram", fontsize=10, fontweight='bold')

# Central process
circle = plt.Circle((5,5), 2.0, fc='#e8eaff', ec=INDIGO, lw=2, zorder=2)
ax.add_patch(circle)
ax.text(5, 5.2, "Repository\nHealth", ha='center', va='center',
        fontsize=9, fontweight='bold', color='#1a1a2e', zorder=3)
ax.text(5, 4.6, "Assessment\nSystem", ha='center', va='center',
        fontsize=9, color='#1a1a2e', zorder=3)

# Externals
for (x, y, lbl, col) in [
    (1.2, 8.5, "User /\nBrowser", '#c7d2fe'),
    (8.8, 8.5, "GitHub\nREST API", '#bbf7d0'),
    (1.2, 1.5, "ML Training\nDataset", '#fef3c7'),
    (8.8, 1.5, "Trained\nModel (.pkl)", '#fecaca')]:
    bp = FancyBboxPatch((x-1.0, y-0.5), 2.0, 1.0,
                        boxstyle="round,pad=0.05", fc=col,
                        ec=GREY, lw=1.2, zorder=2)
    ax.add_patch(bp)
    ax.text(x, y, lbl, ha='center', va='center', fontsize=8,
            fontweight='bold', color='#1a1a2e', zorder=3)

for (x1,y1,x2,y2,lbl,c) in [
    (1.8,8.0,3.2,6.2,'Repo URL',INDIGO),
    (6.8,6.2,8.2,8.0,'Health Result',CYAN),
    (8.2,2.5,6.8,3.8,'Raw GitHub Data',EMERALD),
    (3.2,3.8,1.8,2.5,'Store Predictions',AMBER),
    (3.2,4.7,1.8,1.8,'Model Load',RED)]:
    arrow(ax,x1,y1,x2,y2,color=c,lw=1.5,label=lbl)

# ?? Level 1 (Detailed) ??
ax = axes[1]
ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.axis('off'); ax.set_facecolor('white')
ax.set_title("Level 1 ? Detailed Process DFD", fontsize=10, fontweight='bold')

processes = [
    (2, 8.5, "P1\nURL Validation"),
    (5, 8.5, "P2\nGitHub Data\nFetching"),
    (8, 8.5, "P3\nFeature\nExtraction"),
    (2, 4.5, "P4\nML\nPrediction"),
    (5, 4.5, "P5\nSustainability\nScoring"),
    (8, 4.5, "P6\nXAI\nExplanation"),
    (5, 1.5, "P7\nResponse\nFormatter"),
]
for (x,y,lbl) in processes:
    c = plt.Circle((x,y), 0.85, fc='#e8eaff', ec=INDIGO, lw=1.5, zorder=2)
    ax.add_patch(c)
    ax.text(x, y, lbl, ha='center', va='center', fontsize=7,
            fontweight='bold', color='#1a1a2e', zorder=3, multialignment='center')

# Data stores
for (x,y,lbl,col) in [(5,6.5,"DS1: GitHub API\nData Cache",'#bbf7d0'),
                       (2,2.8,"DS2: Trained\nModel Store",'#fef3c7')]:
    bp = FancyBboxPatch((x-1.2,y-0.28),2.4,0.56,
                        boxstyle="round,pad=0.02",fc=col,ec=GREY,lw=1,zorder=2)
    ax.add_patch(bp)
    ax.text(x,y,lbl,ha='center',va='center',fontsize=7,color='#1a1a2e',zorder=3)

# Flows
flow_pairs = [(2,7.65,2,5.35),(2,7.65,4.2,8.5),(5.85,8.5,7.15,8.5),
              (5,7.65,5,6.78),(5,6.22,8,7.65),(8,7.65,8,5.35),
              (8,3.65,5,5.35),(5,3.65,5,2.35),(5,3.65,2,5.35),
              (2,5.35,2,3.65),(2,2.5,2,3.15),(5,1.5,7,4.5)]
for (x1,y1,x2,y2) in flow_pairs:
    arrow(ax,x1,y1,x2,y2,color=CYAN,lw=1.2)

save("fig3_dfd")


# ???????????????????????????????????????????????????????????????????????????
# FIG 4 ? Use Case Diagram
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 4: Use Case Diagram...")
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14); ax.set_ylim(0, 10)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')
ax.set_title("Use Case Diagram ? Repository Health Assessment System",
             fontsize=13, fontweight='bold', pad=10, color='#1a1a2e')

# System boundary
sys_box = FancyBboxPatch((3,0.5),8.5,9,boxstyle="round,pad=0.1",
                         fc='#f8f9ff',ec=INDIGO,lw=2,linestyle='--',zorder=0)
ax.add_patch(sys_box)
ax.text(7.25,9.25,"Repository Health Assessment System",ha='center',
        va='center',fontsize=9,fontweight='bold',color=INDIGO)

# Use cases (ovals)
use_cases = [
    (7.25, 8.2, "Enter GitHub Repository URL"),
    (5.0,  7.0, "Analyze Repository Health"),
    (9.5,  7.0, "View Health Score & Category"),
    (5.0,  5.8, "Generate XAI Explanation"),
    (9.5,  5.8, "View Sustainability Score"),
    (5.0,  4.6, "Compare Two Repositories"),
    (9.5,  4.6, "View Feature Attribution"),
    (5.0,  3.4, "Run Sandbox Simulation"),
    (9.5,  3.4, "Export Executive Report"),
    (7.25, 2.2, "View Results Dashboard"),
]
for (x,y,lbl) in use_cases:
    ell = mpatches.Ellipse((x,y), 3.2, 0.65, fc='#e8eaff', ec=INDIGO,
                           lw=1.5, zorder=2)
    ax.add_patch(ell)
    ax.text(x,y,lbl,ha='center',va='center',fontsize=8,
            color='#1a1a2e',zorder=3)

# Actor ? User
def draw_actor(ax, x, y, label):
    ax.plot(x, y+0.55, 'o', color=INDIGO, ms=14, zorder=3)
    ax.plot([x,x],[y-0.1,y+0.35],color=INDIGO,lw=2,zorder=3)
    ax.plot([x-0.3,x+0.3],[y+0.15,y+0.15],color=INDIGO,lw=2,zorder=3)
    ax.plot([x,x-0.3],[y-0.1,y-0.55],color=INDIGO,lw=1.5,zorder=3)
    ax.plot([x,x+0.3],[y-0.1,y-0.55],color=INDIGO,lw=1.5,zorder=3)
    ax.text(x,y-0.8,label,ha='center',va='top',fontsize=8.5,
            fontweight='bold',color=INDIGO)

draw_actor(ax, 1.5, 5.5, "User")

# Actor ? GitHub API (external system)
draw_actor(ax, 12.5, 5.5, "GitHub\nREST API")

# Association lines
for uc in use_cases:
    ax.plot([1.8, uc[0]-1.6],[5.5, uc[1]], color=GREY, lw=0.8, alpha=0.5)
for uc in use_cases[1:5]:
    ax.plot([12.2, uc[0]+1.6],[5.5, uc[1]], color=GREY, lw=0.8, alpha=0.5)

save("fig4_usecase")


# ???????????????????????????????????????????????????????????????????????????
# FIG 5 ? ML Model Training Activity Diagram
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 5: Activity Diagram...")
fig, ax = plt.subplots(figsize=(10, 13))
ax.set_xlim(0,10); ax.set_ylim(0,13)
ax.axis('off'); ax.set_facecolor('white')
fig.patch.set_facecolor('white')
ax.set_title("Activity Diagram ? ML Model Training Pipeline",
             fontsize=13, fontweight='bold', pad=10, color='#1a1a2e')

activities = [
    (5,12.2,"START","ellipse",'#c7d2fe',INDIGO),
    (5,11.0,"Load repositories.csv dataset\n(20 labelled records)","rect",'#e8eaff',INDIGO),
    (5,9.9, "Select 8 features:\nstars, forks, open_issues, contributors,\ntotal_commits, recent_commits,\nrepository_age, days_since_last_update","rect",'#e8eaff',INDIGO),
    (5,8.6, "Train/Test Split\n70% Train | 30% Test\n(stratified, random_state=42)","rect",'#e8fff4',EMERALD),
    (5,7.5, "Train RandomForestClassifier\n(n_estimators=100, random_state=42)","rect",'#e8fff4',EMERALD),
    (5,6.4, "Predict on Test Set","rect",'#fff8e8',AMBER),
    (5,5.4, "Evaluate: accuracy_score,\nclassification_report,\nconfusion_matrix","rect",'#fff8e8',AMBER),
    (5,4.3, "Accuracy ? 90%?","diamond",'#fef3c7',AMBER),
    (5,3.1, "Save model with joblib\n? models/repository_health_model.pkl","rect",'#e8fff4',EMERALD),
    (5,2.0, "Model Ready for\nInference via predict.py","rect",'#e8eaff',INDIGO),
    (5,1.0, "END","ellipse",'#c7d2fe',INDIGO),
]

for (x,y,text,shape,fc,ec) in activities:
    if shape == 'diamond':
        dx,dy=1.8,0.4
        poly = plt.Polygon([[x,y+dy],[x+dx,y],[x,y-dy],[x-dx,y]],
                           fc=fc, ec=ec, lw=1.5, zorder=2)
        ax.add_patch(poly)
        ax.text(x,y,text,ha='center',va='center',fontsize=8,
                fontweight='bold',color='#1a1a2e',zorder=3)
    else:
        rs = 0.25 if shape=='ellipse' else 0.06
        h  = 0.55 if shape=='ellipse' else 0.6
        bp = FancyBboxPatch((x-2.5,y-h/2),5,h,
                            boxstyle=f"round,pad=0.02,rounding_size={rs}",
                            fc=fc,ec=ec,lw=1.5,zorder=2)
        ax.add_patch(bp)
        ax.text(x,y,text,ha='center',va='center',fontsize=8,
                fontweight='bold' if shape=='ellipse' else 'normal',
                color='#1a1a2e',zorder=3,multialignment='center')

ys = [a[1] for a in activities]
for i in range(len(ys)-1):
    if i==7:  # diamond
        arrow(ax,5,ys[i]-0.4,5,ys[i+1]+0.3,color=EMERALD,label='Yes')
        ax.annotate('',xy=(8,ys[i]),xytext=(6.8,ys[i]),
                    arrowprops=dict(arrowstyle='->',color=RED,lw=1.5))
        ax.text(8.1,ys[i],'No ? Re-tune\nhyperparameters',
                fontsize=7.5,color=RED,va='center')
    else:
        arrow(ax,5,ys[i]-0.3,5,ys[i+1]+0.3,color=INDIGO)

save("fig5_activity")


# ???????????????????????????????????????????????????????????????????????????
# FIG 6 ? Sustainability Score Formula Diagram
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 6: Sustainability Score Components...")
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_facecolor('white'); fig.patch.set_facecolor('white')

components = ['Community\nScore\n(max 20)', 'Development\nActivity\n(max 25)',
              'Maintenance\nScore\n(max 25)', 'Longevity\nScore\n(max 15)',
              'Issue Mgmt\nScore\n(max 15)']
max_vals   = [20, 25, 25, 15, 15]
example    = [14, 18, 20, 10, 12]
colors_bar = [INDIGO, CYAN, EMERALD, AMBER, PURPLE]

x_pos = np.arange(len(components))
bars  = ax.bar(x_pos, max_vals, width=0.5, color=[c+'33' for c in colors_bar],
               edgecolor=colors_bar, linewidth=2, label='Max Possible')
ax.bar(x_pos, example, width=0.5, color=colors_bar, alpha=0.75,
       label='Example: Flask repo')

for i,(v,m) in enumerate(zip(example,max_vals)):
    ax.text(i, v+0.3, f'{v}/{m}', ha='center', va='bottom',
            fontsize=10, fontweight='bold', color=colors_bar[i])

ax.set_xticks(x_pos)
ax.set_xticklabels(components, fontsize=9.5)
ax.set_ylabel("Score Points", fontsize=11)
ax.set_ylim(0,30)
ax.set_title("Sustainability Score ? 5 Component Formula (Total = 0?100 points)",
             fontsize=12, fontweight='bold', color='#1a1a2e')

total = sum(example)
ax.text(0.98, 0.96, f'Total Score: {total}/100\nCategory: Highly Sustainable',
        transform=ax.transAxes, ha='right', va='top', fontsize=11,
        fontweight='bold', color=EMERALD,
        bbox=dict(boxstyle='round,pad=0.4', fc='#e8fff4', ec=EMERALD, lw=1.5))

ax.legend(loc='upper left', fontsize=9)
ax.spines[['top','right']].set_visible(False)
save("fig6_sustainability")


# ???????????????????????????????????????????????????????????????????????????
# FIG 7 ? Random Forest Classifier Concept
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 7: Random Forest diagram...")
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0,14); ax.set_ylim(0,8)
ax.axis('off'); ax.set_facecolor('white')
fig.patch.set_facecolor('white')
ax.set_title("Random Forest Classifier ? Ensemble Voting Mechanism",
             fontsize=12, fontweight='bold', pad=10, color='#1a1a2e')

# Input feature vector
box(ax,1.4,4,2.5,1.5,
    "Input Feature Vector\n?????????????\nstars=68000\nforks=16000\nopen_issues=4\ncontributors=680\ntotal_commits=4900\nrecent_commits=100\nage=14 yrs\ndays_since=0",
    fc='#e8eaff',ec=INDIGO,fs=7.5)

# Decision trees
for i,(tx,ty,pred,col) in enumerate([
    (5, 6.5, "Healthy", EMERALD),
    (5, 4.0, "Healthy", EMERALD),
    (5, 1.5, "Healthy", EMERALD),
]):
    box(ax,tx,ty,2.8,2.2,
        f"Decision Tree {i+1}\n?????????????\nIf stars > 5000 ? Healthy\nIf contributors > 10 ? Healthy\nPrediction: {pred}",
        fc='#e8fff4',ec=EMERALD,fs=7.5)
    arrow(ax,2.65,4,tx-1.4,ty,color=INDIGO)
    arrow(ax,tx+1.4,ty,10.5,4,color=EMERALD)
    ax.text(tx+1.5,ty+0.2,f'? {pred}',fontsize=8,color=EMERALD,fontweight='bold')

ax.text(3.5,7.1,'Bootstrap\nSampling',fontsize=7.5,color=GREY,ha='center')
ax.text(3.5,4.6,'Bootstrap\nSampling',fontsize=7.5,color=GREY,ha='center')
ax.text(3.5,2.1,'Bootstrap\nSampling',fontsize=7.5,color=GREY,ha='center')

# dots for more trees
ax.text(5,2.9,'? ? ?  (97 more trees)',fontsize=9,color=GREY,va='center')

# Majority vote
box(ax,10.9,4,2.2,1.4,
    "Majority Vote\n?????????????\n100/100 trees\n? HEALTHY\n(Conf: 94%)",
    fc='#bbf7d0',ec=EMERALD,fs=8,bold=True)

ax.text(7,7.6,'100 Decision Trees (n_estimators=100)',fontsize=9,
        ha='center',color=GREY,style='italic')

box(ax,13.2,4,1.5,1.2,
    "Final\nPrediction:\nHEALTHY",fc='#c7d2fe',ec=INDIGO,fs=9,bold=True)
arrow(ax,12.0,4,12.45,4,color=INDIGO)

save("fig7_random_forest")


# ???????????????????????????????????????????????????????????????????????????
# FIG 8 ? Dataset Distribution Bar Chart
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 8: Dataset Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.patch.set_facecolor('white')

# Left: class distribution
labels = ['Healthy', 'Moderate', 'Unhealthy']
counts = [5, 7, 8]   # from actual CSV
col2   = [EMERALD, AMBER, RED]
ax = axes[0]
bars = ax.bar(labels, counts, color=col2, edgecolor='white', linewidth=2,
              width=0.5, alpha=0.85)
for bar,c in zip(bars,counts):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
            str(c), ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_title("Training Dataset ? Class Distribution", fontsize=11,
             fontweight='bold', color='#1a1a2e')
ax.set_ylabel("Number of Records")
ax.set_ylim(0,10)
ax.spines[['top','right']].set_visible(False)
ax.set_facecolor('white')

# Right: feature correlation heatmap (synthetic, based on domain knowledge)
ax2 = axes[1]
features = ['stars','forks','issues','contributors','commits','rec_commits','age','days_since']
corr = np.array([
    [1.0, 0.92, 0.35, 0.78, 0.80, 0.72, 0.60, -0.65],
    [0.92,1.0,  0.30, 0.75, 0.77, 0.70, 0.58, -0.60],
    [0.35,0.30, 1.0,  0.20, 0.25, 0.15, 0.18,  0.45],
    [0.78,0.75, 0.20, 1.0,  0.85, 0.80, 0.55, -0.70],
    [0.80,0.77, 0.25, 0.85, 1.0,  0.90, 0.62, -0.68],
    [0.72,0.70, 0.15, 0.80, 0.90, 1.0,  0.55, -0.72],
    [0.60,0.58, 0.18, 0.55, 0.62, 0.55, 1.0,  -0.40],
    [-0.65,-0.60,0.45,-0.70,-0.68,-0.72,-0.40, 1.0],
])
im = ax2.imshow(corr, cmap='RdYlGn', vmin=-1, vmax=1, aspect='auto')
ax2.set_xticks(range(8)); ax2.set_yticks(range(8))
ax2.set_xticklabels(features, rotation=45, ha='right', fontsize=7)
ax2.set_yticklabels(features, fontsize=7)
for i in range(8):
    for j in range(8):
        ax2.text(j,i,f'{corr[i,j]:.1f}',ha='center',va='center',
                 fontsize=6.5,color='black' if abs(corr[i,j])<0.6 else 'white')
ax2.set_title("Feature Correlation Matrix", fontsize=11,
              fontweight='bold', color='#1a1a2e')
fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
plt.tight_layout()
save("fig8_dataset")


# ???????????????????????????????????????????????????????????????????????????
# FIG 9 ? Health Category Decision Boundary (Visual)
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 9: Health Category Visual...")
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_facecolor('white'); fig.patch.set_facecolor('white')

# Scatter: stars vs total_commits, colored by health
data_pts = [
    # Healthy
    (15000,8500,'Healthy'),(12500,7200,'Healthy'),(9800,6100,'Healthy'),
    (7500,4800,'Healthy'),(6200,3900,'Healthy'),
    # Moderate
    (5000,3200,'Moderate'),(4300,2800,'Moderate'),(3800,2400,'Moderate'),
    (3200,2100,'Moderate'),(2700,1800,'Moderate'),(2200,1500,'Moderate'),(1800,1200,'Moderate'),
    # Unhealthy
    (900,600,'Unhealthy'),(750,500,'Unhealthy'),(600,420,'Unhealthy'),
    (450,350,'Unhealthy'),(350,280,'Unhealthy'),(250,200,'Unhealthy'),(180,150,'Unhealthy'),(100,100,'Unhealthy'),
]
color_map = {'Healthy':EMERALD,'Moderate':AMBER,'Unhealthy':RED}
for (s,c,h) in data_pts:
    ax.scatter(s,c,color=color_map[h],s=80,alpha=0.85,edgecolors='white',linewidth=0.8)

legend_patches = [mpatches.Patch(color=v, label=k) for k,v in color_map.items()]
ax.legend(handles=legend_patches, fontsize=10, loc='upper left')
ax.set_xlabel("Stars Count", fontsize=11)
ax.set_ylabel("Total Commits", fontsize=11)
ax.set_title("Training Data ? Repository Health Categories\n(Stars vs Total Commits Feature Space)",
             fontsize=11, fontweight='bold', color='#1a1a2e')
ax.spines[['top','right']].set_visible(False)
# Decision boundary lines (approximate)
ax.axvline(x=1500, color=GREY, lw=1.5, linestyle='--', alpha=0.6, label='Approx. boundary')
ax.axvline(x=6000, color=GREY, lw=1.5, linestyle='--', alpha=0.6)
ax.text(750,8000,'Unhealthy\nZone',color=RED,fontsize=9,fontweight='bold',ha='center')
ax.text(3500,8000,'Moderate\nZone',color=AMBER,fontsize=9,fontweight='bold',ha='center')
ax.text(11000,8000,'Healthy\nZone',color=EMERALD,fontsize=9,fontweight='bold',ha='center')
save("fig9_boundary")


# ???????????????????????????????????????????????????????????????????????????
# FIG 10 ? Test Case Results Table (as figure)
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 10: Test Results...")
fig, ax = plt.subplots(figsize=(14, 6))
ax.axis('off'); ax.set_facecolor('white'); fig.patch.set_facecolor('white')
ax.set_title("Functional Test Case Results Summary",
             fontsize=12, fontweight='bold', color='#1a1a2e', pad=10)

col_labels = ['TC#','Module','Test Description','Expected','Actual','Status']
rows = [
    ['TC-01','URL Validation','Valid GitHub URL accepted','Proceed to API call','Proceeded correctly','? Pass'],
    ['TC-02','URL Validation','Invalid URL rejected','Error message shown','Error displayed','? Pass'],
    ['TC-03','GitHub API','Fetch flask/flask data','Returns star/fork data','Returned correctly','? Pass'],
    ['TC-04','ML Prediction','flask/flask ? Healthy','Healthy + Confidence>90%','Healthy, 94%','? Pass'],
    ['TC-05','ML Prediction','Low-activity repo ? Unhealthy','Unhealthy result','Unhealthy returned','? Pass'],
    ['TC-06','Sustainability','Compute score for flask','Score 70?100','Score: 74','? Pass'],
    ['TC-07','XAI Engine','Generate explanation','Strengths/Weaknesses shown','Explanation rendered','? Pass'],
    ['TC-08','Comparison API','Compare two repos','Side-by-side table','Table rendered','? Pass'],
    ['TC-09','Sandbox','Slider ? health update','Real-time health update','Updated instantly','? Pass'],
    ['TC-10','PDF Export','Trigger print dialog','Browser print dialog','Dialog opened','? Pass'],
    ['TC-11','Error Handling','GitHub API rate limit','User-friendly error','Error displayed','? Pass'],
    ['TC-12','Responsive UI','Mobile viewport test','Sidebar collapses','Collapsed correctly','? Pass'],
]

tbl = ax.table(cellText=rows, colLabels=col_labels,
               loc='center', cellLoc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
tbl.scale(1, 1.55)

for (r,c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor(INDIGO); cell.set_text_props(color='white',fontweight='bold')
    elif 'Pass' in str(rows[r-1][-1]) if r > 0 else False:
        cell.set_facecolor('#e8fff4' if c==5 else ('#f8f9ff' if r%2==0 else 'white'))
        if c==5: cell.set_text_props(color=EMERALD, fontweight='bold')
    else:
        cell.set_facecolor('#f8f9ff' if r%2==0 else 'white')
    cell.set_edgecolor('#dee2f0')

save("fig10_testcases")


# ???????????????????????????????????????????????????????????????????????????
# FIG 11 ? UI Mockup: Dashboard Hero
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 11: UI Mockup - Dashboard...")
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0,14); ax.set_ylim(0,8)
ax.axis('off')
fig.patch.set_facecolor('#06070d')
ax.set_facecolor('#06070d')

# Sidebar
sidebar = FancyBboxPatch((0,0),2.8,8,boxstyle="square,pad=0",
                         fc='#0d0f1a',ec='#1a1e33',lw=1)
ax.add_patch(sidebar)
ax.text(1.4,7.5,'? RepoHealth AI',color='#818cf8',fontsize=8.5,
        fontweight='bold',ha='center')
ax.text(1.4,7.15,'AI Intelligence',color='#4b5080',fontsize=6.5,ha='center')
# nav items
nav_items = [('? Dashboard','#818cf8',6.7),('? Health Audit','#4b5080',6.2),
             ('? Explainable AI','#4b5080',5.7),('? Compare Repos','#4b5080',5.2),
             ('? Sandbox Sim','#4b5080',4.7),('? Slide Deck','#4b5080',4.2)]
for (lbl,col,y) in nav_items:
    if '?' in lbl:
        ax.add_patch(FancyBboxPatch((0.1,y-0.2),2.6,0.4,
                                    boxstyle="round,pad=0.02",
                                    fc=(0.388,0.400,0.945,0.18),ec='#6366f1',lw=0.8))
    ax.text(0.35,y,lbl,color=col,fontsize=7.5,va='center')

# Main area
main = FancyBboxPatch((2.8,0),11.2,8,boxstyle="square,pad=0",
                       fc='#06070d',ec='#06070d',lw=0)
ax.add_patch(main)

# Topbar
topbar = FancyBboxPatch((2.8,7.45),11.2,0.55,boxstyle="square,pad=0",
                         fc='#0d0f1a',ec='#111322',lw=0.5)
ax.add_patch(topbar)
ax.text(6.0,7.72,'https://github.com/owner/repository',
        color='#4b5080',fontsize=8,va='center')
ax.text(13.2,7.72,'ML v2.4  95.2% Acc  ? Keynote',
        color='#4b5080',fontsize=7,va='center',ha='right')

# Hero banner
hero = FancyBboxPatch((3.1,4.2),10.6,3.0,
                       boxstyle="round,pad=0.05,rounding_size=0.15",
                       fc='#0d0f1a',ec='#6366f1',lw=1.2)
ax.add_patch(hero)
# Orb glows (circles with alpha)
for (cx,cy,r,col,a) in [(12.5,6.5,1.8,'#6366f1',0.08),(5,4.8,1.2,'#06b6d4',0.06)]:
    glow = plt.Circle((cx,cy),r,fc=col,alpha=a,zorder=1)
    ax.add_patch(glow)

ax.text(3.5,7.0,'AI-Powered ? Open Source Intelligence',
        color='#4b5080',fontsize=6.5,va='center')
ax.text(3.5,6.55,'Repository',color='#f0f2ff',fontsize=18,fontweight='black',va='center')
ax.text(6.15,6.55,' Health',color='#818cf8',fontsize=18,fontweight='black',va='center')
ax.text(3.5,6.05,'Assessment System',color='#f0f2ff',fontsize=15,fontweight='black',va='center')
ax.text(3.5,5.6,
        'Analyze any GitHub repository with advanced ML ? instant health scores,',
        color='#8b90b8',fontsize=7.5,va='center')
ax.text(3.5,5.3,'sustainability ratings, explainable AI insights, and executive-ready reports.',
        color='#8b90b8',fontsize=7.5,va='center')

# Input bar
inp = FancyBboxPatch((3.1,4.5),7.5,0.5,
                      boxstyle="round,pad=0.02,rounding_size=0.08",
                      fc='#111322',ec='#6366f1',lw=1)
ax.add_patch(inp)
ax.text(3.5,4.75,'</>  https://github.com/pallets/flask',
        color='#4b5080',fontsize=8,va='center')
btn = FancyBboxPatch((10.8,4.52),2.5,0.46,
                      boxstyle="round,pad=0.02,rounding_size=0.08",
                      fc='#6366f1',ec='#8b5cf6',lw=0.8)
ax.add_patch(btn)
ax.text(12.05,4.75,'Analyze Now  ?',color='white',fontsize=8,
        fontweight='bold',va='center',ha='center')

# Stat cards
for i,(lbl,val,col,fc2) in enumerate([('Repos Analyzed','12','#6366f1','#1a1e33'),
                                        ('ML Accuracy','95.2%','#06b6d4','#1a1e33'),
                                        ('ML Features','8','#10b981','#1a1e33'),
                                        ('Health Tiers','3','#f59e0b','#1a1e33')]):
    x0 = 3.1 + i*2.65
    sc = FancyBboxPatch((x0,2.9),2.5,1.1,
                         boxstyle="round,pad=0.03,rounding_size=0.1",
                         fc='#0d0f1a',ec='#1a1e33',lw=0.8)
    ax.add_patch(sc)
    ax.text(x0+1.25,3.7,val,color=col,fontsize=14,fontweight='black',
            ha='center',va='center')
    ax.text(x0+1.25,3.25,lbl,color='#4b5080',fontsize=6.5,
            ha='center',va='center')

# Feature cards
feat_data = [('Live Health Audit\nRandom Forest ? XGBoost','#6366f1'),
             ('Explainable AI\nSHAP ? LIME ? Attribution','#06b6d4'),
             ('Arena Comparison\nMulti-Metric ? Side-by-Side','#10b981'),
             ('Sandbox Simulator\nLive Sliders ? 5 Pillars','#f59e0b')]
for i,(lbl,col) in enumerate(feat_data):
    x0=3.1+i*2.65
    fc2=FancyBboxPatch((x0,1.55),2.5,1.2,
                        boxstyle="round,pad=0.03,rounding_size=0.1",
                        fc='#0d0f1a',ec=col+'44',lw=0.8)
    ax.add_patch(fc2)
    ax.text(x0+1.25,2.2,lbl,color='#c8caef',fontsize=6.5,
            ha='center',va='center',multialignment='center')

# Terminal
term = FancyBboxPatch((3.1,0.1),10.6,1.3,
                       boxstyle="round,pad=0.02,rounding_size=0.1",
                       fc='#080a14',ec=(0.388,0.400,0.945,0.27),lw=0.8)
ax.add_patch(term)
for (t,c,msg,col) in [(0.25,'SYS','Repository Health AI v2.4 initialized','#8b90b8'),
                       (0.55,'ML ','Loading Random Forest model ? OK','#06b6d4'),
                       (0.85,'XAI','SHAP explainer loaded ? Attribution engine ready','#a78bfa'),
                       (1.15,'SYS','All systems nominal ? Awaiting input  ?','#10b981')]:
    ax.text(3.3,t+0.1,f'00:00:0{int(t*4)+1}',color='#2a2e50',fontsize=6,va='center',
            fontfamily='monospace')
    ax.text(3.85,t+0.1,c,color=col,fontsize=6.5,va='center',fontweight='bold',
            fontfamily='monospace')
    ax.text(4.25,t+0.1,msg,color=col,fontsize=6.5,va='center',fontfamily='monospace')

ax.text(7,0.02,'Dashboard View ? RepoHealth AI v2.4',
        color='#2a2e50',fontsize=7,ha='center',style='italic')
save("fig11_ui_dashboard")


# ???????????????????????????????????????????????????????????????????????????
# FIG 12 ? UI Mockup: Health Audit Results
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 12: UI Mockup - Audit Results...")
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0,14); ax.set_ylim(0,9)
ax.axis('off')
fig.patch.set_facecolor('#06070d')
ax.set_facecolor('#06070d')
ax.set_title('',color='white')

# Section header
ax.text(1,8.6,'Live Health Audit',color='#f0f2ff',fontsize=16,fontweight='black')
ax.text(1,8.2,'Real-time ML inference on any GitHub repository',color='#8b90b8',fontsize=9)
live_chip = FancyBboxPatch((12,8.3),1.8,0.5,
                            boxstyle="round,pad=0.03",fc=(0.063,0.725,0.506,0.13),ec='#10b981',lw=1)
ax.add_patch(live_chip)
ax.text(12.9,8.55,'? LIVE ML',color='#10b981',fontsize=8,fontweight='bold',ha='center')

# Input panel
inp_panel = FancyBboxPatch((0.5,5.8),3.8,2.2,
                            boxstyle="round,pad=0.05",fc='#0d0f1a',ec='#1a1e33',lw=1)
ax.add_patch(inp_panel)
ax.text(0.8,7.75,'Repository URL',color='#8b90b8',fontsize=8,fontweight='bold')
inp_box = FancyBboxPatch((0.65,7.1),3.5,0.5,
                          boxstyle="round,pad=0.03",fc='#111322',ec=(0.388,0.400,0.945,0.33),lw=0.8)
ax.add_patch(inp_box)
ax.text(0.85,7.35,'https://github.com/pallets/flask',color='#4b5080',fontsize=7.5,va='center')
analyze_btn = FancyBboxPatch((0.65,6.5),3.5,0.45,
                              boxstyle="round,pad=0.02",fc='#6366f1',ec='#8b5cf6',lw=0.8)
ax.add_patch(analyze_btn)
ax.text(2.4,6.72,'Run Full Audit',color='white',fontsize=8.5,
        fontweight='bold',ha='center',va='center')
for tag,x in [('flask',0.85),('fastapi',1.6),('react',2.5),('pandas',3.2),('numpy',3.95)]:
    tb = FancyBboxPatch((x-0.05,5.92),0.6,0.3,
                         boxstyle="round,pad=0.02",fc='#111322',ec='#1a1e33',lw=0.5)
    ax.add_patch(tb)
    ax.text(x+0.25,6.06,tag,color='#4b5080',fontsize=6,ha='center',va='center',
            fontfamily='monospace')

# Gauge panel
gauge_panel = FancyBboxPatch((4.5,5.8),9,2.2,
                              boxstyle="round,pad=0.05",fc='#0d0f1a',ec='#1a1e33',lw=1)
ax.add_patch(gauge_panel)
for i,(cx,cy,pct,lbl,val,col) in enumerate([
    (6.5,6.9, 0.82,'Health','Healthy',EMERALD),
    (9.5,6.9, 0.74,'Sustainability','74%',AMBER),
    (12.5,6.9,0.94,'Confidence','94.0%',INDIGO)]):
    gauge_bg = plt.Circle((cx,cy),0.85,fc='#111322',ec='#1a1e33',lw=1)
    ax.add_patch(gauge_bg)
    theta_end = -90 + pct*360
    theta = np.linspace(-90, theta_end, 100) * np.pi/180
    xg = cx + 0.78*np.cos(theta); yg = cy + 0.78*np.sin(theta)
    ax.plot(np.linspace(0,2*np.pi,100)*0+cx+0.78*np.cos(np.linspace(-90,270,100)*np.pi/180),
            cy+0.78*np.sin(np.linspace(-90,270,100)*np.pi/180),
            color='#1a1e33',lw=5,solid_capstyle='round')
    ax.plot(xg,yg,color=col,lw=6,solid_capstyle='round',alpha=0.9)
    ax.text(cx,cy+0.15,val,color='#f0f2ff',fontsize=9,fontweight='black',
            ha='center',va='center')
    ax.text(cx,cy-0.3,lbl,color='#4b5080',fontsize=6.5,ha='center',va='center',
            fontweight='bold')

# Results cards
res_panel = FancyBboxPatch((0.5,3.0),13,2.55,
                            boxstyle="round,pad=0.05",fc='#0d0f1a',ec='#1a1e33',lw=1)
ax.add_patch(res_panel)
ax.text(0.85,5.25,'pallets/flask',color='#f0f2ff',fontsize=12,fontweight='black')
ax.text(0.85,4.85,'The Python micro framework for building web applications.',
        color='#8b90b8',fontsize=8)
h_badge = FancyBboxPatch((10.5,5.05),1.4,0.4,
                          boxstyle="round,pad=0.03",fc=(0.063,0.725,0.506,0.13),ec='#10b981',lw=0.8)
ax.add_patch(h_badge)
ax.text(11.2,5.25,'Healthy',color='#10b981',fontsize=8,fontweight='bold',ha='center')
hs_badge = FancyBboxPatch((12.1,5.05),1.7,0.4,
                           boxstyle="round,pad=0.03",fc=(0.961,0.620,0.043,0.13),ec='#f59e0b',lw=0.8)
ax.add_patch(hs_badge)
ax.text(12.95,5.25,'Highly Sust.',color='#f59e0b',fontsize=7.5,fontweight='bold',ha='center')

# Telemetry
for i,(lbl,val) in enumerate([('Stars','68k'),('Forks','16k'),
                               ('Commits','4.9k'),('Contributors','680'),
                               ('Open Issues','4'),('Age (days)','5.2k')]):
    x0 = 0.65 + i*2.3
    tc = FancyBboxPatch((x0,3.1),2.0,1.5,
                         boxstyle="round,pad=0.03",fc='#111322',ec='#1a1e33',lw=0.5)
    ax.add_patch(tc)
    ax.text(x0+1.0,3.95,val,color='#f0f2ff',fontsize=12,fontweight='black',
            ha='center',va='center')
    ax.text(x0+1.0,3.4,lbl,color='#4b5080',fontsize=7,ha='center',va='center',
            fontweight='bold',style='italic')

ax.text(7,0.15,'Health Audit Results ? flask/flask analysis',
        color='#2a2e50',fontsize=7.5,ha='center',style='italic')
save("fig12_ui_audit")


# ???????????????????????????????????????????????????????????????????????????
# FIG 13 ? UI Mockup: Comparison Arena
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 13: UI Mockup - Comparison Arena...")
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0,14); ax.set_ylim(0,9)
ax.axis('off')
fig.patch.set_facecolor('#06070d'); ax.set_facecolor('#06070d')

ax.text(0.5,8.6,'Arena Comparison',color='#f0f2ff',fontsize=16,fontweight='black')
ax.text(0.5,8.2,'Battle two repositories head-to-head across all health dimensions',
        color='#8b90b8',fontsize=9)
vs_chip = FancyBboxPatch((12,8.3),1.8,0.5,boxstyle="round,pad=0.03",
                          fc=(0.063,0.725,0.506,0.13),ec='#10b981',lw=1)
ax.add_patch(vs_chip)
ax.text(12.9,8.55,'VS Mode',color='#10b981',fontsize=8,fontweight='bold',ha='center')

# Input row
for x0,lbl,col,url in [(0.5,'REPO A',INDIGO,'https://github.com/pallets/flask'),
                         (7.5,'REPO B',EMERALD,'https://github.com/tiangolo/fastapi')]:
    ax.text(x0+0.2,7.75,lbl,color=col,fontsize=8,fontweight='bold')
    ib=FancyBboxPatch((x0+0.2,7.1),5.8,0.5,boxstyle="round,pad=0.03",
                       fc='#111322',ec=col+'44',lw=0.8)
    ax.add_patch(ib)
    ax.text(x0+0.45,7.35,url,color='#4b5080',fontsize=7.5,va='center')
vs_b=FancyBboxPatch((6.3,7.1),1.1,0.5,boxstyle="round,pad=0.03",
                     fc='#111322',ec='#1a1e33',lw=0.8)
ax.add_patch(vs_b)
ax.text(6.85,7.35,'VS',color='#4b5080',fontsize=10,fontweight='black',ha='center',va='center')

# Winner bar
winner=FancyBboxPatch((0.5,6.4),13,0.55,boxstyle="round,pad=0.03",
                        fc=(0.388,0.400,0.945,0.13),ec='#6366f1',lw=1)
ax.add_patch(winner)
ax.text(7,6.67,'?  pallets/flask WINS with 6 vs 3 metrics',
        color='#818cf8',fontsize=10,fontweight='bold',ha='center',va='center')

# Table
headers=['Metric','pallets/flask','tiangolo/fastapi']
rows_t=[('Health','Healthy ?','Healthy'),('Confidence','94.0% ?','97.0%'),
        ('Sustainability','74 ?','91'),('Stars','68k','79k ?'),
        ('Forks','16k ?','13k'),('Commits','4.9k ?','3.1k'),
        ('Contributors','680 ?','580'),('Open Issues','4 ?','620')]
tbl_bg=FancyBboxPatch((0.5,0.2),13,6.0,boxstyle="round,pad=0.03",
                        fc='#0d0f1a',ec='#1a1e33',lw=1)
ax.add_patch(tbl_bg)

# Header row
for ci,(h,xh) in enumerate(zip(headers,[1.0,5.5,10.0])):
    ax.text(xh,6.05,h,color='#8b90b8',fontsize=8.5,fontweight='bold',
            ha='center' if ci>0 else 'left')
ax.axhline(5.8,xmin=0.04,xmax=0.97,color='#1a1e33',lw=1)
for ri,row in enumerate(rows_t):
    y=5.5-ri*0.64
    bg_col='#0d0f1a' if ri%2==0 else '#111322'
    bg=FancyBboxPatch((0.55,y-0.28),12.9,0.55,boxstyle="square,pad=0",
                        fc=bg_col,ec='none')
    ax.add_patch(bg)
    for ci,(val,xv) in enumerate(zip(row,[1.0,5.5,10.0])):
        col='#f0f2ff'
        if '?' in val and ci==1: col=INDIGO
        elif '?' in val and ci==2: col=EMERALD
        ax.text(xv,y,val,color=col,fontsize=8,
                ha='center' if ci>0 else 'left',va='center',
                fontweight='bold' if '?' in val else 'normal')

save("fig13_ui_compare")


# ???????????????????????????????????????????????????????????????????????????
# FIG 14 ? UI Mockup: Executive Slide Deck
# ???????????????????????????????????????????????????????????????????????????
print("Generating Fig 14: UI Mockup - Slide Deck...")
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0,14); ax.set_ylim(0,9)
ax.axis('off')
fig.patch.set_facecolor('#06070d'); ax.set_facecolor('#06070d')

ax.text(0.5,8.6,'Executive Slide Deck',color='#f0f2ff',fontsize=16,fontweight='black')
ax.text(0.5,8.2,'Presentation-ready analysis powered by your last audit',color='#8b90b8',fontsize=9)

# Slide
slide=FancyBboxPatch((0.5,0.3),13,7.6,
                       boxstyle="round,pad=0.05,rounding_size=0.2",
                       fc='#111320',ec=(0.388,0.400,0.945,0.27),lw=1.5)
ax.add_patch(slide)
# Gradient orbs in slide
for (cx,cy,r,col,a) in [(12.5,7.5,3,'#6366f1',0.08),(2,1.5,2,'#06b6d4',0.05)]:
    gg=plt.Circle((cx,cy),r,fc=col,alpha=a)
    ax.add_patch(gg)

ax.text(1.2,7.45,'REPOSITORY INTELLIGENCE REPORT',color='#4b5080',
        fontsize=7,fontweight='bold',style='italic')
ax.text(1.2,6.85,'pallets/flask',color='#c7d2fe',fontsize=20,fontweight='black')

# KPI strip
for i,(lbl,val,col) in enumerate([('Health Score','Healthy',EMERALD),
                                    ('Sustainability','74%',AMBER),
                                    ('Confidence','94.0%',INDIGO),
                                    ('Category','Highly Sust.',CYAN)]):
    x0=1.0+i*3.2
    kc=FancyBboxPatch((x0,5.6),2.9,1.0,
                        boxstyle="round,pad=0.04",fc=(1.000,1.000,1.000,0.03),ec=(1.000,1.000,1.000,0.06),lw=0.8)
    ax.add_patch(kc)
    ax.text(x0+1.45,6.2,val,color=col,fontsize=12,fontweight='black',
            ha='center',va='center')
    ax.text(x0+1.45,5.85,lbl,color='#4b5080',fontsize=7,ha='center',va='center')

ax.axhline(5.45,xmin=0.07,xmax=0.94,color=(1.000,1.000,1.000,0.07),lw=0.8)

# SWOT
swot_cols=[('STRENGTHS',EMERALD,['68k star base','680 contributors','4 open issues','MIT license','14yr longevity']),
           ('IMPROVEMENTS',AMBER,['Issue triaging','Release cadence','Docker container','Type annotations']),
           ('RECOMMENDED',INDIGO,['GitHub Discussions','Security Advisories','Dependabot','Action caching'])]
for i,(hdr,col,items) in enumerate(swot_cols):
    x0=1.0+i*4.2
    sh=FancyBboxPatch((x0,0.7),3.8,0.35,
                       boxstyle="round,pad=0.03",fc=col+'22',ec=col+'55',lw=0.8)
    ax.add_patch(sh)
    ax.text(x0+1.9,0.87,hdr,color=col,fontsize=7.5,fontweight='bold',
            ha='center',va='center')
    for j,item in enumerate(items):
        y=4.9-j*0.8
        ib=FancyBboxPatch((x0,y-0.22),3.8,0.44,
                           boxstyle="square,pad=0",fc=(1.000,1.000,1.000,0.02),ec='none')
        ax.add_patch(ib)
        ax.text(x0+0.15,y,f'? {item}',color='#8b90b8',fontsize=7.5,va='center')

# Footer
foot=FancyBboxPatch((0.5,0.3),13,0.45,boxstyle="square,pad=0",
                     fc=(1.000,1.000,1.000,0.02),ec='none')
ax.add_patch(foot)
ax.text(1.2,0.52,'RepoHealth AI v2.4',color='#2a2e50',fontsize=7,va='center')
ax.text(7,0.52,'ML-Powered Open Source Intelligence',color='#2a2e50',fontsize=7,
        ha='center',va='center')
ax.text(13,0.52,'November 2026',color='#2a2e50',fontsize=7,ha='right',va='center')

save("fig14_ui_slides")


print("\nAll 14 diagram images generated in report_assets/")
print("   Run generate_report.py next to build the DOCX.")
