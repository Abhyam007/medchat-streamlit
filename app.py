import streamlit as st
from rag_engine import search_pdf
from csv_engine import search_csv
from txt_engine import search_txt
from gemini_engine import ask_gemini

st.set_page_config(page_title="Medical AI Assistant", layout="wide")

# ----------- UI STYLING -----------
st.markdown("""
<style>

/* BACKGROUND */
body {
    background-color: #0e1117;
}

/* MAIN CONTAINER */
.main-container {
    max-width: 800px;
    margin: auto;
}

/* USER MESSAGE */
.user-msg {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white;
    padding: 12px;
    border-radius: 14px;
    margin: 8px 0;
    text-align: right;
    font-size: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* BOT MESSAGE */
.bot-msg {
    background: #1c1f26;
    color: #e6edf3;
    padding: 12px;
    border-radius: 14px;
    margin: 8px 0;
    font-size: 15px;
    border: 1px solid #30363d;
}

/* ALERT HIGH */
.alert-high {
    background: #ff9800;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
    font-weight: bold;
}

/* ALERT CRITICAL */
.alert-critical {
    background: #ff4d4d;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
    font-weight: bold;
}

/* HEADER */
.header {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 5px;
    color: #e6edf3;
}

/* SUBTEXT */
.subtext {
    text-align: center;
    color: #8b949e;
    margin-bottom: 20px;
}

/* INPUT FIX */
.stChatInputContainer {
    background-color: #161b22 !important;
    border-top: 1px solid #30363d !important;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #8b949e;
    font-size: 14px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.markdown('<div class="header">🩺 AI Medical Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Welcome to your medical solutions</div>', unsafe_allow_html=True)

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

    # ----------- SEVERITY ALERTS -----------
    if severity == "high":
        answer = f"""
<div class="alert-high">
⚠️ This seems persistent. Please consult a doctor soon.
</div>
{answer}
"""

    if severity == "critical":
        answer = f"""
<div class="alert-critical">
🚨 URGENT: Seek immediate medical attention.
</div>
{answer}
"""

    st.session_state.history.append(("bot", answer))

# ----------- DISPLAY CHAT -----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ----------- FOOTER -----------
st.markdown("---")
st.markdown('<div class="footer">⚠️ This is not medical advice. Always consult a doctor.</div>', unsafe_allow_html=True)
