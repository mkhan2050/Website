from pathlib import Path
from typing import Optional
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="Muneeb Khan — Resume", page_icon="💼", layout="wide")

# ======================== THEME / CSS (BLACK + RED) =========================
CSS = """
<style>
:root{
  --bg1:#0a0a0c;          /* near black */
  --bg2:#111114;          /* card background */
  --text:#f5f5f6;         /* primary text */
  --muted:#ababaf;        /* secondary text */
  --primary:#ef4444;      /* red */
  --primary-2:#f87171;    /* light red */
  --chip-bg: rgba(255,255,255,.05);
  --card:#0f0f12;
  --shadow: 0 10px 30px rgba(239,68,68,.18), 0 0 40px rgba(239,68,68,.08);
}

html, body, .block-container {
  background:
    radial-gradient(1000px 500px at 0% -10%, rgba(239,68,68,.06), transparent 60%),
    radial-gradient(1000px 500px at 100% 0%, rgba(248,113,113,.06), transparent 60%),
    var(--bg1);
  color: var(--text);
}
.block-container{padding-top:4.5rem;}

/* ---------------- NAVBAR ---------------- */
.navbar{
  position:fixed; top:0; left:0; right:0; height:64px;
  background:linear-gradient(180deg, rgba(17,17,20,.85), rgba(17,17,20,.55));
  backdrop-filter: blur(8px);
  border-bottom:1px solid rgba(255,255,255,.06);
  display:flex; align-items:center; justify-content:space-between;
  padding:0 24px; z-index:9999;
}
.nav-left{
  font-size:1.5rem; font-weight:800;
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-2) 60%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.nav-links{display:flex; gap:28px; align-items:center;}
.nav-link a{color:var(--text); text-decoration:none; opacity:.85; font-weight:600;}
.nav-link a:hover{opacity:1; text-shadow:0 0 10px rgba(239,68,68,.6);}
.nav-cta{ padding:8px 14px; border-radius:10px; font-weight:700;
  background:linear-gradient(135deg, var(--primary), var(--primary-2));
  color:#130a0a; text-decoration:none; box-shadow: var(--shadow); }

/* ---------------- REUSABLE ---------------- */
.card{
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.02));
  border:1px solid rgba(255,255,255,.08);
  border-radius:18px; padding:22px; box-shadow: var(--shadow);
}
.card-outline{
  border:1px solid rgba(239,68,68,.40);
  box-shadow: 0 0 0 2px rgba(239,68,68,.18), inset 0 0 40px rgba(239,68,68,.05);
  border-radius:18px; padding:26px; background:rgba(0,0,0,.35);
}
.section-title{ font-size:2.2rem; font-weight:800; margin:0 0 .6rem 0; }
.rule{ height:4px; width:140px; border-radius:999px; background: linear-gradient(90deg, var(--primary), transparent); }

.chips{display:flex; flex-wrap:wrap; gap:12px; margin-top:14px;}
.chip{
  display:inline-flex; align-items:center; gap:8px;
  padding:10px 14px; border-radius:14px;
  background: radial-gradient(120px 60px at 30% 20%, rgba(239,68,68,.14), var(--chip-bg));
  border:1px solid rgba(255,255,255,.08); font-weight:600; color:var(--text);
  box-shadow: var(--shadow);
}
.badge{font-size:.85rem; color:var(--muted);}
.muted{color:var(--muted);}
.mt-2{margin-top:.5rem;} .mt-4{margin-top:1rem;} .mt-6{margin-top:1.5rem;}
.small{font-size:.9rem;}

/* ---------------- HERO ---------------- */
.hero{
  display:grid; gap:28px; align-items:center;
  grid-template-columns: 220px minmax(0,1fr);
}
@media (max-width: 820px){
  .hero{ grid-template-columns: 1fr; }
}

.avatar{
  width:220px; height:220px; border-radius:9999px; object-fit:cover;
  box-shadow: 0 10px 30px rgba(239,68,68,.25), 0 0 0 3px rgba(248,113,113,.35) inset;
  background: radial-gradient(60% 60% at 50% 50%, rgba(239,68,68,.05), transparent);
}
.avatar-fallback{
  width:220px; height:220px; border-radius:9999px;
  display:flex; align-items:center; justify-content:center; font-weight:900; font-size:48px;
  color:#ffd7d7; background:radial-gradient(60% 60% at 50% 50%, rgba(239,68,68,.08), rgba(239,68,68,.02));
  box-shadow: 0 10px 30px rgba(239,68,68,.25), 0 0 0 3px rgba(248,113,113,.35) inset;
}

.hero-card{
  border:1px solid rgba(239,68,68,.45);
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  border-radius:18px; padding:24px;
  box-shadow: 0 25px 60px rgba(0,0,0,.45), 0 0 0 2px rgba(239,68,68,.18);
}
.hero-title{
  font-size:2.2rem; font-weight:900; line-height:1.25;
  background: linear-gradient(90deg, var(--primary), var(--primary-2));
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
.hero-desc{ font-size:1.1rem; color:var(--text); line-height:1.6; max-width:70ch; }
.hero-desc .em{ font-weight:800; color:#fff; }

/* quick links */
.quick-links{ display:flex; gap:12px; flex-wrap:wrap; margin-top:14px; }
.btn{
  display:inline-flex; align-items:center; gap:8px; padding:10px 14px; border-radius:12px;
  text-decoration:none; font-weight:700; color:#130a0a;
  background:linear-gradient(135deg, var(--primary), var(--primary-2));
  box-shadow: var(--shadow);
}
.btn.secondary{
  color:var(--text); background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.1);
}
.btn:hover{ filter:brightness(1.05); }

/* ---------------- MARQUEE (coursework) ---------------- */
.marquee{ position:relative; overflow:hidden; width:100%; }
.marquee__track{
  display:flex; gap:14px; align-items:center; padding:10px 0;
  animation: marquee-scroll 24s linear infinite; will-change: transform;
}
.marquee:hover .marquee__track{ animation-play-state: paused; }
.marquee .chip{
  white-space:nowrap; padding:10px 16px; border-radius:16px;
  background: radial-gradient(120px 60px at 30% 20%, rgba(239,68,68,.16), var(--chip-bg));
  border:1px solid rgba(255,255,255,.08);
  box-shadow: 0 6px 22px rgba(239,68,68,.12), 0 0 24px rgba(239,68,68,.08);
}
.marquee__fade{
  position:absolute; top:0; bottom:0; width:80px; pointer-events:none; z-index:2;
  background: linear-gradient(to right, var(--bg1), rgba(10,10,12,0));
}
.marquee__fade.right{ right:0; transform: scaleX(-1); }
@keyframes marquee-scroll{ 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ============================ NAVBAR ============================
st.markdown("""
<div class="navbar">
  <div class="nav-left">Muneeb Khan</div>
  <div class="nav-links">
    <div class="nav-link"><a href="#home">Home</a></div>
    <div class="nav-link"><a href="#experience">Experience</a></div>
    <div class="nav-link"><a href="#projects">Projects</a></div>
    <div class="nav-link"><a href="#education">Education</a></div>
    <div class="nav-link"><a href="#skills">Skills</a></div>
    <a class="nav-cta" href="#contact">Contact</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================ DATA ============================
