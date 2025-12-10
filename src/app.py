import streamlit as st
import time
import random
from puzzle_generator import generate_puzzle
from tracker import PerformanceTracker
from adaptive_engine import adjust_difficulty

# --- Page Configuration ---
st.set_page_config(
    page_title="Math Adventures",
    page_icon="🌌",
    layout="centered"
)

# --- Subtle Dark Animated CSS ---
st.markdown("""
<style>
    /* Dark Animated Background (Subtle) */
    .stApp {
        background: linear-gradient(300deg, #0f2027, #203a43, #2c5364);
        background-size: 180% 180%;
        animation: gradient-animation 18s ease infinite;
        color: #ffffff;
    }

    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05); /* Very subtle white tint */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        margin-bottom: 20px;
    }

    /* Typography */
    h1, h2, h3, p, label {
        color: #f0f0f0 !important;
    }
    
    .big-question {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: 700;
        color: #64ffda; /* Neon cyan */
        text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
        margin: 10px 0;
    }
    
    /* Input Styling Override */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.3);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Metrics */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    div[data-testid="metric-container"] label {
        color: #aaaaaa !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'tracker' not in st.session_state: st.session_state.tracker = PerformanceTracker()
if 'difficulty' not in st.session_state: st.session_state.difficulty = "Easy"
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'current_puzzle' not in st.session_state: st.session_state.current_puzzle = None
if 'current_answer' not in st.session_state: st.session_state.current_answer = None
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'feedback_msg' not in st.session_state: st.session_state.feedback_msg = None
if 'is_correct_last' not in st.session_state: st.session_state.is_correct_last = False

def start_new_game():
    if st.session_state.user_name.strip():
        st.session_state.game_active = True
        st.session_state.tracker = PerformanceTracker()
        st.session_state.difficulty = "Easy"
        st.session_state.feedback_msg = None
        generate_next_puzzle()

def generate_next_puzzle():
    problem, answer = generate_puzzle(st.session_state.difficulty)
    st.session_state.current_puzzle = problem
    st.session_state.current_answer = answer
    st.session_state.tracker.start_timer()

def check_answer():
    user_val = st.session_state.answer_input
    if user_val:
        try:
            val = int(user_val)
            is_correct = (val == st.session_state.current_answer)
        except ValueError:
            is_correct = False

        # Log & Adapt
        last_record = st.session_state.tracker.log_attempt(st.session_state.difficulty, is_correct)
        st.session_state.difficulty = adjust_difficulty(st.session_state.difficulty, last_record)
        
        # Feedback
        st.session_state.is_correct_last = is_correct
        if is_correct:
            st.session_state.feedback_msg = f"✨ Correct! ({last_record['time_taken']}s)"
        else:
            st.session_state.feedback_msg = f"❌ Incorrect. Answer: {st.session_state.current_answer}"
            
        generate_next_puzzle()
        st.session_state.answer_input = "" 
        
# --- UI Rendering ---

if not st.session_state.game_active:
    st.markdown("<h1 style='text-align: center;'>🌌 Math Adventures</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc;'>Begin your journey through the cosmos of calculation.</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("Enter Explorer Name:", key="user_name", placeholder="Captain...")
        if st.button("Launch Mission 🚀", use_container_width=True):
            start_new_game()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"## 👩‍🚀 {st.session_state.user_name}")
        st.divider()
        stats = st.session_state.tracker.get_summary()
        if isinstance(stats, dict):
            st.metric("Streak", stats.get('streak', 0))
            st.metric("Accuracy", stats.get('accuracy', "0%"))
            st.metric("Avg Time", stats.get('avg_time', "0.00s"))
            st.metric("Solved", stats.get('total_attempts', 0))
        
        st.divider()
        st.write(f"Level: **{st.session_state.difficulty}**")
        if st.button("Abort Mission"):
            st.session_state.game_active = False
            st.rerun()

    # Main HUD
    # Progress
    levels = ["Easy", "Medium", "Hard"]
    try:
        progress = (levels.index(st.session_state.difficulty) + 1) / 3
    except:
        progress = 0
    st.progress(progress)

    # Feedback
    if st.session_state.feedback_msg:
        if st.session_state.is_correct_last:
            st.balloons()
            st.success(st.session_state.feedback_msg, icon="✨")
        else:
            st.error(st.session_state.feedback_msg, icon="⚠️")

    # Puzzle Area
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="big-question">{st.session_state.current_puzzle} = ?</div>', unsafe_allow_html=True)
    
    with st.form("answer_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("Answer", key="answer_input", label_visibility="collapsed", placeholder="Enter value...")
        with col2:
            st.form_submit_button("Engage ⚡", on_click=check_answer, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
