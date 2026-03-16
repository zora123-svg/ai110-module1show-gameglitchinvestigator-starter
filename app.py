import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

# Fixed: The logic for the hint is worng and it's in the return statment of this function
def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="centered")

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Hero header ── */
    .hero {
        background: linear-gradient(135deg, #6c63ff 0%, #3ecf8e 100%);
        border-radius: 16px;
        padding: 2rem 1.5rem 1.5rem;
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(108,99,255,0.25);
    }
    .hero h1 { font-size: 2rem; font-weight: 700; margin: 0; }
    .hero p  { opacity: 0.85; margin: 0.3rem 0 0; font-size: 0.95rem; }

    /* ── Stat cards ── */
    .stat-row { display: flex; gap: 12px; margin-bottom: 1.2rem; }
    .stat-card {
        flex: 1;
        border-radius: 12px;
        padding: 0.9rem 1rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12);
    }
    .stat-card .label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.85; }
    .stat-card .value { font-size: 1.8rem; font-weight: 700; line-height: 1.1; }
    .card-score    { background: linear-gradient(135deg, #f093fb, #f5576c); }
    .card-attempts { background: linear-gradient(135deg, #4facfe, #00f2fe); }
    .card-range    { background: linear-gradient(135deg, #43e97b, #38f9d7); }

    /* ── Progress bar ── */
    .progress-wrap {
        background: #e9ecef;
        border-radius: 999px;
        height: 12px;
        overflow: hidden;
        margin-bottom: 1.4rem;
    }
    .progress-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.4s ease;
    }

    /* ── Guess history ── */
    .history-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 1.2rem; }
    .chip {
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: white;
    }
    .chip-high { background: #f5576c; }
    .chip-low  { background: #4facfe; }
    .chip-win  { background: #43e97b; color: #155724; }
    .chip-err  { background: #adb5bd; }

    /* ── Input & buttons polish ── */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        border: 2px solid #dee2e6 !important;
        font-size: 1.1rem !important;
        padding: 0.6rem 0.9rem !important;
        transition: border-color 0.2s;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6c63ff !important;
        box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
    }
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.45rem 1rem !important;
        transition: transform 0.1s, box-shadow 0.1s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }

    /* ── Difficulty badge in sidebar ── */
    .diff-easy   { color: #28a745; font-weight: 700; }
    .diff-normal { color: #fd7e14; font-weight: 700; }
    .diff-hard   { color: #dc3545; font-weight: 700; }

    /* ── Footer ── */
    .footer { text-align: center; color: #adb5bd; font-size: 0.8rem; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("## ⚙️ Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

diff_colors = {"Easy": "diff-easy", "Normal": "diff-normal", "Hard": "diff-hard"}
st.sidebar.markdown(
    f"<span class='{diff_colors[difficulty]}'>{difficulty}</span> &nbsp;|&nbsp; "
    f"Range: **{low}–{high}** &nbsp;|&nbsp; Attempts: **{attempt_limit}**",
    unsafe_allow_html=True,
)

st.sidebar.divider()
st.sidebar.markdown("### 📊 Scoring Guide")
st.sidebar.markdown(
    "- **Win**: `100 − 10 × attempt` (min 10)\n"
    "- **Too High** (even attempt): `+5`\n"
    "- **Too High** (odd attempt): `−5`\n"
    "- **Too Low**: `−5`"
)

# ── Session state ──────────────────────────────────────────────────────────────
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []
if "outcomes" not in st.session_state:
    st.session_state.outcomes = []   # parallel list: outcome per history entry

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero">'
    '<h1>🎮 Game Glitch Investigator</h1>'
    '<p>An AI-generated guessing game. Something is off.</p>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Stat cards ────────────────────────────────────────────────────────────────
attempts_left = attempt_limit - st.session_state.attempts
st.markdown(
    f'<div class="stat-row">'
    f'  <div class="stat-card card-score">'
    f'    <div class="label">Score</div>'
    f'    <div class="value">{st.session_state.score}</div>'
    f'  </div>'
    f'  <div class="stat-card card-attempts">'
    f'    <div class="label">Attempts Left</div>'
    f'    <div class="value">{attempts_left}</div>'
    f'  </div>'
    f'  <div class="stat-card card-range">'
    f'    <div class="label">Range</div>'
    f'    <div class="value">{low}–{high}</div>'
    f'  </div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Attempts progress bar ─────────────────────────────────────────────────────
pct = max(0, attempts_left / attempt_limit * 100)
if pct > 60:
    bar_color = "linear-gradient(90deg,#43e97b,#38f9d7)"
elif pct > 30:
    bar_color = "linear-gradient(90deg,#f7971e,#ffd200)"
else:
    bar_color = "linear-gradient(90deg,#f5576c,#f093fb)"

st.markdown(
    f'<div class="progress-wrap">'
    f'  <div class="progress-fill" style="width:{pct}%; background:{bar_color};"></div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Developer debug info ───────────────────────────────────────────────────────
with st.expander("🔧 Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# ── Guess history chips ────────────────────────────────────────────────────────
if st.session_state.history:
    chip_class_map = {"Win": "chip-win", "Too High": "chip-high", "Too Low": "chip-low", None: "chip-err"}
    chips_html = "".join(
        f'<span class="chip {chip_class_map.get(o, "chip-err")}">{v}</span>'
        for v, o in zip(st.session_state.history, st.session_state.outcomes)
    )
    st.markdown(
        f'<div style="font-size:0.8rem;color:#6c757d;margin-bottom:4px;">Previous guesses</div>'
        f'<div class="history-wrap">{chips_html}</div>',
        unsafe_allow_html=True,
    )

# ── Input & controls ───────────────────────────────────────────────────────────
st.markdown("### 🎯 Make a guess")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}",
    placeholder=f"Pick a number between {low} and {high}…",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀", use_container_width=True)
with col2:
    new_game = st.button("New Game 🔁", use_container_width=True)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# ── New game ──────────────────────────────────────────────────────────────────
# Fixed: The new game button doesn't reset beacuse the new_game function doesn't have the session status
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.outcomes = []
    st.success("New game started!")
    st.rerun()

# ── Game-over gate ─────────────────────────────────────────────────────────────
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("🏆 You already won! Start a new game to play again.")
    else:
        st.error("💀 Game over. Start a new game to try again.")
    st.stop()

# ── Submit logic ───────────────────────────────────────────────────────────────
if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.outcomes.append(None)
        st.error(f"⚠️ {err}")
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)
        st.session_state.outcomes.append(outcome)

        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.error(f"🔴 Too High! {message}")
            else:
                st.info(f"🔵 Too Low! {message}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"🏆 You won! The secret was **{st.session_state.secret}**. "
                f"Final score: **{st.session_state.score}**"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"💀 Out of attempts! "
                    f"The secret was **{st.session_state.secret}**. "
                    f"Score: **{st.session_state.score}**"
                )

# Fixed: Moved st.info after the submit function this fixed the game ending earlier before attempts reaches 0
st.info(
    f"🔢 Guess a number between **{low}** and **{high}**. "
    f"**{attempt_limit - st.session_state.attempts}** attempt(s) remaining."
)

st.divider()
st.markdown('<div class="footer">Built by an AI that claims this code is production-ready.</div>', unsafe_allow_html=True)
