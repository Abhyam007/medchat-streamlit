import streamlit as st

class Config:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    DB_PATH = "vectorstore/db_faiss"
    CSV_PATH = "data/medical.csv"
    TXT_PATH = "data/medical.txt"
