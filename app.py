import streamlit as st
from rag_engine import search_pdf
from csv_engine import search_csv
from txt_engine import search_txt
from gemini_engine import ask_gemini

st.set_page_config(page_title="Medical AI Assistant", layout="wide")
st.write("Welcome to your medical solutions")

st.title("🩺 AI Medical Assistant")

# Session memory
if "history" not in st.session_state:
    st.session_state.history = []

# Input
query = st.chat_input("Describe your symptoms...")

if query:
    st.session_state.history.append(("user", query))

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
        context = ""

    # Gemini response
    answer = ask_gemini(query, context)

    st.session_state.history.append(("bot", answer))

# Display chat
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)

# Footer
st.markdown("---")
st.markdown("⚠️ This is not medical advice. Always consult a doctor.")
