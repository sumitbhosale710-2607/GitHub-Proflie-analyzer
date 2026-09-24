import streamlit as st
import html
import re
from github_api import get_user, get_repos, get_events
from analyzer import (
    get_top_languages, get_top_repos, get_recently_updated,
    get_total_stars, get_total_forks, calculate_score, account_age_years
)
from charts import language_pie_chart, top_repos_bar_chart, score_gauge, score_breakdown_bar


# ── Security helpers ───────────────────────────────────────────────────────────
def validate_username(username):
    """
    Validate GitHub username strictly.
    Rules: 1-39 chars, alphanumeric + hyphens only,
    cannot start or end with a hyphen, no consecutive hyphens.
    """
    if not username:
        return False, "Please enter a username."
    if len(username) > 39:
        return False, "GitHub usernames cannot exceed 39 characters."
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$', username):
        return False, "Invalid username. Only letters, numbers, and hyphens allowed. Cannot start or end with a hyphen."
    if '--' in username:
        return False, "Invalid username. Consecutive hyphens are not allowed."
    return True, None


def s(text):
    """
    Escape any user-provided text before inserting into HTML.
    Prevents XSS — even if a GitHub bio contains <script> tags,
    they will be rendered as plain text, not executed.
    """
    if text is None:
        return ""
    return html.escape(str(text))

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GitHub Profile Analyzer",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Animations & CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

