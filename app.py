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
    page_title="Nexus Mind // Next-Gen AI Gaming",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ULTRA-PREMIUM MODERN OBSIDIAN & AURORA DESIGN SYSTEM
# ---------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

<style>
    /* Global App Canvas */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #171b30 0%, #080a12 60%, #030408 100%);
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Ambient Header Glow */
    .hero-container {
        position: relative;
        padding: 30px 24px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 24px;
        overflow: hidden;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, transparent 70%);
        filter: blur(40px);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        font-size: 0.8rem;
        font-weight: 700;
        color: #38bdf8;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.15;
        background: linear-gradient(135deg, #ffffff 20%, #93c5fd 60%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 10px 0;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.5;
        margin: 0 0 16px 0;
        max-width: 720px;
    }

    /* Quick Guide Chips */
    .quick-chips-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
    }
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 10px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.15);
        font-size: 0.85rem;
        color: #cbd5e1;
    }

    /* Metric Luxury Card */
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.7) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.3);
    }
    .metric-label {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Glass Panels */
    .glass-panel {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.75) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5);
    }

    /* Thermal Radar Box */
    .radar-box {
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 12px;
        position: relative;
        overflow: hidden;
    }
    .radar-boiling {
        background: radial-gradient(circle at 50% 0%, rgba(239, 68, 68, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-color: rgba(239, 68, 68, 0.5);
    }
    .radar-warm {
        background: radial-gradient(circle at 50% 0%, rgba(245, 158, 11, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-color: rgba(245, 158, 11, 0.5);
    }
    .radar-lukewarm {
        background: radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-color: rgba(56, 189, 248, 0.5);
    }
    .radar-cold {
        background: radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%);
        border-color: rgba(99, 102, 241, 0.5);
    }

    /* Target Search Range Visualizer */
    .range-visualizer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 12px 18px;
        margin: 14px 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .range-endpoint {
        font-size: 1.15rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .range-middle {
        color: #f59e0b;
        font-weight: 700;
        letter-spacing: 0.1em;
    }

    /* Styled Inputs & Buttons */
    div[data-testid="stForm"] {
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 18px;
        padding: 20px;
        background: rgba(15, 23, 42, 0.4);
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        padding: 10px 20px;
        transition: all 0.2s ease;
        border: none;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px -6px rgba(56, 189, 248, 0.5);
    }

    /* Sidebar Creator Card */
    .creator-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 16px;
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
                "content": "👋 **Hello! I'm Nova**, your 24/7 AI Gaming Concierge. You can ask me for live hints, how to play, or learn about the developer!"
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
    st.session_state.max_allowed_moves = st.session_state.optimal_steps + 2  # for 7-guess challenge
    st.session_state.ai_duel_turn = "Player"
    st.session_state.ai_duel_history = []
    st.session_state.agent_logs = [
        f"[{time.strftime('%H:%M:%S')}] Nexus Arbiter generated secret between {st.session_state.min_val} and {st.session_state.max_val}."
    ]

# First-time initialization
if "secret_number" not in st.session_state:
    init_game_state()


# ---------------------------------------------------------
# SIDEBAR: LUXURY CONTROL PANEL
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Live Agents Status Pill
    st.markdown("""
    <div style="display:flex; flex-direction:column; gap:8px; margin-bottom: 20px;">
        <div style="display:flex; align-items:center; gap:8px; background:rgba(15,23,42,0.7); border:1px solid rgba(16,185,129,0.3); padding:7px 12px; border-radius:10px; font-size:0.83rem; color:#34d399;">
            <span style="width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
            Arbiter Engine: Active
        </div>
        <div style="display:flex; align-items:center; gap:8px; background:rgba(15,23,42,0.7); border:1px solid rgba(56,189,248,0.3); padding:7px 12px; border-radius:10px; font-size:0.83rem; color:#38bdf8;">
            <span style="width:8px; height:8px; border-radius:50%; background:#38bdf8; box-shadow:0 0 8px #38bdf8;"></span>
            Nova AI Concierge: 24/7 Live
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Friendly Game Mode Selection
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
        "Select Experience:",
        mode_options,
        index=mode_options.index(current_mode),
        help="Classic: Relaxed play | Play Against AI: Turn-by-turn race | 7-Guess: Limited tries"
    )

    if selected_mode != st.session_state.game_mode:
        st.session_state.game_mode = selected_mode
        init_game_state(reset_lifetime=False)
        st.rerun()

    # Friendly Range Configuration
    st.markdown("#### 📏 Target Range")
    range_tier = st.radio(
        "Difficulty Level:",
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

    # Developer Portfolio Showcase Card
    st.markdown(f"""
    <div class="creator-card">
        <div style="font-size:0.75rem; text-transform:uppercase; color:#38bdf8; font-weight:700; letter-spacing:0.05em;">Engineered By</div>
        <div style="font-size:1.05rem; font-weight:800; color:#f8fafc; margin: 4px 0;">Sainbux (Hadi) Seelro</div>
        <div style="font-size:0.8rem; color:#94a3b8; margin-bottom:10px;">Agentic AI & Systems Developer</div>
        <a href="https://github.com/SainBux-HadiSeelro/nexus-mind-agentic-platform" target="_blank" style="text-decoration:none; display:inline-block; background:rgba(56,189,248,0.15); border:1px solid rgba(56,189,248,0.4); color:#38bdf8; padding:5px 12px; border-radius:8px; font-size:0.78rem; font-weight:600;">
            ⭐ View GitHub Repository
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Optional OpenAI Key
    with st.expander("🔑 Advanced: Add OpenAI Key (Optional)", expanded=False):
        user_api_key = st.text_input(
            "API Key:",
            type="password",
            placeholder="sk-...",
            help="Nova works 100% free with its autonomous built-in engine. Add an OpenAI key if you want to use GPT-4o-mini."
        )

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("🔄 Reset Score & Session", use_container_width=True):
        init_game_state(reset_lifetime=True)
        st.rerun()


# ---------------------------------------------------------
# HERO HEADER BANNER
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ Autonomous Agentic AI System</div>
    <div class="hero-title">Nexus Mind</div>
    <div class="hero-subtitle">
        An intelligent, multi-agent number deduction experience. Can you find the secret number before the autonomous AI opponent?
    </div>
    <div class="quick-chips-row">
        <div class="chip">🎯 <b>1. Pick a Guess</b></div>
        <div class="chip">📡 <b>2. Read AI Proximity Radar</b></div>
        <div class="chip">💬 <b>3. Ask Nova for 24/7 Hints</b></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# TOP TELEMETRY METRIC CARDS
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
    <div class="metric-card">
        <div class="metric-label">🎮 Games Played</div>
        <div class="metric-value">{stats_summary['games_played']}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🏆 Victories</div>
        <div class="metric-value" style="color:#10b981;">{stats_summary['games_won']}</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🎯 Win Rate</div>
        <div class="metric-value" style="color:#38bdf8;">{stats_summary['win_rate']}%</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔥 Win Streak</div>
        <div class="metric-value" style="color:#f59e0b;">{stats_summary['current_streak']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)


# ---------------------------------------------------------
# MAIN INTERFACE TABS
# ---------------------------------------------------------
tab_game, tab_chatbot, tab_specs, tab_logs = st.tabs([
    "🎮 Interactive Arena",
    "💬 Nova AI Concierge (24/7)",
    "🧠 Multi-Agent Architecture",
    "📜 Live Agent Logs"
])


# =========================================================
# TAB 1: INTERACTIVE ARENA
# =========================================================
with tab_game:
    col_play, col_clues = st.columns([1.3, 1.0])

    with col_play:
        st.markdown(f"### Active Mode: **{st.session_state.game_mode}**")
        
        # Sleek Target Search Range Visualizer
        total_span = max(1, st.session_state.max_val - st.session_state.min_val)
        active_span = max(1, st.session_state.active_high - st.session_state.active_low)
        eliminated_pct = int(((total_span - active_span) / total_span) * 100)
        remaining_count = active_span + 1

        st.markdown(f"""
        <div class="range-visualizer">
            <span class="range-endpoint">[{st.session_state.active_low}]</span>
            <span class="range-middle">━━━━ 🎯 TARGET HIDDEN ━━━━</span>
            <span class="range-endpoint">[{st.session_state.active_high}]</span>
        </div>
        """, unsafe_allow_html=True)

        st.progress(min(1.0, max(0.0, eliminated_pct / 100.0)), text=f"Search Space Eliminated: {eliminated_pct}% ({remaining_count} numbers remaining)")

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
            with st.form("modern_guess_form", clear_on_submit=False):
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
                    submit_guess = st.form_submit_button("⚡ Submit Guess", use_container_width=True, type="primary")

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
                <div class="glass-panel" style="border-left: 6px solid #10b981; background: radial-gradient(circle at 0% 0%, rgba(16,185,129,0.15) 0%, rgba(15,23,42,0.9) 100%);">
                    <h2 style="color:#10b981; margin:0 0 8px 0; font-size:1.8rem;">🎉 VICTORY ACHIEVED!</h2>
                    <p style="font-size:1.15rem; margin-bottom:12px;">You cracked the secret number <b>{st.session_state.secret_number}</b> in only <b>{st.session_state.attempts}</b> tries!</p>
                    <div style="font-size: 1.35rem; margin-bottom: 6px;">{badge.get('stars', '⭐⭐⭐')} <b>{badge['title']}</b></div>
                    <p style="color:#94a3b8; font-style:italic;">"{badge['verdict']}"</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-panel" style="border-left: 6px solid #ef4444; background: radial-gradient(circle at 0% 0%, rgba(239,68,68,0.15) 0%, rgba(15,23,42,0.9) 100%);">
                    <h3 style="color:#ef4444; margin-top:0;">Round Complete!</h3>
                    <p>The secret number was <b>{st.session_state.secret_number}</b>.</p>
                    <p>Ready for another round? Hit the button below!</p>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🚀 Play Another Round", type="primary", use_container_width=True):
                init_game_state(reset_lifetime=False)
                st.rerun()

        # EASY CLUE EXPANDER
        with st.expander("💡 Request Mathematical Clue from Nexus Arbiter", expanded=False):
            if not st.session_state.game_over:
                hint_text = arbiter_agent.generate_smart_hint(
                    st.session_state.secret_number,
                    st.session_state.active_low,
                    st.session_state.active_high,
                    max(1, st.session_state.attempts)
                )
                st.info(f"🤖 **Arbiter Clue:** {hint_text}")
                rec_guess = arbiter_agent.get_binary_search_recommendation(st.session_state.active_low, st.session_state.active_high)
                st.caption(f"Binary Search Midpoint Recommendation: **{rec_guess}**")
            else:
                st.write("Start a new round to unlock live tactical clues.")

    # CLUES & RECENT GUESSES COLUMN
    with col_clues:
        st.markdown("### 📡 Proximity Radar")
        
        # Last Feedback Callout
        if st.session_state.last_feedback:
            heat_class = {
                "🔥 BOILING HOT": "radar-boiling",
                "🌡️ WARM": "radar-warm",
                "🌤️ LUKEWARM": "radar-lukewarm",
                "❄️ SUB-ZERO COLD": "radar-cold"
            }.get(st.session_state.last_heat, "radar-lukewarm")

            st.markdown(f"""
            <div class="radar-box {heat_class}">
                <div style="font-size:0.8rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em;">Live Reading</div>
                <div style="font-size:1.3rem; font-weight:800; margin: 8px 0; color:#f8fafc;">{st.session_state.last_feedback}</div>
                <div style="font-size:1rem; font-weight:700; margin-top:8px;">{st.session_state.last_heat}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Submit your first guess to activate the live thermal sensor.")

        # Past Guesses
        if st.session_state.history:
            st.markdown("#### 📝 Guess History")
            for h in reversed(st.session_state.history[-5:]):
                st.markdown(f"• Try #{h['attempt']}: **{h['guess']}** ➔ `{h['status']}` ({h['heat']})")

        # AI Moves (if playing against AI)
        if st.session_state.game_mode == "🤖 Play Against AI" and st.session_state.ai_duel_history:
            st.markdown("#### 🤖 AI Rival History")
            for m in reversed(st.session_state.ai_duel_history[-4:]):
                st.markdown(f"• AI Turn #{m['turn']}: **{m['ai_guess']}** ➔ `{m['status']}`")


# =========================================================
# TAB 2: NOVA 24/7 AI HELPER CHATBOT
# =========================================================
with tab_chatbot:
    st.markdown("### 💬 Nova — 24/7 Live AI Concierge")
    st.caption("Nova monitors the live telemetry of your game session. Ask for strategic hints, application architecture, or developer portfolio details.")

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
    st.markdown("**Quick Inquiries:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    if qc1.button("💡 Tactical Hint", use_container_width=True):
        quick_query = "Can you give me an easy hint for my current number?"
    if qc2.button("❓ How Do I Play?", use_container_width=True):
        quick_query = "How do I play this game and win quickly?"
    if qc3.button("👨‍💻 Who Created This?", use_container_width=True):
        quick_query = "Who is the developer that built this game and what is their portfolio?"
    if qc4.button("🤖 Multi-Agent Architecture", use_container_width=True):
        quick_query = "Explain how the multi-agent AI system operates behind the scenes."

    # Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    chat_input = st.chat_input("Ask Nova anything about the game, hints, or developer portfolio...")
    user_prompt = quick_query or chat_input

    if user_prompt:
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Nova is reasoning over live telemetry..."):
                response_text = support_agent.respond(
                    user_message=user_prompt,
                    live_state=live_telemetry_snapshot,
                    api_key=user_api_key if 'user_api_key' in locals() and user_api_key else None
                )
                st.markdown(response_text)

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        st.session_state.agent_logs.append(
            f"[{time.strftime('%H:%M:%S')}] Nova Concierge responded to: '{user_prompt[:35]}...'."
        )


# =========================================================
# TAB 3: SYSTEM ARCHITECTURE (FOR RECRUITERS & TECHIES)
# =========================================================
with tab_specs:
    st.markdown("### 🧠 Multi-Agent AI System Architecture (For Technical Review)")
    st.markdown("""
    Underneath the intuitive UI is an **Agentic Multi-Agent System (MAS)** where dedicated autonomous agents
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
<div style="text-align: center; color: #64748b; font-size: 0.88rem; padding: 12px 0;">
    ⚡ <b>Nexus Mind</b> | Engineered by <b>Sainbux (Hadi) Seelro</b> (Agentic AI Developer) | 
    Featuring Autonomous Multi-Agent Swarms & 24/7 Live AI Concierge.
</div>
""", unsafe_allow_html=True)
