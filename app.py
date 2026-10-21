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
    page_title="Nexus Mind // Smart AI Guessing Game",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM MODERN STYLING (FRIENDLY & CLEAN)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global App Canvas */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }

    /* Quick Guide Banner */
    .guide-banner {
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 20px;
    }

    /* Live Agent Indicator */
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
    }

    /* Hero Header */
    .hero-title {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 16px;
    }

    /* Proximity Radar Badges */
    .heat-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.03em;
    }
    .heat-boiling { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid #ef4444; }
    .heat-warm { background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid #f59e0b; }
    .heat-lukewarm { background: rgba(56, 189, 248, 0.25); color: #38bdf8; border: 1px solid #0284c7; }
    .heat-cold { background: rgba(99, 102, 241, 0.25); color: #a5b4fc; border: 1px solid #6366f1; }
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
                "content": "👋 **Hello! I'm Nova**, your 24/7 AI Helper. If you ever need an easy hint or want to know how the game works, just ask me below!"
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
        f"[{time.strftime('%H:%M:%S')}] Arbiter Agent picked secret number between {st.session_state.min_val} and {st.session_state.max_val}."
    ]

# First-time initialization
if "secret_number" not in st.session_state:
    init_game_state()


# ---------------------------------------------------------
# SIDEBAR: EASY CONTROLS & CREATOR INFO
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎮 Game Settings")
    
    # Live Agents Status Pill
    st.markdown("""
    <div style="display:flex; flex-direction:column; gap:6px; margin-bottom: 16px;">
        <div class="agent-pill"><div class="status-dot"></div> AI Game Arbiter: Online</div>
        <div class="agent-pill"><div class="status-dot"></div> Nova AI Helper: 24/7 Live</div>
    </div>
    """, unsafe_allow_html=True)

    # Friendly Game Mode Selection
    mode_options = [
        "🎯 Classic Mode",
        "🤖 Play Against AI",
        "⏳ 7-Guess Challenge"
    ]
    
    # Map from existing state if needed
    current_mode = st.session_state.game_mode
    if current_mode not in mode_options:
        current_mode = "🎯 Classic Mode"
        st.session_state.game_mode = current_mode

    selected_mode = st.selectbox(
        "Choose Game Mode:",
        mode_options,
        index=mode_options.index(current_mode),
        help="Classic: Play at your pace | Play Against AI: Race the computer | 7-Guess: Limited tries challenge!"
    )

    if selected_mode != st.session_state.game_mode:
        st.session_state.game_mode = selected_mode
        init_game_state(reset_lifetime=False)
        st.rerun()

    # Friendly Range Configuration
    st.markdown("#### 📏 Pick Number Range")
    range_tier = st.radio(
        "Difficulty:",
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
            new_min = st.number_input("From", value=1, step=1)
        with col_c2:
            new_max = st.number_input("To", value=100, step=10)

    if new_min >= new_max:
        st.error("Starting number must be less than ending number.")
        new_max = new_min + 10

    if new_min != st.session_state.min_val or new_max != st.session_state.max_val:
        st.session_state.min_val = int(new_min)
        st.session_state.max_val = int(new_max)
        init_game_state(reset_lifetime=False)
        st.rerun()

    st.markdown("---")

    # Developer Portfolio Showcase
    st.markdown("### 👨‍💻 Creator Dossier")
    st.markdown("""
    **Developer:** **Sainbux (Hadi) Seelro**  
    **Role:** Agentic AI & Systems Engineer  
    **Skills:** Autonomous Multi-Agent Swarms, Interactive AI Systems, Python  
    """)
    st.caption("🔗 [View GitHub Repository](https://github.com/SainBux-HadiSeelro/nexus-mind-agentic-platform)")

    # Optional OpenAI Key
    with st.expander("🔑 Advanced: Add OpenAI Key (Optional)", expanded=False):
        user_api_key = st.text_input(
            "API Key (Optional):",
            type="password",
            placeholder="sk-...",
            help="Nova already works 100% free with an autonomous built-in engine. Adding an OpenAI key is optional for GPT-4o-mini."
        )

    if st.button("🔄 Start Fresh / Reset Score", use_container_width=True):
        init_game_state(reset_lifetime=True)
        st.rerun()


# ---------------------------------------------------------
# TOP TELEMETRY METRIC CARDS (SIMPLE & CLEAR)
# ---------------------------------------------------------
stats_summary = analytics_agent.summarize_session({
    "games_played": st.session_state.games_played,
    "games_won": st.session_state.games_won,
    "current_streak": st.session_state.current_streak,
    "best_streak": st.session_state.best_streak,
    "best_score": st.session_state.best_score
})

m1, m2, m3, m4 = st.columns(4)
m1.metric("🎮 Rounds Played", stats_summary["games_played"])
m2.metric("🏆 Games Won", stats_summary["games_won"])
m3.metric("🎯 Win Rate", f"{stats_summary['win_rate']}%")
m4.metric("🔥 Win Streak", f"{stats_summary['current_streak']} in a row")

st.markdown("---")


# ---------------------------------------------------------
# HERO HEADER & SIMPLE 3-STEP GUIDE
# ---------------------------------------------------------
st.markdown("""
<div class="hero-title">🎯 Nexus Mind — Smart AI Number Game</div>
<div class="hero-subtitle">
    Can you find the secret number? An intelligent AI arbiter gives you hot & cold clues to help you win!
</div>

<div class="guide-banner">
    <b style="color:#38bdf8;">💡 How to Play in 3 Easy Steps:</b><br/>
    1️⃣ Type your guess in the box below and click <b>Check My Guess</b>.<br/>
    2️⃣ Watch the AI clue: It will tell you if your guess is <b>Too High</b>, <b>Too Low</b>, or <b>Getting Warm/Hot!</b><br/>
    3️⃣ If you ever get stuck, open the <b>💬 Nova AI Helper</b> tab for a free clue!
</div>
""", unsafe_allow_html=True)


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
# TAB 1: PLAY GAME (CLEAN & NON-TECHNICAL)
# =========================================================
with tab_game:
    col_play, col_clues = st.columns([1.3, 1.0])

    with col_play:
        st.markdown(f"### Current Mode: **{st.session_state.game_mode}**")
        
        # Friendly range progress bar
        total_span = max(1, st.session_state.max_val - st.session_state.min_val)
        active_span = max(1, st.session_state.active_high - st.session_state.active_low)
        eliminated_pct = int(((total_span - active_span) / total_span) * 100)
        remaining_count = active_span + 1

        st.markdown(f"🎯 **Target is between:** **`{st.session_state.active_low}`** and **`{st.session_state.active_high}`**")
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
            with st.form("simple_guess_form", clear_on_submit=False):
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
                <div class="glass-card" style="border-left: 6px solid #10b981;">
                    <h2 style="color:#10b981; margin:0 0 8px 0;">🎉 CONGRATULATIONS! YOU WON!</h2>
                    <p style="font-size:1.1rem; margin-bottom:12px;">You found the secret number <b>{st.session_state.secret_number}</b> in just <b>{st.session_state.attempts}</b> tries!</p>
                    <div style="font-size: 1.3rem; margin-bottom: 6px;">{badge.get('stars', '⭐⭐⭐')} <b>{badge['title']}</b></div>
                    <p style="color:#94a3b8; font-style:italic;">"{badge['verdict']}"</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="glass-card" style="border-left: 6px solid #ef4444;">
                    <h3 style="color:#ef4444; margin-top:0;">Good Effort!</h3>
                    <p>The secret number was <b>{st.session_state.secret_number}</b>.</p>
                    <p>Ready for another round? Hit the button below!</p>
                </div>
                """, unsafe_allow_html=True)

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
                st.write("Start a new game round to unlock clues.")

    # CLUES & RECENT GUESSES COLUMN
    with col_clues:
        st.markdown("### 📡 Live AI Sensor")
        
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
                <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase;">Latest AI Reading</div>
                <div style="font-size:1.25rem; font-weight:700; margin: 8px 0; color:#f8fafc;">{st.session_state.last_feedback}</div>
                <div style="margin-top:12px;">
                    <span class="heat-badge {heat_class}">{st.session_state.last_heat}</span>
                </div>
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
    st.markdown("### 💬 Nova — Your 24/7 AI Helper")
    st.caption("Nova knows everything happening in your game right now. Ask for an easy hint, how to play, or who created this app!")

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
    if qc3.button("👨‍💻 Who Created This Game?", use_container_width=True):
        quick_query = "Who is the developer that built this game and what is their portfolio?"
    if qc4.button("🤖 How Does the AI Work?", use_container_width=True):
        quick_query = "Explain how the AI agents work in simple words."

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
            f"[{time.strftime('%H:%M:%S')}] Nova AI Helper replied to: '{user_prompt[:35]}...'."
        )


# =========================================================
# TAB 3: SYSTEM ARCHITECTURE (FOR RECRUITERS & TECHIES)
# =========================================================
with tab_specs:
    st.markdown("### 🧠 Multi-Agent AI System Architecture (For Technical Review)")
    st.markdown("""
    This section showcases the **Agentic AI engineering** behind this platform.
    Under the friendly UI lies a decoupled **Multi-Agent System (MAS)** communicating via a centralized reactive state bus.
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
    - **Creator:** **Sainbux (Hadi) Seelro** | [GitHub Repo](https://github.com/SainBux-HadiSeelro/nexus-mind-agentic-platform)
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
<div style="text-align: center; color: #64748b; font-size: 0.88rem; padding: 10px 0;">
    🎯 <b>Nexus Mind</b> | Created by <b>Sainbux (Hadi) Seelro</b> (Agentic AI Developer) | 
    Powered by Autonomous Multi-Agent Systems & 24/7 Live AI Helper.
</div>
""", unsafe_allow_html=True)
