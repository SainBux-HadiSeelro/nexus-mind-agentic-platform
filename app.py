"""
Nexus Mind: Autonomous Multi-Agent Gaming & Intelligence Platform
Engineered by an Agentic AI Developer.
Demonstrating real-time state synchronization, multi-agent arbitration,
Shannon entropy analysis, and a 24/7 live contextual customer support agent.
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
    page_title="Nexus Mind // Agentic AI Gaming Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM MODERN GLASSMORPHISM CYBERPUNK STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global Background & Typography */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
    }

    /* Agent Status Pill Bar */
    .agent-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 9999px;
        padding: 6px 14px;
        font-size: 0.82rem;
        font-weight: 500;
        color: #38bdf8;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.85); }
    }

    /* Hero Header */
    .hero-title {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 18px;
    }

    /* Radar Heat Indicator */
    .heat-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .heat-boiling { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
    .heat-warm { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
    .heat-lukewarm { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #0284c7; }
    .heat-cold { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; border: 1px solid #6366f1; }

    /* Button Enhancements */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
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
    support = SupportAgent()
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
                "content": "👋 **Welcome to Nexus Mind!** I'm **Nova**, your 24/7 Autonomous AI Concierge. I have live telemetry access to this entire application. Feel free to ask for hints, analyze your guessing entropy, or inquire about the developer's portfolio!"
            }
        ]

    # Current Round Configuration
    if "min_val" not in st.session_state:
        st.session_state.min_val = 1
    if "max_val" not in st.session_state:
        st.session_state.max_val = 100
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "🎯 Adaptive Arena"

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
    st.session_state.max_allowed_moves = st.session_state.optimal_steps + 2  # for Quantum countdown
    st.session_state.ai_duel_turn = "Player"
    st.session_state.ai_duel_history = []
    st.session_state.agent_logs = [
        f"[{time.strftime('%H:%M:%S')}] Arbiter Agent initialized secret in [{st.session_state.min_val}..{st.session_state.max_val}]."
    ]

# First-time initialization
if "secret_number" not in st.session_state:
    init_game_state()


# ---------------------------------------------------------
# SIDEBAR: CONTROL CENTER & PORTFOLIO TELEMETRY
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Agentic Control Center")
    
    # Live Agents Status Pill
    st.markdown("""
    <div style="display:flex; flex-direction:column; gap:8px; margin-bottom: 18px;">
        <div class="agent-pill"><div class="status-dot"></div> Arbiter Engine: Online</div>
        <div class="agent-pill"><div class="status-dot"></div> Oracle Analytics: Active</div>
        <div class="agent-pill"><div class="status-dot"></div> Nova 24/7 Concierge: Live</div>
    </div>
    """, unsafe_allow_html=True)

    # Game Mode Selection
    selected_mode = st.selectbox(
        "Select Operation Mode:",
        ["🎯 Adaptive Arena", "🤖 Human vs AI Agent Duel", "⚡ Quantum Countdown"],
        index=["🎯 Adaptive Arena", "🤖 Human vs AI Agent Duel", "⚡ Quantum Countdown"].index(st.session_state.game_mode)
    )

    if selected_mode != st.session_state.game_mode:
        st.session_state.game_mode = selected_mode
        init_game_state(reset_lifetime=False)
        st.rerun()

    # Range Configuration
    st.markdown("#### 📏 Search Bounds")
    range_tier = st.radio(
        "Difficulty Range:",
        ["Casual (1 - 20)", "Standard (1 - 100)", "Master (1 - 500)", "Custom Range"],
        index=1
    )

    new_min, new_max = st.session_state.min_val, st.session_state.max_val
    if range_tier == "Casual (1 - 20)":
        new_min, new_max = 1, 20
    elif range_tier == "Standard (1 - 100)":
        new_min, new_max = 1, 100
    elif range_tier == "Master (1 - 500)":
        new_min, new_max = 1, 500
    else:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            new_min = st.number_input("Min", value=1, step=1)
        with col_c2:
            new_max = st.number_input("Max", value=200, step=10)

    if new_min >= new_max:
        st.error("Min value must be less than Max value.")
        new_max = new_min + 10

    if new_min != st.session_state.min_val or new_max != st.session_state.max_val:
        st.session_state.min_val = int(new_min)
        st.session_state.max_val = int(new_max)
        init_game_state(reset_lifetime=False)
        st.rerun()

    st.markdown("---")

    # Optional LLM Key for Nova Support Agent
    st.markdown("#### 🔑 Optional LLM Brain")
    user_api_key = st.text_input(
        "OpenAI API Key (Optional):",
        type="password",
        placeholder="sk-...",
        help="Optional: Nova has a full autonomous offline reasoning engine built-in. If you add an OpenAI key, Nova uses GPT-4o-mini with live state injection."
    )

    st.markdown("---")

    # Developer Portfolio Showcase
    st.markdown("### 👨‍💻 Developer Dossier")
    st.markdown("""
    **Architect:** Agentic AI Developer  
    **Specialization:** Autonomous Multi-Agent Swarms, RAG Pipelines & Cognitive Systems  
    **Frameworks:** Python, Streamlit, LangChain/CrewAI Patterns, Entropy Engines  
    """)
    st.info("⭐ *This application is engineered as a portfolio showcase demonstrating agentic state synchronization, resilience, and interactive design.*")

    if st.button("🔄 Reset Entire Session", help="Clears lifetime stats and restarts fresh"):
        init_game_state(reset_lifetime=True)
        st.rerun()


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

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("🎮 Rounds Played", stats_summary["games_played"])
m2.metric("🏆 Victories", stats_summary["games_won"])
m3.metric("🎯 Win Rate", f"{stats_summary['win_rate']}%")
m4.metric("🔥 Current Streak", stats_summary["current_streak"])
m5.metric("⚡ Best Efficiency", f"{stats_summary['best_score']}%" if stats_summary['best_score'] != "--" else "--")

st.markdown("---")


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="hero-title">🧠 NEXUS MIND // Multi-Agent Decision Engine</div>
<div class="hero-subtitle">
    Next-generation probabilistic gaming powered by autonomous AI agents with real-time entropy telemetry & 24/7 live concierge.
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# MAIN INTERFACE TABS
# ---------------------------------------------------------
tab_game, tab_chatbot, tab_specs, tab_inspect = st.tabs([
    "🎮 Interactive Arena",
    "💬 Nova 24/7 Live AI Concierge",
    "📋 System Specifications & Docs",
    "🔍 Real-time Agent Telemetry & Logs"
])


# =========================================================
# TAB 1: INTERACTIVE ARENA
# =========================================================
with tab_game:
    col_play, col_radar = st.columns([1.3, 1.0])

    with col_play:
        st.markdown(f"### Mode: {st.session_state.game_mode}")
        
        # Interval search progress
        total_span = max(1, st.session_state.max_val - st.session_state.min_val)
        active_span = max(1, st.session_state.active_high - st.session_state.active_low)
        eliminated_pct = int(((total_span - active_span) / total_span) * 100)

        st.markdown(f"**Search Boundary:** `{st.session_state.active_low}` ➔ **`?`** ➔ `{st.session_state.active_high}`")
        st.progress(min(1.0, max(0.0, eliminated_pct / 100.0)), text=f"Search Space Eliminated: {eliminated_pct}%")

        if st.session_state.game_mode == "⚡ Quantum Countdown":
            moves_left = max(0, st.session_state.max_allowed_moves - st.session_state.attempts)
            st.warning(f"⏳ **Moves Remaining:** {moves_left} / {st.session_state.max_allowed_moves} (Theoretical Optimal: {st.session_state.optimal_steps})")
            if moves_left <= 0 and not st.session_state.game_over:
                st.session_state.game_over = True
                st.session_state.game_won = False
                st.session_state.current_streak = 0
                st.session_state.games_played += 1
                st.error(f"💥 Quantum collapse! You ran out of moves. The secret number was **{st.session_state.secret_number}**.")

        # GUESS INPUT FORM
        if not st.session_state.game_over:
            with st.form("guess_form", clear_on_submit=False):
                col_inp, col_btn = st.columns([2, 1])
                with col_inp:
                    user_guess = st.number_input(
                        "Input your deduction:",
                        min_value=int(st.session_state.min_val),
                        max_value=int(st.session_state.max_val),
                        value=int((st.session_state.active_low + st.session_state.active_high) // 2),
                        step=1,
                        help="Enter a guess within the active search boundary."
                    )
                with col_btn:
                    st.write("")
                    st.write("")
                    submit_guess = st.form_submit_button("⚡ Submit Deduction", use_container_width=True)

            if submit_guess and not st.session_state.game_over:
                st.session_state.attempts += 1
                status, feedback, heat = arbiter_agent.evaluate_guess(user_guess, st.session_state.secret_number)
                st.session_state.last_feedback = feedback
                st.session_state.last_heat = heat

                # Update active search boundaries
                if status == "TOO_LOW":
                    st.session_state.active_low = max(st.session_state.active_low, user_guess + 1)
                elif status == "TOO_HIGH":
                    st.session_state.active_high = min(st.session_state.active_high, user_guess - 1)

                # Record in history
                st.session_state.history.append({
                    "attempt": st.session_state.attempts,
                    "guess": user_guess,
                    "status": status,
                    "heat": heat,
                    "window": f"[{st.session_state.active_low}..{st.session_state.active_high}]"
                })

                # Agent log
                st.session_state.agent_logs.append(
                    f"[{time.strftime('%H:%M:%S')}] User guessed {user_guess} -> {status} ({heat}). New bracket: [{st.session_state.active_low}..{st.session_state.active_high}]."
                )

                # CHECK WIN CONDITION
                if status == "WIN":
                    st.session_state.game_over = True
                    st.session_state.game_won = True
                    st.session_state.games_played += 1
                    st.session_state.games_won += 1
                    st.session_state.current_streak += 1
                    st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.current_streak)

                    # Compute efficiency
                    efficiency = analytics_agent.calculate_efficiency(st.session_state.optimal_steps, st.session_state.attempts)
                    if st.session_state.best_score is None or efficiency > st.session_state.best_score:
                        st.session_state.best_score = efficiency

                    st.session_state.last_efficiency = efficiency
                    st.balloons()
                    st.rerun()

                # IF AI DUEL MODE: AI takes turn
                elif st.session_state.game_mode == "🤖 Human vs AI Agent Duel" and not st.session_state.game_over:
                    ai_guess = arbiter_agent.autonomous_ai_guess(st.session_state.active_low, st.session_state.active_high, strategy="optimal")
                    ai_status, ai_feedback, ai_heat = arbiter_agent.evaluate_guess(ai_guess, st.session_state.secret_number)
                    
                    st.session_state.ai_duel_history.append({
                        "turn": len(st.session_state.ai_duel_history) + 1,
                        "ai_guess": ai_guess,
                        "status": ai_status,
                        "heat": ai_heat
                    })

                    st.session_state.agent_logs.append(
                        f"[{time.strftime('%H:%M:%S')}] Autonomous AI Rival guessed {ai_guess} -> {ai_status} ({ai_heat})."
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
                        st.warning(f"🤖 Autonomous AI Rival guessed **{ai_guess}** and cracked the secret before you!")
                        st.rerun()

                st.rerun()

        # REVEAL POST-GAME VERDICT
        if st.session_state.game_over:
            if st.session_state.game_won:
                efficiency = analytics_agent.calculate_efficiency(st.session_state.optimal_steps, st.session_state.attempts)
                badge = analytics_agent.evaluate_performance_badge(efficiency, st.session_state.attempts, st.session_state.optimal_steps)
                
                st.markdown(f"""
                <div class="glass-card" style="border-left: 6px solid #10b981;">
                    <h3 style="color:#10b981; margin-top:0;">🏆 TARGET NEUTRALIZED!</h3>
                    <p>You cracked the secret <b>{st.session_state.secret_number}</b> in <b>{st.session_state.attempts}</b> deduction steps.</p>
                    <p><b>Oracle Performance Badge:</b> <span style="background:{badge['color']}33; color:{badge['color']}; padding: 4px 10px; border-radius:6px; font-weight:700;">{badge['title']}</span></p>
                    <p><b>Efficiency Rating:</b> {efficiency}% (Optimal: {st.session_state.optimal_steps} moves)</p>
                    <p><i>"{badge['verdict']}"</i></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 6px solid #ef4444;">
                    <h3 style="color:#ef4444; margin-top:0;">🛑 ROUND TERMINATED</h3>
                    <p>The secret number was <b>{st.session_state.secret_number}</b>.</p>
                    <p>Don't worry! Analyze your entropy tree and attempt another challenge.</p>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🚀 Launch Next Game Round", type="primary", use_container_width=True):
                init_game_state(reset_lifetime=False)
                st.rerun()

        # CLUE & HINT EXPANDER
        with st.expander("💡 Request Tactical Agent Clue (Mathematical Deductions)", expanded=False):
            if not st.session_state.game_over:
                hint_text = arbiter_agent.generate_smart_hint(
                    st.session_state.secret_number,
                    st.session_state.active_low,
                    st.session_state.active_high,
                    max(1, st.session_state.attempts)
                )
                st.info(f"🤖 **Nexus Arbiter Mathematical Clue:**\n\n{hint_text}")
                rec_guess = arbiter_agent.get_binary_search_recommendation(st.session_state.active_low, st.session_state.active_high)
                st.caption(f"Theoretical Binary Search Midpoint: **{rec_guess}**")
            else:
                st.write("Start a new game to unlock real-time tactical clues.")

    # RADAR & TELEMETRY COLUMN
    with col_radar:
        st.markdown("### 📡 Live Sensor Telemetry")
        
        # Last Feedback Callout
        if st.session_state.last_feedback:
            heat_class = {
                "🔥 BOILING HOT": "heat-boiling",
                "🌡️ WARM": "heat-warm",
                "🌤️ LUKEWARM": "heat-lukewarm",
                "❄️ SUB-ZERO COLD": "heat-cold"
            }.get(st.session_state.last_heat, "heat-lukewarm")

            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase;">Latest Arbiter Reading</div>
                <div style="font-size:1.15rem; font-weight:600; margin: 6px 0;">{st.session_state.last_feedback}</div>
                <div style="margin-top:10px;">
                    <span class="heat-badge {heat_class}">{st.session_state.last_heat}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Shannon Entropy Meter
        remaining_range = max(1, st.session_state.active_high - st.session_state.active_low + 1)
        total_range = max(1, st.session_state.max_val - st.session_state.min_val + 1)
        current_entropy = analytics_agent.compute_entropy_remaining(remaining_range, total_range)
        max_entropy = analytics_agent.compute_entropy_remaining(total_range, total_range)

        st.markdown(f"""
        <div class="glass-card">
            <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase;">Shannon Entropy Remaining</div>
            <div style="font-size:1.8rem; font-weight:800; color:#38bdf8;">{current_entropy} <span style="font-size:0.95rem; color:#64748b;">bits</span></div>
            <div style="font-size:0.82rem; color:#94a3b8;">Initial Entropy: {max_entropy} bits | Search Space: {remaining_range} possibilities</div>
        </div>
        """, unsafe_allow_html=True)

        # Guess History Log Table
        if st.session_state.history:
            st.markdown("#### 📜 Deduction Sequence")
            for h in reversed(st.session_state.history[-5:]):
                st.markdown(f"`#{h['attempt']}` Guess: **{h['guess']}** ➔ `{h['status']}` ({h['heat']}) | Bound: `{h['window']}`")

        # AI Rival History (if duel mode)
        if st.session_state.game_mode == "🤖 Human vs AI Agent Duel" and st.session_state.ai_duel_history:
            st.markdown("#### 🤖 Autonomous AI Moves")
            for m in reversed(st.session_state.ai_duel_history[-4:]):
                st.markdown(f"🤖 AI Turn #{m['turn']}: Guess **{m['ai_guess']}** ➔ `{m['status']}` ({m['heat']})")