DATA = {
  "contact": {
    "name": "Muneeb Khan",
    "citizenship": "US Citizen",
    "email": "khan.529@buckeyemail.osu.edu",
    "phone": "614-812-7692",
    "linkedin": "https://www.linkedin.com/in/muneeb-khan-3090a6290/",
    "github": "https://github.com/mkhan2050",
    "city": "Columbus, Ohio",
    "headshot": "headshot_mk.jpg"
  },
  "hero": {
    "headline": "B.S. in Computer Science & Engineering",
    "subline": "Building scalable, secure solutions across software, cloud, and AI.",
    "description": """
I'm a Computer Science & Engineering student at <span class='em'>Ohio State University</span>, passionate about designing impactful systems that blend modern web platforms, AI, and robust security.

I turn complex problems into clean, reliable products and thrive on learning from real-world feedback.
"""
  },
  "education": {
    "school": "The Ohio State University, Columbus, Ohio",
    "degree": "B.S. in Computer Science and Engineering",
    "deans_list": "Dean’s List (>3.5 GPA)",
    "grad": "Expected Graduation, May 2026",
    "coursework": [
      "Fundamentals of Engineering", "Calculus 1", "Engineering Calculus",
      "Linear Algebra", "Differential Equations", "Physics Kinematics & Motion",
      "Electrical Circuits Physics", "C++", "Python", "Java",
      "Software 2", "Engineering Statistics"
    ],
    "certs": ["JPMorgan Chase & Co — Software Engineering Job Simulation"]
  },
  "experience": [
    {
      "role": "Student IT Assistant – Pathology",
      "org": "The Ohio State University College of Medicine",
      "place": "Columbus, Ohio",
      "period": "May 2025 – July 2025",
      "points": [
        "Configured and troubleshot pathology lab workstations and servers supporting digital pathology software.",
        "Pre-processed 10,000+ whole slide images (WSIs) for AI training; improved dataset standardization.",
        "Automated scripts for annotation/feature extraction, reducing manual labeling by 20%."
      ]
    },
    {
      "role": "Undergraduate Research Assistant",
      "org": "The Ohio State University College of Medicine",
      "place": "Columbus, Ohio",
      "period": "Dec 2023 – Feb 2024",
      "points": [
        "Analyzed cardiomyocyte activity datasets, automating repetitive tasks to save 8 hours/week.",
        "Built visualization tools improving interpretation speed by 25%.",
        "Streamlined data access pipelines, cutting prep time by 10%."
      ]
    },
    {
      "role": "Software Developer Intern",
      "org": "Fee Dodger LLC",
      "place": "Columbus, Ohio",
      "period": "Mar 2024 – Present",
      "points": [
        "Designed & integrated APIs, projected to save 10+ hours/month of manual inventory tracking.",
        "Led iOS/Android feature development for 100+ early adopters.",
        "Ran beta sessions; shipped 30+ UX and navigation improvements pre-launch."
      ]
    },
    {
      "role": "Student IT Assistant — Engineering Technology Services",
      "org": "The Ohio State University College of Engineering",
      "place": "Columbus, Ohio",
      "period": "Jul 2024 – Present",
      "points": [
        "Investigated & resolved cybersecurity incidents with CrowdStrike (200+ devices).",
        "Configured networking gear (routers/switches) to boost departmental performance.",
        "Collaborated on infra hardening, reducing vulnerabilities by 20%."
      ]
    }
  ],
  "projects": [
    {
      "name": "Chatbot with Sentiment Analysis",
      "period": "Aug 2024 – Sep 2024",
      "points": [
        "Rasa/Dialogflow chatbot; VADER + BERT for sentiment (92% accuracy).",
        "Customizable templates; Flask deployment for scalability."
      ]
    },
    {
      "name": "To-Do List App (React)",
      "period": "Oct 2024 – Nov 2024",
      "points": [
        "Responsive CRUD with smooth state management.",
        "Local storage persistence for ~20 tasks/session; user-tested UI."
      ]
    },
    {
      "name": "AI-Powered Predictive Maintenance",
      "period": "Nov 2024 – Dec 2024",
      "points": [
        "Python + Scikit-learn/TensorFlow on vehicle sensor data (95% accuracy).",
        "Anomaly detection for engine/brake/tire health; analytics via Plotly Dash."
      ]
    }
  ],
  "activities": [
    {
      "name": "NAIMA — Youth Coordinator",
      "place": "Columbus, Ohio",
      "period": "Aug 2021 – Current",
      "points": [
        "Led youth-oriented programs for community development in a non-profit."
      ]
    },
    {
      "name": "Clubs — The Ohio State University",
      "place": "Columbus, Ohio",
      "period": "Aug 2023 – Current",
      "points": [
        "AI Club, Collaborative Software Development Club, Competitive Coding Club."
      ]
    }
  ],
  "skills": {
    "Programming": ["Java", "Python", "HTML/CSS", "JavaScript", "Node.js", "React.js", "MATLAB", "C++", "R"],
    "Tools": ["IntelliJ", "PyCharm", "Eclipse", "SolidWorks", "Webstorm", "MS Office"],
    "Non-Technical": ["Solution Oriented", "Skilled Collaborator", "Time Efficient", "Communication", "Critical Thinking"]
  }
}

