import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config

# -----------------------------
# LOAD EMBEDDING MODEL (CACHED)
# -----------------------------
@st.cache_resource
def load_embedding():
    try:
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    except Exception as e:
        print("❌ EMBEDDING ERROR:", e)
        return None


# -----------------------------
# LOAD FAISS DB (SAFE)
# -----------------------------
@st.cache_resource
def load_retriever():
    try:
        if not os.path.exists(Config.DB_PATH):
            print("⚠️ FAISS path not found:", Config.DB_PATH)
            return None

        embedding_model = load_embedding()

        if embedding_model is None:
            return None

        db = FAISS.load_local(
            Config.DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        retriever = db.as_retriever(search_kwargs={"k": 3})

        print("✅ FAISS loaded successfully")
        return retriever

    except Exception as e:
        print("❌ FAISS ERROR:", e)
        return None


# Initialize retriever (cached)
retriever = load_retriever()


# -----------------------------
# SEARCH FUNCTION
# -----------------------------
def search_pdf(query):
    """
    Returns:
        context (str or None)
        score (int)
    """

    if retriever is None:
        return None, 0

    try:
        docs = retriever.invoke(query)

        if not docs:
            return None, 0

        # Combine top chunks
        context = " ".join([d.page_content[:200] for d in docs])

        # Simple confidence score
        score = len(context)

        return context, score

    except Exception as e:
        print("❌ SEARCH ERROR:", e)
        return None, 0