# =========================================================
# TAB 2: NOVA 24/7 LIVE AI CONCIERGE CHATBOT
# =========================================================
with tab_chatbot:
    st.markdown("### 💬 Nova 24/7 Live Autonomous Agent")
    st.caption("Nova monitors all live telemetry on this website, guides players with mathematical clues, answers customer queries, and showcases developer portfolio capabilities.")

    # Live State Snapshot passed to Nova
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
        "last_feedback": st.session_state.last_feedback,
        "last_efficiency": st.session_state.get("last_efficiency", "--")
    }

    # Quick Action Prompt Chips
    st.markdown("**Quick Inquiries:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    if qc1.button("💡 Tactical Hint", use_container_width=True):
        quick_query = "Can you provide a tactical hint for the current secret number based on our live interval?"
    if qc2.button("📊 Live Status & Score", use_container_width=True):
        quick_query = "What is my current game status, win streak, and algorithmic efficiency?"
    if qc3.button("👨‍💻 Architect Portfolio", use_container_width=True):
        quick_query = "Tell me about the Agentic AI Developer who built this platform and their skillset."
    if qc4.button("⚙️ Multi-Agent Architecture", use_container_width=True):
        quick_query = "How does this autonomous multi-agent system work under the hood?"

    # Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle User Input
    chat_input = st.chat_input("Ask Nova anything about the game, hints, or developer portfolio...")
    user_prompt = quick_query or chat_input

    if user_prompt:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generate response via SupportAgent
        with st.chat_message("assistant"):
            with st.spinner("Nova is processing live application telemetry..."):
                response_text = support_agent.respond(
                    user_message=user_prompt,
                    live_state=live_telemetry_snapshot,
                    api_key=user_api_key if user_api_key else None
                )
                st.markdown(response_text)

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        st.session_state.agent_logs.append(
            f"[{time.strftime('%H:%M:%S')}] Nova Concierge handled user inquiry: '{user_prompt[:35]}...'."
        )


# =========================================================
# TAB 3: SPECIFICATIONS & ARCHITECTURE DOCS
# =========================================================
with tab_specs:
    st.markdown("### 📋 Platform Specifications & Architecture")
    st.markdown("""
    This project is engineered using **Agentic AI Architecture** patterns, separating concerns into autonomous agents
    with dedicated responsibilities, dynamic state arbitration, and telemetry feedback loops.
    """)

    st.markdown("""
    #### 🏗️ Multi-Agent System Topology
    ```mermaid
    flowchart TD
        User([👤 Human Player / Client]) -->|1. Submit Deduction / Query| UI[🖥️ Streamlit Cyberpunk Interface]
        UI -->|Synchronize State| Core[🧠 Session State Manager]
        Core -->|Evaluate Move| Arbiter[⚖️ Nexus Arbiter Agent]
        Arbiter -->|Calculate Clues & Bounds| Core
        Core -->|Telemetry Stream| Oracle[📊 Oracle Analytics Agent]
        Oracle -->|Shannon Entropy & Efficiency| UI
        UI -->|Live Telemetry Ingestion| Nova[🤖 Nova 24/7 AI Concierge]
        Nova -->|Dual Engine: Offline Heuristic + LLM| User
    ```
    """)

    st.markdown("""
    #### 📦 Component Matrix
    | Agent / Module | Responsibility | Key Mathematical / Algorithmic Concept |
    | :--- | :--- | :--- |
    | **Nexus Arbiter Agent** | Manages game rounds, narrows bounds, generates progressive mathematical clues, controls AI rival. | Binary Search Partitioning, Divisibility & Prime sieve. |
    | **Oracle Analytics Agent** | Evaluates decision optimality, tracks win streaks, Shannon entropy reduction. | $H = \\log_2(N)$ Information Entropy, $O(\\log N)$ Efficiency Index. |
    | **Nova 24/7 Support Concierge** | Live web concierge, answers questions, guides visitors, portfolio inquiries. | Contextual RAG, Intent Parsing, Graceful Offline Degradation. |
    | **Cyberpunk UI Engine** | Glassmorphic design, dynamic progress tracking, thermal radar. | CSS3 Backdrop Filter, Event-driven Streamlit Rerender. |
    """)

    st.markdown("""
    #### 🚀 Key Production Highlights
    - **Zero-Downtime Guarantee:** Built-in Autonomous Heuristic engine ensures Nova operates 24/7 without requiring third-party API keys or internet connection.
    - **Dual-Engine Flexibility:** Seamlessly accepts OpenAI/Gemini/Groq compatible API keys to upgrade Nova to live LLM generation with live state injection.
    - **Mathematical Precision:** Every clue and efficiency rating is derived from computational complexity theory and binary search bounds.
    """)


# =========================================================
# TAB 4: REAL-TIME AGENT TELEMETRY & LOGS
# =========================================================
with tab_inspect:
    st.markdown("### 🔍 Real-Time Multi-Agent Execution Log")
    st.caption("Live event stream of inter-agent messages, state changes, and evaluation loops.")

    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        st.markdown("#### 📜 Event Stream")
        for log in reversed(st.session_state.agent_logs[-15:]):
            st.code(log, language="bash")

    with col_l2:
        st.markdown("#### 💾 Current State Dump")
        st.json({
            "secret_number": "[PROTECTED]" if not st.session_state.game_over else st.session_state.secret_number,
            "active_boundary": [st.session_state.active_low, st.session_state.active_high],
            "attempts": st.session_state.attempts,
            "optimal_steps": st.session_state.optimal_steps,
            "game_mode": st.session_state.game_mode,
            "game_over": st.session_state.game_over,
            "game_won": st.session_state.game_won,
            "games_played": st.session_state.games_played,
            "games_won": st.session_state.games_won,
            "current_streak": st.session_state.current_streak,
            "best_streak": st.session_state.best_streak
        })


# ---------------------------------------------------------
# FOOTER: PORTFOLIO SIGNATURE
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.88rem; padding: 12px 0;">
    ⚡ <b>Nexus Mind Platform</b> | Crafted with precision by an <b>Agentic AI Developer</b> | 
    Featuring Autonomous Multi-Agent Systems, Shannon Entropy Engine & 24/7 Live AI Concierge.
</div>
""", unsafe_allow_html=True)