# ============================ HELPERS ============================
def find_headshot(preferred: str) -> Optional[str]:
  """Return a path string to the headshot, trying common case/extension variants."""
  if not preferred:
    return None
  p = Path(preferred)
  candidates = [
    p,
    p.with_suffix(".JPG"), p.with_suffix(".JPEG"), p.with_suffix(".png"), p.with_suffix(".PNG"),
    Path("headshot.jpg"), Path("headshot.JPG"), Path("headshot.jpeg"), Path("headshot.PNG"),
    Path("headshot_mk.jpg"), Path("headshot_mk.JPG"), Path("headshot_mk.jpeg"),
  ]
  candidates += list(Path(".").glob("headshot*.*"))
  for c in candidates:
    if c.exists():
      return c.as_posix()
  return None

def chips(items):
  st.markdown("<div class='chips'>" + "".join(f"<div class='chip'>{i}</div>" for i in items) + "</div>", unsafe_allow_html=True)

def marquee_chips(items, seconds: float = 26):
  doubled = items + items
  chips_html = "".join(f"<div class='chip'>{i}</div>" for i in doubled)
  st.markdown(
    f"""
    <div class="marquee">
      <div class="marquee__fade"></div>
      <div class="marquee__fade right"></div>
      <div class="marquee__track" style="animation-duration:{float(seconds)}s">
        {chips_html}
      </div>
    </div>
    """,
    unsafe_allow_html=True
  )


# ============================ HERO (TOP) ============================
st.markdown('<a id="home"></a>', unsafe_allow_html=True)
img_src = find_headshot(DATA["contact"]["headshot"])
avatar_html = f"<img src='{img_src}' class='avatar'/>" if img_src else "<div class='avatar-fallback'>MK</div>"