/* ── Keyframes ── */
@keyframes gradientShift {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
}
@keyframes twinkle {
    0%, 100% { opacity: 0.1; transform: scale(0.6); }
    50%       { opacity: 0.9; transform: scale(1.1); }
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInLeft {
    from { opacity: 0; transform: translateX(-24px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    from { opacity: 0; transform: translateX(24px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 12px rgba(124,58,237,0.4), 0 0 24px rgba(124,58,237,0.2); }
    50%       { box-shadow: 0 0 28px rgba(167,139,250,0.8), 0 0 56px rgba(124,58,237,0.5), 0 0 80px rgba(79,70,229,0.3); }
}
@keyframes borderRotate {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}
@keyframes scoreReveal {
    from { width: 0%; }
    to   { width: var(--score-pct); }
}
@keyframes typingCursor {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
}
@keyframes floatUp {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
}
@keyframes ripple {
    0%   { transform: scale(1);   opacity: 0.6; }
    100% { transform: scale(2.5); opacity: 0; }
}
@keyframes scanline {
    0%   { top: -10%; }
    100% { top: 110%; }
}
@keyframes numberCount {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: radial-gradient(ellipse at 20% 20%, #1a0533 0%, #0D0D1A 40%, #090915 70%, #0D0D1A 100%);
    min-height: 100vh;
}

/* ── Animated title ── */
.main-title {
    font-family: 'Fira Code', monospace;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(270deg, #7C3AED, #A78BFA, #4F46E5, #C4B5FD, #7C3AED);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease infinite;
    text-align: center;
    letter-spacing: -0.5px;
}
.sub-title {
    text-align: center;
    color: #6B7280;
    font-size: 1rem;
    margin-bottom: 2rem;
    animation: fadeInUp 0.8s ease 0.3s both;
}

/* ── Glowing divider ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #7C3AED, #A78BFA, #7C3AED, transparent);
    margin: 1.5rem 0;
    border: none;
    animation: gradientShift 3s ease infinite;
    background-size: 200% 200%;
}

/* ── Profile card ── */
.profile-card {
    background: linear-gradient(135deg, rgba(26,5,51,0.9), rgba(45,26,74,0.9));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    animation: fadeInUp 0.6s ease both;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
.profile-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #A78BFA, transparent);
    animation: scanline 3s linear infinite;
}

/* ── Avatar glow ── */
.avatar-wrapper {
    position: relative;
    display: inline-block;
}
.avatar-wrapper img {
    border-radius: 50%;
    border: 3px solid transparent;
    background: linear-gradient(135deg, #7C3AED, #A78BFA) border-box;
    animation: glowPulse 2.5s ease-in-out infinite;
}
.avatar-ring {
    position: absolute;
    top: -6px; left: -6px;
    right: -6px; bottom: -6px;
    border-radius: 50%;
    border: 2px solid rgba(167,139,250,0.3);
    animation: ripple 2s ease-out infinite;
}
.avatar-ring-2 {
    position: absolute;
    top: -12px; left: -12px;
    right: -12px; bottom: -12px;
    border-radius: 50%;
    border: 1px solid rgba(124,58,237,0.2);
    animation: ripple 2s ease-out 0.6s infinite;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, #1a0533, #2d1a4a);
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: 14px;
    padding: 1.25rem 0.75rem;
    text-align: center;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    animation: fadeInUp 0.5s ease both;
    cursor: default;
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    transform: translateY(-5px) scale(1.03);
    border-color: #A78BFA;
    box-shadow: 0 8px 30px rgba(124,58,237,0.4);
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.06), transparent);
    transition: left 0.5s ease;
}
.metric-card:hover::after { left: 150%; }
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #A78BFA;
    font-family: 'Fira Code', monospace;
    animation: numberCount 0.5s ease both;
}
.metric-label {
    font-size: 0.72rem;
    color: #6B7280;
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── Score bar ── */
.score-bar-container {
    background: #1a0533;
    border-radius: 100px;
    height: 12px;
    margin: 0.75rem 0;
    overflow: hidden;
    border: 1px solid rgba(124,58,237,0.3);
}
.score-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #4C1D95, #7C3AED, #A78BFA);
    background-size: 200% 100%;
    animation: scoreReveal 1.5s cubic-bezier(0.4,0,0.2,1) both, gradientShift 2s ease infinite;
    width: var(--score-pct);
    box-shadow: 0 0 12px rgba(167,139,250,0.6);
}

/* ── Section headers ── */
.section-header {
    font-family: 'Fira Code', monospace;
    font-size: 1rem;
    font-weight: 600;
    background: linear-gradient(90deg, #A78BFA, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    border-bottom: 1px solid rgba(124,58,237,0.3);
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem 0;
    animation: fadeInLeft 0.5s ease both;
}

/* ── Repo cards ── */
.repo-card {
    background: linear-gradient(135deg, #1a0533, #1f0d3a);
    border: 1px solid rgba(59,27,110,0.8);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.65rem;
    transition: all 0.3s ease;
    animation: fadeInLeft 0.5s ease both;
    position: relative;
    overflow: hidden;
}
.repo-card:hover {
    border-color: #7C3AED;
    transform: translateX(6px);
    box-shadow: -4px 0 20px rgba(124,58,237,0.3), 0 4px 20px rgba(124,58,237,0.15);
}
.repo-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #7C3AED, #A78BFA);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.repo-card:hover::before { opacity: 1; }
.repo-name { font-family: 'Fira Code', monospace; font-size: 0.95rem; color: #A78BFA; font-weight: 600; }
.repo-name a { text-decoration: none; color: inherit; }
.repo-name a:hover { color: #C4B5FD; }
.repo-desc { font-size: 0.82rem; color: #6B7280; margin-top: 0.2rem; }
.repo-meta { font-size: 0.8rem; color: #9CA3AF; margin-top: 0.5rem; display: flex; gap: 1rem; }

/* ── Tips ── */
.tip-box {
    background: linear-gradient(135deg, rgba(26,5,51,0.8), rgba(45,26,74,0.6));
    border-left: 3px solid #7C3AED;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #CBD5E1;
    animation: fadeInRight 0.5s ease both;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.tip-box:hover {
    border-left-color: #A78BFA;
    background: linear-gradient(135deg, rgba(45,26,74,0.8), rgba(76,29,149,0.4));
    transform: translateX(4px);
}

/* ── Username & bio ── */
.username { font-size: 1.7rem; font-weight: 700; color: #E2E8F0; font-family: 'Fira Code', monospace; }
.bio-text  { color: #94A3B8; font-size: 0.95rem; margin-top: 0.5rem; font-style: italic; }

/* ── Tags ── */
.tag {
    display: inline-block;
    background: rgba(45,26,74,0.8);
    color: #A78BFA;
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.78rem;
    margin: 0.25rem;
    font-family: 'Fira Code', monospace;
    transition: all 0.2s ease;
}
.tag:hover { background: rgba(124,58,237,0.3); border-color: #A78BFA; }

/* ── Score label badge ── */
.score-badge {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 100px;
    font-weight: 600;
    font-size: 0.9rem;
    font-family: 'Fira Code', monospace;
    animation: floatUp 3s ease-in-out infinite;
}

/* ── Search box ── */
.stTextInput > div > div > input {
    background: rgba(26,5,51,0.8) !important;
    border: 1.5px solid rgba(124,58,237,0.5) !important;
    color: #E2E8F0 !important;
    border-radius: 12px !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    transition: all 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.2), 0 0 20px rgba(124,58,237,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: #4B5563 !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #6D28D9, #5B21B6) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(124,58,237,0.5), 0 0 40px rgba(124,58,237,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #374151;
    font-size: 0.8rem;
    font-family: 'Fira Code', monospace;
    padding: 1rem 0;
    animation: fadeInUp 0.5s ease both;
}

/* ── Landing ── */
.landing-icon {
    font-size: 5rem;
    animation: floatUp 3s ease-in-out infinite;
    display: block;
    text-align: center;
}

/* ── Spinner override ── */
.stSpinner > div { border-top-color: #7C3AED !important; }
</style>
""", unsafe_allow_html=True)


# ── Star field background ───────────────────────────────────────────────────────
st.markdown("""
<div id="star-field" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:hidden;"></div>
<script>
(function() {
    const field = document.getElementById('star-field');
    if (!field) return;
    const count = 180;
    for (let i = 0; i < count; i++) {
        const s = document.createElement('div');
        const size = Math.random() * 2.5 + 0.5;
        const dur  = (Math.random() * 4 + 2).toFixed(1);
        const del  = (Math.random() * 5).toFixed(1);
        s.style.cssText = `
            position:absolute;
            left:${(Math.random()*100).toFixed(2)}%;
            top:${(Math.random()*100).toFixed(2)}%;
            width:${size.toFixed(1)}px;
            height:${size.toFixed(1)}px;
            background:rgba(${Math.random()>0.7?'167,139,250':'255,255,255'},${(Math.random()*0.6+0.1).toFixed(2)});
            border-radius:50%;
            animation:twinkle ${dur}s ${del}s ease-in-out infinite;
        `;
        field.appendChild(s);
    }
})();
</script>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">⬡ GitHub Profile Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analyze any GitHub profile — score, stats, languages & top repos</div>', unsafe_allow_html=True)

# ── Search ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([4, 1])
with col_input:
    username = st.text_input(label="GitHub Username", placeholder="e.g. Premnath-06  ·  torvalds  ·  gvanrossum", label_visibility="collapsed")
with col_btn:
    analyze = st.button("Analyze →")

st.markdown('<hr class="glow-divider"/>', unsafe_allow_html=True)


# ── Main ───────────────────────────────────────────────────────────────────────
if analyze and username.strip():
    username = username.strip()

    # ── Validate username before touching the API ────────────────────────────
    valid, err_msg = validate_username(username)
    if not valid:
        st.error(f"⚠️ {err_msg}")
        st.stop()

    with st.spinner(f"Fetching {s(username)}..."):
        user,   user_err = get_user(username)
        repos,  _        = get_repos(username)
        events, _        = get_events(username)

    if user_err:
        st.error(f"❌ {s(user_err)}")
        st.stop()

    repos  = repos  or []
    events = events or []

    languages    = get_top_languages(repos)
    top_repos    = get_top_repos(repos)
    recent_repos = get_recently_updated(repos)
    total_stars  = get_total_stars(repos)
    total_forks  = get_total_forks(repos)
    score, breakdown = calculate_score(user, repos, events)
    age_years    = account_age_years(user.get("created_at", ""))

    # ── Profile card ────────────────────────────────────────────────────────
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    col_av, col_info = st.columns([1, 4])

    with col_av:
        # Avatar URL comes from GitHub's own CDN — safe to use directly
        avatar = user.get("avatar_url", "")
        if avatar and avatar.startswith("https://avatars.githubusercontent.com"):
            st.markdown(f"""
            <div class="avatar-wrapper">
                <img src="{avatar}" width="110" style="border-radius:50%;box-shadow:0 0 20px rgba(124,58,237,0.6)"/>
                <div class="avatar-ring"></div>
                <div class="avatar-ring-2"></div>
            </div>""", unsafe_allow_html=True)

    with col_info:
        # All user-provided fields are escaped via s() before going into HTML
        name  = s(user.get("name") or user.get("login"))
        login = s(user.get("login"))
        bio   = s(user.get("bio", ""))

        st.markdown(f'<div class="username">@{login}</div>', unsafe_allow_html=True)
        if user.get("name") and user.get("name") != user.get("login"):
            st.markdown(f"<span style='color:#94A3B8;font-size:0.95rem'>{name}</span>", unsafe_allow_html=True)
        if bio:
            st.markdown(f'<div class="bio-text">"{bio}"</div>', unsafe_allow_html=True)

        tags = []
        if user.get("location"): tags.append(f"📍 {s(user['location'])}")
        if user.get("company"):  tags.append(f"🏢 {s(user['company'])}")
        if user.get("blog"):     tags.append(f"🌐 {s(user['blog'])}")
        if user.get("created_at"): tags.append(f"📅 Joined {s(user['created_at'][:4])}")
        if tags:
            st.markdown("".join(f'<span class="tag">{t}</span>' for t in tags), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Metric cards ────────────────────────────────────────────────────────
    # public_repos from GitHub API = public only, private repos are never returned
    # by unauthenticated requests so they are never counted here
    cols = st.columns(6)
    metrics = [
        (user.get("public_repos", 0), "Public Repos", "0.1s"),
        (total_stars,                  "Stars",         "0.2s"),
        (total_forks,                  "Forks",         "0.3s"),
        (user.get("followers", 0),     "Followers",     "0.4s"),
        (user.get("following", 0),     "Following",     "0.5s"),
        (f"{age_years:.1f}y",          "Account Age",   "0.6s"),
    ]
    for col, (val, label, delay) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="animation-delay:{delay}">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<hr class="glow-divider"/>', unsafe_allow_html=True)

    # ── Score + Languages ────────────────────────────────────────────────────
    col_s, col_l = st.columns(2)

    with col_s:
        st.markdown('<div class="section-header">◈ Profile Score</div>', unsafe_allow_html=True)

        if   score >= 75: badge_style = "background:rgba(34,197,94,0.15);color:#22C55E;border:1px solid #22C55E"; label = "🟢 Excellent"
        elif score >= 50: badge_style = "background:rgba(245,158,11,0.15);color:#F59E0B;border:1px solid #F59E0B"; label = "🟡 Good"
        elif score >= 25: badge_style = "background:rgba(249,115,22,0.15);color:#F97316;border:1px solid #F97316"; label = "🟠 Needs Work"
        else:             badge_style = "background:rgba(239,68,68,0.15);color:#EF4444;border:1px solid #EF4444"; label = "🔴 Just Starting"

        st.markdown(f"""
        <div style="text-align:center;margin-bottom:1rem">
            <span class="score-badge" style="{badge_style}">{label} · {score}/100</span>
        </div>
        <div class="score-bar-container">
            <div class="score-bar-fill" style="--score-pct:{score}%"></div>
        </div>
        """, unsafe_allow_html=True)

        gauge_fig = score_gauge(score)
        st.plotly_chart(gauge_fig, use_container_width=True, key="gauge")

    with col_l:
        st.markdown('<div class="section-header">◈ Languages</div>', unsafe_allow_html=True)
        if languages:
            st.plotly_chart(language_pie_chart(languages), use_container_width=True, key="lang_pie")
        else:
            st.info("No language data found.")

    st.markdown('<hr class="glow-divider"/>', unsafe_allow_html=True)

    # ── Score breakdown ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">◈ Score Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(score_breakdown_bar(breakdown), use_container_width=True, key="breakdown")

    # ── Tips ────────────────────────────────────────────────────────────────
    tips = []
    safe_login = s(user.get("login", ""))
    if breakdown.get("Has bio", 0) == 0:
        tips.append("💡 Add a bio to your GitHub profile — it instantly makes you look more professional.")
    if breakdown.get("Has portfolio/website", 0) == 0:
        tips.append("🌐 Add a portfolio or project link to your profile settings.")
    if breakdown.get("Has profile README", 0) == 0:
        tips.append(f"📄 Create a repo named exactly '{safe_login}' with a README.md — it appears on your profile page.")
    if breakdown.get("Active in last 30 days", 0) == 0:
        tips.append("⚡ No pushes in the last 30 days. Commit something — even small improvements count.")
    if breakdown.get("Stars earned", 0) == 0:
        tips.append("⭐ Stars come from solving real problems. Share your projects on Reddit, dev.to, or Twitter.")

    if tips:
        st.markdown('<div class="section-header">◈ How to Improve</div>', unsafe_allow_html=True)
        for i, tip in enumerate(tips):
            st.markdown(f'<div class="tip-box" style="animation-delay:{i*0.1}s">{tip}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<hr class="glow-divider"/>', unsafe_allow_html=True)

    # ── Top repos chart ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">◈ Top Repos by Stars</div>', unsafe_allow_html=True)
    if top_repos:
        st.plotly_chart(top_repos_bar_chart(top_repos), use_container_width=True, key="top_repos")
    else:
        st.info("No repositories found.")

    # ── Recent repos ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">◈ Recently Updated</div>', unsafe_allow_html=True)
    for i, repo in enumerate(recent_repos):
        # All repo fields escaped — repo descriptions can contain arbitrary text
        repo_name = s(repo.get("name", ""))
        repo_desc = s(repo.get("description") or "No description")
        stars     = int(repo.get("stargazers_count", 0))
        forks     = int(repo.get("forks_count", 0))
        language  = s(repo.get("language") or "—")
        updated   = s(repo.get("updated_at", "")[:10])
        # Repo URL validated — must start with github.com
        raw_url   = repo.get("html_url", "")
        url       = raw_url if raw_url.startswith("https://github.com/") else "#"

        st.markdown(f"""
        <div class="repo-card" style="animation-delay:{i*0.08}s">
            <div class="repo-name">
                <a href="{url}" target="_blank" rel="noopener noreferrer">📁 {repo_name}</a>
            </div>
            <div class="repo-desc">{repo_desc}</div>
            <div class="repo-meta">
                <span>⭐ {stars}</span>
                <span>🍴 {forks}</span>
                <span>🔤 {language}</span>
                <span>🕐 {updated}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown('<hr class="glow-divider"/>', unsafe_allow_html=True)
    st.markdown(
        '<div class="footer">'
        '🔒 Public data only · No authentication · No private repos · All inputs validated'
        '</div>',
        unsafe_allow_html=True
    )

elif analyze and not username.strip():
    st.warning("Please enter a GitHub username first.")

else:
    st.markdown("""
    <div style="text-align:center;padding:4rem 0;">
        <div class="landing-icon">⬡</div>
        <br/>
        <div style="font-size:1.15rem;color:#6B7280;font-family:'Fira Code',monospace;">
            Enter any GitHub username and click <span style="color:#A78BFA;font-weight:600;">Analyze →</span>
        </div>
        <div style="font-size:0.85rem;color:#374151;margin-top:0.75rem;">
            Try: &nbsp;
            <span style="color:#7C3AED">Premnath-06</span> &nbsp;·&nbsp;
            <span style="color:#7C3AED">torvalds</span> &nbsp;·&nbsp;
            <span style="color:#7C3AED">gvanrossum</span>
        </div>
    </div>
    """, unsafe_allow_html=True)