"""
Nexus Mind: Autonomous Multi-Agent Gaming & Intelligence Platform
Engineered by Sainbux (Hadi) Seelro - Agentic AI Developer.
Demonstrating real-time state synchronization, multi-agent arbitration,
and an accessible 24/7 live contextual customer support agent.
"""

import streamlit as st
import time
from typing import Dict, Any

from agents.arbiter_agent import ArbiterAgent
from agents.analytics_agent import AnalyticsAgent
from agents.support_agent import SupportAgent

# ---------------------------------------------------------
# PAGE CONFIGURATION & METADATA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nexus Mind // Smart AI Number Game",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# HIGH-CONTRAST CLEAN SLATE MODERN DESIGN (100% VISIBILITY)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global App Canvas - Clean Deep Slate */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Force Full Text Visibility Across Streamlit Widgets */
    p, span, label, div, h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9;
    }
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    .stMarkdown p {
        color: #e2e8f0 !important;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Modern Hero Header Banner */
    .hero-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #38bdf8;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .hero-badge {
        display: inline-block;
        background: #0284c7;
        color: #ffffff !important;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
    }
    .hero-title {
        color: #ffffff !important;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0 0 8px 0;
    }
    .hero-desc {
        color: #cbd5e1 !important;
        font-size: 1.05rem;
        margin: 0 0 14px 0;
    }

    /* 3-Step Guide Box */
    .steps-box {
        background: #1e293b;
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
        padding: 12px 18px;
        margin-top: 10px;
    }
    .steps-box b {
        color: #38bdf8 !important;
    }
    .steps-box span {
        color: #f1f5f9 !important;
    }

    /* Metric Cards */
    .stat-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .stat-title {
        color: #94a3b8 !important;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .stat-num {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 800;
    }

    /* Target Search Boundary Bar */
    .boundary-banner {
        background: #1e293b;
        border: 2px dashed #0284c7;
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
        margin: 16px 0;
    }
    .boundary-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff !important;
    }
    .boundary-highlight {
        color: #38bdf8 !important;
        font-size: 1.4rem;
    }

    /* Radar Clue Boxes */
    .clue-card {
        border-radius: 12px;
        padding: 18px;
        margin-top: 14px;
        text-align: center;
        border: 2px solid #475569;
    }
    .clue-boiling {
        background: #450a0a;
        border-color: #ef4444;
    }
    .clue-warm {
        background: #451a03;
        border-color: #f59e0b;
    }
    .clue-lukewarm {
        background: #082f49;
        border-color: #0284c7;
    }
    .clue-cold {
        background: #1e1b4b;
        border-color: #6366f1;
    }

    /* Input & Button Styling (Crisp & High Contrast) */
    .stTextInput input, .stNumberInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 2px solid #475569 !important;
        border-radius: 10px !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #38bdf8 !important;
    }

    /* Primary Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4) !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
    }

    /* Tabs Styling - Bold and Visible */
    [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0f172a;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    [data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border-radius: 8px !important;
        padding: 10px 18px !important;
    }
    [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 700 !important;
        border-bottom: 3px solid #38bdf8 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }

    /* Creator Card in Sidebar */
    .dev-badge {
        background: #1e293b;
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 14px;
        margin-top: 14px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# INITIALIZE AGENTS
# ---------------------------------------------------------
@st.cache_resource
def get_agents():
    arbiter = ArbiterAgent()
    analytics = AnalyticsAgent()
    support = SupportAgent(developer_name="Sainbux (Hadi) Seelro")
    return arbiter, analytics, support

arbiter_agent, analytics_agent, support_agent = get_agents()


# ---------------------------------------------------------
# SESSION STATE MANAGEMENT
# ---------------------------------------------------------
def init_game_state(reset_lifetime: bool = False):
    """Safely initialize or reset game and telemetry state."""
    if reset_lifetime or "games_played" not in st.session_state:
        st.session_state.games_played = 0
        st.session_state.games_won = 0
        st.session_state.current_streak = 0
        st.session_state.best_streak = 0
        st.session_state.best_score = None
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "👋 **Hello! I'm Nova**, your 24/7 AI Helper. You can ask me for a hint, learn the rules, or ask about the developer!"
            }
        ]

    # Current Round Configuration
    if "min_val" not in st.session_state:
        st.session_state.min_val = 1
    if "max_val" not in st.session_state:
        st.session_state.max_val = 100
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "🎯 Classic Mode"

    # Reset Round variables
    st.session_state.secret_number = arbiter_agent.generate_secret(st.session_state.min_val, st.session_state.max_val)
    st.session_state.active_low = st.session_state.min_val
    st.session_state.active_high = st.session_state.max_val
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.game_won = False
    st.session_state.last_feedback = None
    st.session_state.last_heat = None
    st.session_state.history = []
    st.session_state.optimal_steps = arbiter_agent.calculate_optimal_steps(st.session_state.min_val, st.session_state.max_val)
    st.session_state.max_allowed_moves = st.session_state.optimal_steps + 2
    st.session_state.ai_duel_turn = "Player"
    st.session_state.ai_duel_history = []
    st.session_state.agent_logs = [
        f"[{time.strftime('%H:%M:%S')}] Nexus Arbiter picked secret number between {st.session_state.min_val} and {st.session_state.max_val}."
    ]

# First-time initialization
if "secret_number" not in st.session_state:
    init_game_state()


# ---------------------------------------------------------
# SIDEBAR: SETTINGS & CREATOR PROFILE
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Game Settings")
    
    # Live Status
    st.markdown("""
    <div style="background:#1e293b; padding:10px 14px; border-radius:10px; border:1px solid #334155; margin-bottom:16px;">
        <div style="color:#34d399; font-weight:700; font-size:0.85rem; margin-bottom:4px;">● AI Arbiter: Online</div>
        <div style="color:#38bdf8; font-weight:700; font-size:0.85rem;">● Nova AI Concierge: 24/7 Live</div>
    </div>
    """, unsafe_allow_html=True)

    # Game Mode Selection
    mode_options = [
        "🎯 Classic Mode",
        "🤖 Play Against AI",
        "⏳ 7-Guess Challenge"
    ]
    
    current_mode = st.session_state.game_mode
    if current_mode not in mode_options:
        current_mode = "🎯 Classic Mode"
        st.session_state.game_mode = current_mode

    selected_mode = st.selectbox(
        "Choose Mode:",
        mode_options,
        index=mode_options.index(current_mode),
        help="Classic: Relaxed play | Play Against AI: Beat the computer | 7-Guess: Limited tries"
    )

    if selected_mode != st.session_state.game_mode:
        st.session_state.game_mode = selected_mode
        init_game_state(reset_lifetime=False)
        st.rerun()

    # Range Selection
    st.markdown("### 📏 Number Range")
    range_tier = st.radio(
        "Select Range:",
        ["Easy (1 to 20)", "Medium (1 to 100)", "Hard (1 to 500)", "Custom Range"],
        index=1
    )

    new_min, new_max = st.session_state.min_val, st.session_state.max_val
    if range_tier == "Easy (1 to 20)":
        new_min, new_max = 1, 20
    elif range_tier == "Medium (1 to 100)":
        new_min, new_max = 1, 100
    elif range_tier == "Hard (1 to 500)":
        new_min, new_max = 1, 500
    else:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            new_min = st.number_input("Min", value=1, step=1)
        with col_c2:
            new_max = st.number_input("Max", value=100, step=10)

    if new_min >= new_max:
        st.error("Min value must be less than Max.")
        new_max = new_min + 10

    if new_min != st.session_state.min_val or new_max != st.session_state.max_val:
        st.session_state.min_val = int(new_min)
        st.session_state.max_val = int(new_max)
        init_game_state(reset_lifetime=False)
        st.rerun()

    st.markdown("---")

    # Developer Profile Card
    st.markdown(f"""
    <div class="dev-badge">
        <div style="font-size:0.75rem; text-transform:uppercase; color:#38bdf8; font-weight:700;">Developer Portfolio</div>
        <div style="font-size:1.1rem; font-weight:800; color:#ffffff; margin: 4px 0;">Sainbux (Hadi) Seelro</div>
        <div style="font-size:0.85rem; color:#cbd5e1; margin-bottom:10px;">Agentic AI & Systems Developer</div>
        <a href="https://github.com/SainBux-HadiSeelro/nexus-mind-agentic-platform" target="_blank" style="text-decoration:none; display:inline-block; background:#0284c7; color:#ffffff; padding:6px 14px; border-radius:6px; font-size:0.8rem; font-weight:700;">
            ⭐ GitHub Repo
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Optional OpenAI Key
    with st.expander("🔑 Advanced: OpenAI Key (Optional)", expanded=False):
        user_api_key = st.text_input(
            "API Key:",
            type="password",
            placeholder="sk-...",
            help="Nova works 100% free with the built-in offline engine. Adding an OpenAI key is optional."
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("🔄 Reset Score", use_container_width=True):
        init_game_state(reset_lifetime=True)
        st.rerun()


# ---------------------------------------------------------
# HERO HEADER BOX (HIGH CONTRAST & CLEAR)
# ---------------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-badge">⚡ Autonomous Agentic AI System</div>
    <div class="hero-title">🎯 Nexus Mind: Smart AI Number Game</div>
    <div class="hero-desc">
        Can you guess the secret number? An intelligent AI Arbiter gives you live Hot & Cold clues to help you win!
    </div>
    <div class="steps-box">
        <b>Quick 3-Step Guide:</b><br/>
        <span>1️⃣ Enter a number between the range and click <b>Check My Guess</b>.</span><br/>
        <span>2️⃣ Read the AI clue: It will tell you if you are <b>Too High</b>, <b>Too Low</b>, or <b>Getting Warm/Hot!</b></span><br/>
        <span>3️⃣ If you ever get stuck, open the <b>💬 Nova AI Helper</b> tab for a free clue!</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# TOP SCORE METRIC CARDS
# ---------------------------------------------------------
stats_summary = analytics_agent.summarize_session({
    "games_played": st.session_state.games_played,
    "games_won": st.session_state.games_won,
    "current_streak": st.session_state.current_streak,
    "best_streak": st.session_state.best_streak,
    "best_score": st.session_state.best_score
})

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-title">🎮 Games Played</div>
        <div class="stat-num">{stats_summary['games_played']}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-title">🏆 Victories</div>
        <div class="stat-num" style="color:#34d399;">{stats_summary['games_won']}</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-title">🎯 Win Rate</div>
        <div class="stat-num" style="color:#38bdf8;">{stats_summary['win_rate']}%</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-title">🔥 Win Streak</div>
        <div class="stat-num" style="color:#fbbf24;">{stats_summary['current_streak']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)


# ---------------------------------------------------------
# MAIN INTERFACE TABS
# ---------------------------------------------------------
tab_game, tab_chatbot, tab_specs, tab_logs = st.tabs([
    "🎮 Play Game",
    "💬 Nova AI Helper (24/7 Chat)",
    "🧠 System Architecture (For Techies)",
    "📜 Live AI Activity Log"
])


# =========================================================
# TAB 1: PLAY GAME
# =========================================================
with tab_game:
    col_play, col_clues = st.columns([1.3, 1.0])

    with col_play:
        st.markdown(f"### Current Mode: **{st.session_state.game_mode}**")
        
        # Target Boundary Banner
        total_span = max(1, st.session_state.max_val - st.session_state.min_val)
        active_span = max(1, st.session_state.active_high - st.session_state.active_low)
        eliminated_pct = int(((total_span - active_span) / total_span) * 100)
        remaining_count = active_span + 1

        st.markdown(f"""
        <div class="boundary-banner">
            <span class="boundary-text">Secret number is between </span>
            <span class="boundary-highlight">[{st.session_state.active_low}]</span>
            <span class="boundary-text"> and </span>
            <span class="boundary-highlight">[{st.session_state.active_high}]</span>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(1.0, max(0.0, eliminated_pct / 100.0)), text=f"Search Progress: {eliminated_pct}% eliminated ({remaining_count} possible numbers left)")

        # Challenge Mode Countdown
        if st.session_state.game_mode == "⏳ 7-Guess Challenge":
            moves_left = max(0, st.session_state.max_allowed_moves - st.session_state.attempts)
            st.warning(f"⏳ **Tries Remaining:** **{moves_left}** / {st.session_state.max_allowed_moves}")
            if moves_left <= 0 and not st.session_state.game_over:
                st.session_state.game_over = True
                st.session_state.game_won = False
                st.session_state.current_streak = 0
                st.session_state.games_played += 1
                st.error(f"⌛ Out of tries! The secret number was **{st.session_state.secret_number}**.")

        # GUESS INPUT BOX
        if not st.session_state.game_over:
            with st.form("clean_guess_form", clear_on_submit=False):
                col_i1, col_i2 = st.columns([2, 1])
                with col_i1:
                    default_guess = int((st.session_state.active_low + st.session_state.active_high) // 2)
                    user_guess = st.number_input(
                        f"Enter your number ({st.session_state.active_low} to {st.session_state.active_high}):",
                        min_value=int(st.session_state.min_val),
                        max_value=int(st.session_state.max_val),
                        value=default_guess,
                        step=1
                    )
                with col_i2:
                    st.write("")
                    st.write("")
                    submit_guess = st.form_submit_button("🎯 Check My Guess", use_container_width=True, type="primary")

            if submit_guess and not st.session_state.game_over:
                st.session_state.attempts += 1
                status, feedback, heat = arbiter_agent.evaluate_guess(user_guess, st.session_state.secret_number)
                st.session_state.last_feedback = feedback
                st.session_state.last_heat = heat

                # Update boundaries
                if status == "TOO_LOW":
                    st.session_state.active_low = max(st.session_state.active_low, user_guess + 1)
                elif status == "TOO_HIGH":
                    st.session_state.active_high = min(st.session_state.active_high, user_guess - 1)

                # History log
                st.session_state.history.append({
                    "attempt": st.session_state.attempts,
                    "guess": user_guess,
                    "status": status,
                    "heat": heat,
                    "window": f"[{st.session_state.active_low}..{st.session_state.active_high}]"
                })

                st.session_state.agent_logs.append(
                    f"[{time.strftime('%H:%M:%S')}] Player guessed {user_guess} -> {status} ({heat}). New range: [{st.session_state.active_low}..{st.session_state.active_high}]."
                )

                # WIN CONDITION
                if status == "WIN":
                    st.session_state.game_over = True
                    st.session_state.game_won = True
                    st.session_state.games_played += 1
                    st.session_state.games_won += 1
                    st.session_state.current_streak += 1
                    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.current_streak)

                    efficiency = analytics_agent.calculate_efficiency(st.session_state.optimal_steps, st.session_state.attempts)
                    if st.session_state.best_score is None or efficiency > st.session_state.best_score:
                        st.session_state.best_score = efficiency

                    st.session_state.last_efficiency = efficiency
                    st.balloons()
                    st.rerun()

                # AI DUEL MODE: AI TAKES ITS TURN
                elif st.session_state.game_mode == "🤖 Play Against AI" and not st.session_state.game_over:
                    ai_guess = arbiter_agent.autonomous_ai_guess(st.session_state.active_low, st.session_state.active_high, strategy="optimal")
                    ai_status, ai_feedback, ai_heat = arbiter_agent.evaluate_guess(ai_guess, st.session_state.secret_number)
                    
                    st.session_state.ai_duel_history.append({
                        "turn": len(st.session_state.ai_duel_history) + 1,
                        "ai_guess": ai_guess,
                        "status": ai_status,
                        "heat": ai_heat
                    })

                    st.session_state.agent_logs.append(
                        f"[{time.strftime('%H:%M:%S')}] AI Opponent guessed {ai_guess} -> {ai_status} ({ai_heat})."
                    )

                    if ai_status == "TOO_LOW":
                        st.session_state.active_low = max(st.session_state.active_low, ai_guess + 1)
                    elif ai_status == "TOO_HIGH":
                        st.session_state.active_high = min(st.session_state.active_high, ai_guess - 1)
                    elif ai_status == "WIN":
                        st.session_state.game_over = True
                        st.session_state.game_won = False
                        st.session_state.games_played += 1
                        st.session_state.current_streak = 0
                        st.warning(f"🤖 Oh no! The AI Opponent guessed **{ai_guess}** and found the secret number before you!")
                        st.rerun()

                st.rerun()

        # WINNER / GAME OVER CARD
        if st.session_state.game_over:
            if st.session_state.game_won:
                efficiency = analytics_agent.calculate_efficiency(st.session_state.optimal_steps, st.session_state.attempts)
                badge = analytics_agent.evaluate_performance_badge(efficiency, st.session_state.attempts, st.session_state.optimal_steps)
                
                st.markdown(f"""
                <div style="background:#064e3b; border:2px solid #10b981; border-radius:14px; padding:20px; margin-top:16px;">
                    <h2 style="color:#ffffff; margin:0 0 6px 0;">🎉 CONGRATULATIONS! YOU WON!</h2>
                    <p style="font-size:1.15rem; color:#d1fae5; margin-bottom:10px;">You found the secret number <b>{st.session_state.secret_number}</b> in just <b>{st.session_state.attempts}</b> tries!</p>
                    <div style="font-size: 1.3rem; margin-bottom: 6px; color:#fde047;">{badge.get('stars', '⭐⭐⭐')} <b>{badge['title']}</b></div>
                    <p style="color:#a7f3d0; font-style:italic;">"{badge['verdict']}"</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#450a0a; border:2px solid #ef4444; border-radius:14px; padding:20px; margin-top:16px;">
                    <h3 style="color:#ffffff; margin-top:0;">Round Complete!</h3>
                    <p style="color:#fecaca;">The secret number was <b>{st.session_state.secret_number}</b>.</p>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            if st.button("🚀 Play Another Round", type="primary", use_container_width=True):
                init_game_state(reset_lifetime=False)
                st.rerun()

        # EASY CLUE EXPANDER
        with st.expander("💡 Want an easy clue from the AI Arbiter?", expanded=False):
            if not st.session_state.game_over:
                hint_text = arbiter_agent.generate_smart_hint(
                    st.session_state.secret_number,
                    st.session_state.active_low,
                    st.session_state.active_high,
                    max(1, st.session_state.attempts)
                )
                st.info(f"🤖 **AI Clue:** {hint_text}")
                rec_guess = arbiter_agent.get_binary_search_recommendation(st.session_state.active_low, st.session_state.active_high)
                st.caption(f"Smartest guess right now: **{rec_guess}** (halves the remaining choices!)")
            else:
                st.write("Start a new round to unlock clues.")

    # CLUES & RECENT GUESSES COLUMN
    with col_clues:
        st.markdown("### 📡 Live AI Sensor")
        
        # Last Feedback Callout
        if st.session_state.last_feedback:
            heat_class = {
                "🔥 BOILING HOT": "clue-boiling",
                "🌡️ WARM": "clue-warm",
                "🌤️ LUKEWARM": "clue-lukewarm",
                "❄️ SUB-ZERO COLD": "clue-cold"
            }.get(st.session_state.last_heat, "clue-lukewarm")

            st.markdown(f"""
            <div class="clue-card {heat_class}">
                <div style="font-size:0.85rem; color:#cbd5e1; text-transform:uppercase; font-weight:700;">Latest Reading</div>
                <div style="font-size:1.35rem; font-weight:800; margin: 8px 0; color:#ffffff;">{st.session_state.last_feedback}</div>
                <div style="font-size:1.1rem; font-weight:800; color:#ffffff;">{st.session_state.last_heat}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Make your first guess to see live AI radar clues here!")

        # Past Guesses
        if st.session_state.history:
            st.markdown("#### 📝 Your Recent Guesses")
            for h in reversed(st.session_state.history[-5:]):
                st.markdown(f"• Try #{h['attempt']}: Guessed **{h['guess']}** ➔ `{h['status']}` ({h['heat']})")

        # AI Moves (if playing against AI)
        if st.session_state.game_mode == "🤖 Play Against AI" and st.session_state.ai_duel_history:
            st.markdown("#### 🤖 AI Opponent's Moves")
            for m in reversed(st.session_state.ai_duel_history[-4:]):
                st.markdown(f"• AI Turn #{m['turn']}: Guessed **{m['ai_guess']}** ➔ `{m['status']}`")


# =========================================================
# TAB 2: NOVA 24/7 AI HELPER CHATBOT
# =========================================================
with tab_chatbot:
    st.markdown("### 💬 Nova — 24/7 Live AI Helper")
    st.caption("Nova monitors your live game session. Ask for an easy hint, how to play, or about the developer!")

    # Live state for chatbot
    live_telemetry_snapshot = {
        "game_mode": st.session_state.game_mode,
        "active_range": [st.session_state.active_low, st.session_state.active_high],
        "full_range": [st.session_state.min_val, st.session_state.max_val],
        "attempts": st.session_state.attempts,
        "optimal_steps": st.session_state.optimal_steps,
        "game_over": st.session_state.game_over,
        "game_won": st.session_state.game_won,
        "games_played": st.session_state.games_played,
        "games_won": st.session_state.games_won,
        "current_streak": st.session_state.current_streak,
        "last_feedback": st.session_state.last_feedback
    }

    # Friendly Quick Action Chips
    st.markdown("**Click any question to ask quickly:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    if qc1.button("💡 Give Me an Easy Hint", use_container_width=True):
        quick_query = "Can you give me an easy hint for my current number?"
    if qc2.button("❓ How Do I Play?", use_container_width=True):
        quick_query = "How do I play this game and win quickly?"
    if qc3.button("👨‍💻 Who Created This?", use_container_width=True):
        quick_query = "Who is the developer that built this game and what is their portfolio?"
    if qc4.button("🤖 How Does AI Work?", use_container_width=True):
        quick_query = "Explain how the multi-agent AI system operates in simple words."

    # Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    chat_input = st.chat_input("Ask Nova anything (e.g., 'give me a clue' or 'who made this?')...")
    user_prompt = quick_query or chat_input

    if user_prompt:
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Nova is thinking..."):
                response_text = support_agent.respond(
                    user_message=user_prompt,
                    live_state=live_telemetry_snapshot,
                    api_key=user_api_key if 'user_api_key' in locals() and user_api_key else None
                )
                st.markdown(response_text)

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        st.session_state.agent_logs.append(
            f"[{time.strftime('%H:%M:%S')}] Nova Helper replied to: '{user_prompt[:35]}...'."
        )


# =========================================================
# TAB 3: SYSTEM ARCHITECTURE (FOR RECRUITERS & TECHIES)
# =========================================================
with tab_specs:
    st.markdown("### 🧠 Multi-Agent AI System Architecture (For Technical Review)")
    st.markdown("""
    Underneath the user-friendly UI is an **Autonomous Multi-Agent System (MAS)** where dedicated agents
    communicate via a reactive session telemetry bus.
    """)

    st.markdown("""
    ```mermaid
    flowchart TD
        User([👤 Player / Recruiter]) <-->|Interacts & Prompts| UI[🖥️ Streamlit Frontend Layer]
        UI <-->|Bidirectional Sync| Bus[🧠 Reactive Session State Bus]

        subgraph Swarm["Autonomous Multi-Agent Swarm"]
            Arbiter["⚖️ Nexus Arbiter Agent\n• Mathematical Bounds\n• Divisibility Clues\n• AI Opponent Heuristics"]
            Oracle["📊 Oracle Telemetry Agent\n• Shannon Entropy Reduction\n• Logarithmic Efficiency Benchmarks\n• Performance Badges"]
            Nova["🤖 Nova 24/7 AI Concierge\n• Live Telemetry Sync\n• Dual-Engine: Local Heuristics + LLM\n• Portfolio Ingestion"]
        end

        Bus --> Arbiter
        Arbiter --> Bus
        Bus --> Oracle
        Oracle --> Bus
        Bus --> Nova
        Nova --> UI
    ```
    """)

    st.markdown(r"""
    #### 🔬 Technical Highlights:
    - **Algorithmic Optimality:** Mathematical target is reached in $\lceil\log_2 N\rceil$ binary steps.
    - **Shannon Entropy Telemetry:** Uncertainty measured in bits: $H(S) = \log_2(|S|)$.
    - **Dual-Engine Resilient Design:** Built-in Autonomous Heuristic engine ensures zero downtime, with optional GPT-4o-mini dynamic telemetry augmentation.
    - **Developer:** **Sainbux (Hadi) Seelro** | [GitHub Repository](https://github.com/SainBux-HadiSeelro/nexus-mind-agentic-platform)
    """)


# =========================================================
# TAB 4: REAL-TIME AI ACTIVITY LOGS
# =========================================================
with tab_logs:
    st.markdown("### 📜 Real-Time Agent Execution Log")
    st.caption("Live background activity of inter-agent messages, state changes, and evaluation loops.")

    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        st.markdown("#### Live Event Feed")
        for log in reversed(st.session_state.agent_logs[-15:]):
            st.code(log, language="bash")

    with col_l2:
        st.markdown("#### State Vector Snapshot")
        st.json({
            "target_range": [st.session_state.active_low, st.session_state.active_high],
            "attempts": st.session_state.attempts,
            "mode": st.session_state.game_mode,
            "game_over": st.session_state.game_over,
            "games_won": st.session_state.games_won,
            "current_streak": st.session_state.current_streak
        })


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.9rem; padding: 12px 0;">
    🎯 <b>Nexus Mind</b> | Created by <b>Sainbux (Hadi) Seelro</b> (Agentic AI Developer) | 
    Powered by Autonomous Multi-Agent Swarms & 24/7 Live AI Helper.
</div>
""", unsafe_allow_html=True)