st.markdown(
  dedent(f"""
  <div class="hero">
    <div>{avatar_html}</div>
    <div class="hero-card">
      <div class="hero-title">{DATA["hero"]["headline"]}</div>
      <div class="muted mt-2">{DATA["hero"]["subline"]}</div>
      <div class="hero-desc mt-4">{DATA['hero']['description']}</div>
      <div class="quick-links">
        <a class="btn" href="{DATA['contact']['linkedin']}" target="_blank">🔗 LinkedIn</a>
        <a class="btn" href="{DATA['contact']['github']}" target="_blank">💻 GitHub</a>
        <a class="btn secondary" href="mailto:{DATA['contact']['email']}">✉️ Email</a>
      </div>
      <div class="mt-4">
        <span class="badge">📍 {DATA['contact']['city']}</span> &nbsp;&nbsp;
        <span class="badge">📞 {DATA['contact']['phone']}</span> &nbsp;&nbsp;
        <span class="badge">✉️ <a href="mailto:{DATA['contact']['email']}" style="color:inherit;text-decoration:none">{DATA['contact']['email']}</a></span>
      </div>
    </div>
  </div>
  """),
  unsafe_allow_html=True
)


# ============================ EDUCATION ============================
st.markdown('<a id="education"></a>', unsafe_allow_html=True)
st.markdown("<div class='section-title mt-6'>Education</div>", unsafe_allow_html=True)
st.markdown(
  f"<div class='card'><strong>{DATA['education']['school']}</strong><br/>{DATA['education']['degree']}<br/>"
  f"<span class='muted'>{DATA['education']['grad']} · {DATA['education']['deans_list']}</span></div>",
  unsafe_allow_html=True
)
st.markdown("**Related Coursework**")
marquee_chips(DATA["education"]["coursework"], seconds=26)
st.markdown("**Certifications**")
for c in DATA["education"]["certs"]:
  st.markdown(f"- {c}")

# ============================ EXPERIENCE ============================
st.markdown('<a id="experience"></a>', unsafe_allow_html=True)
st.markdown("<div class='section-title mt-6'>Experience</div>", unsafe_allow_html=True)
for e in DATA["experience"]:
  st.markdown(
    f"<div class='card'><div style='display:flex;justify-content:space-between;align-items:center;'>"
    f"<div><strong>{e['role']}</strong> · {e['org']} — <span class='muted'>{e['place']}</span></div>"
    f"<div class='muted'>{e['period']}</div></div></div>",
    unsafe_allow_html=True
  )
  for p in e["points"]:
    st.markdown(f"- {p}")

# ============================ PROJECTS ============================
st.markdown('<a id="projects"></a>', unsafe_allow_html=True)
st.markdown("<div class='section-title mt-6'>Projects</div>", unsafe_allow_html=True)
for p in DATA["projects"]:
  st.markdown(
    f"<div class='card-outline'><div style='display:flex;justify-content:space-between;align-items:center;'>"
    f"<div style='font-weight:700;font-size:1.05rem'>{p['name']}</div>"
    f"<div class='muted'>{p['period']}</div></div></div>",
    unsafe_allow_html=True
  )
  for b in p["points"]:
    st.markdown(f"- {b}")

# ============================ ACTIVITIES ============================
st.markdown('<a id="activities"></a>', unsafe_allow_html=True)
st.markdown("<div class='section-title mt-6'>Activities & Leadership</div>", unsafe_allow_html=True)
for a in DATA["activities"]:
  st.markdown(
    f"<div class='card'><div style='display:flex;justify-content:space-between;align-items:center;'>"
    f"<div><strong>{a['name']}</strong> — <span class='muted'>{a['place']}</span></div>"
    f"<div class='muted'>{a['period']}</div></div></div>",
    unsafe_allow_html=True
  )
  for b in a["points"]:
    st.markdown(f"- {b}")

# ============================ SKILLS ============================
st.markdown('<a id="skills"></a>', unsafe_allow_html=True)
st.markdown("<div class='section-title mt-6'>Skills</div>", unsafe_allow_html=True)
tabs = st.tabs(list(DATA["skills"].keys()))
for tab, key in zip(tabs, DATA["skills"].keys()):
  with tab:
    chips(DATA["skills"][key])

# ============================ CONTACT ============================
st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
st.markdown("<div class='section-title mt-6'>Contact</div>", unsafe_allow_html=True)
st.markdown(f"**Email:** [{DATA['contact']['email']}](mailto:{DATA['contact']['email']})")
st.markdown(f"**Phone:** {DATA['contact']['phone']}")
st.markdown(f"**Location:** {DATA['contact']['city']}")
st.markdown(f"**LinkedIn:** {DATA['contact']['linkedin']}")
st.markdown(f"**GitHub:** {DATA['contact']['github']}")

st.markdown("<div class='muted mt-6 small'>Built with Streamlit • Black + Red theme</div>", unsafe_allow_html=True)
