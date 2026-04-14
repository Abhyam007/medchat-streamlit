import streamlit as st
from rag_engine import search_pdf
from csv_engine import search_csv
from txt_engine import search_txt
from gemini_engine import ask_gemini

st.set_page_config(page_title="Medical AI Assistant", layout="wide")

# ----------- UI STYLING -----------
st.markdown("""
<style>
.main-container {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background: #007bff;
    color: white;
    padding: 10px;
    border-radius: 12px;
    margin: 5px 0;
    text-align: right;
}

.bot-msg {
    background: #f1f3f4;
    padding: 10px;
    border-radius: 12px;
    margin: 5px 0;
}

.alert-high {
    background: #ff9800;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
}

.alert-critical {
    background: #ff4d4d;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
}

.header {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.markdown('<div class="header">🩺 AI Medical Assistant</div>', unsafe_allow_html=True)
st.markdown("### Welcome to your medical solutions")

# ----------- SESSION MEMORY -----------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------- SEVERITY DETECTION -----------
def detect_severity(query):
    q = query.lower()

    if "2 weeks" in q or "persistent" in q or "long time" in q:
        return "high"

    if "chest pain" in q or "breathing problem" in q or "unable to breathe" in q:
        return "critical"

    return "normal"

# ----------- INPUT -----------
query = st.chat_input("Describe your symptoms...")

if query:
    st.session_state.history.append(("user", query))

    # Severity check
    severity = detect_severity(query)

    # STEP 1: PDF
    context, score = search_pdf(query)

    if score > 50:
        source = "PDF"
    else:
        # STEP 2: CSV
        context, score = search_csv(query)

        if score:
            source = "CSV"
        else:
            # STEP 3: TXT
            context, score = search_txt(query)
            source = "TXT" if score else "None"

    # Fallback context
    if not context:
        context = "General medical knowledge"

    # Gemini response
    answer = ask_gemini(query, context)

    # ----------- ADD SEVERITY ALERTS -----------
    if severity == "high":
        answer = "⚠️ This seems persistent. Please consult a doctor soon.\n\n" + answer

    if severity == "critical":
        answer = "🚨 URGENT: Seek immediate medical attention.\n\n" + answer

    st.session_state.history.append(("bot", answer))

# ----------- DISPLAY CHAT -----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ----------- FOOTER -----------
st.markdown("---")
st.markdown("⚠️ This is not medical advice. Always consult a doctor.")
