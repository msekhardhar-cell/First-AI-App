"""OmniChat AI - Interactive Quiz & Scoring Engine."""
import streamlit as st
from typing import List, Dict, Any

# Curated Fallback Quiz for Sandbox / Offline Testing
DEFAULT_QUIZ = [
    {
        "id": 1,
        "question": "In Python, which built-in data structure has O(1) average time complexity for key lookups?",
        "options": ["A) list", "B) tuple", "C) dict", "D) linked list"],
        "correct": 2,
        "explanation": "Dictionaries (dict) in Python are implemented using hash tables, offering O(1) average lookup complexity."
    },
    {
        "id": 2,
        "question": "What does temperature control in LLM text generation?",
        "options": [
            "A) The speed of the GPU execution",
            "B) The randomness and creativity of next-token selection",
            "C) The maximum number of tokens returned",
            "D) The memory usage during context caching"
        ],
        "correct": 1,
        "explanation": "Temperature scales the logits before applying softmax; lower values make output more deterministic, while higher values increase variance."
    },
    {
        "id": 3,
        "question": "Can quantum entanglement be utilized to send classical messages faster than the speed of light?",
        "options": [
            "A) Yes, because wave function collapse is instantaneous",
            "B) No, because measurement outcomes are fundamentally random and require classical communication to compare",
            "C) Yes, but only in deep vacuum",
            "D) Only between superconducting qubits"
        ],
        "correct": 1,
        "explanation": "According to the No-Communication Theorem in quantum mechanics, local measurements on entangled states cannot transmit controllable classical data FTL."
    },
    {
        "id": 4,
        "question": "In a Modular Monolith architecture, what is the primary mechanism to decouple domain boundaries?",
        "options": [
            "A) HTTP REST calls between all modules",
            "B) In-process interfaces, domain events, and explicit contracts",
            "C) Multiple independent physical databases per folder",
            "D) Separate Docker containers per service"
        ],
        "correct": 1,
        "explanation": "Modular monoliths maintain single-process efficiency while enforcing domain boundaries through clean interfaces and domain events without network overhead."
    }
]

def render_interactive_quiz(quiz_data: List[Dict[str, Any]] = None):
    """Renders a fully interactive multiple choice quiz with live scoring and explanations."""
    if not quiz_data:
        quiz_data = DEFAULT_QUIZ
        
    st.markdown("### 🎯 Interactive Study Quiz")
    st.caption("Test your comprehension with instant scoring and detailed explanations.")
    
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
        
    score = 0
    answered_count = 0
    total_questions = len(quiz_data)
    
    for q in quiz_data:
        qid = q["id"]
        st.markdown(f"**Q{qid}: {q['question']}**")
        
        user_choice = st.radio(
            f"Select your answer for Q{qid}:",
            options=range(len(q["options"])),
            format_func=lambda i, opts=q["options"]: opts[i],
            key=f"quiz_radio_{qid}",
            label_visibility="collapsed"
        )
        
        st.session_state.quiz_answers[qid] = user_choice
        
        # Immediate feedback check
        if user_choice is not None:
            answered_count += 1
            if user_choice == q["correct"]:
                score += 1
                st.success(f"✅ Correct! {q['explanation']}")
            else:
                st.error(f"❌ Incorrect. The correct answer was **{q['options'][q['correct']]}**.\n\n*{q['explanation']}*")
        st.divider()
        
    # Score Summary Banner
    if answered_count == total_questions:
        percentage = int((score / total_questions) * 100)
        if percentage >= 75:
            st.balloons()
            st.success(f"🏆 **Outstanding!** You scored **{score}/{total_questions}** ({percentage}%). You've mastered this topic!")
        else:
            st.info(f"📊 **Quiz Completed:** Score: **{score}/{total_questions}** ({percentage}%). Review the explanations above to strengthen key concepts.")
