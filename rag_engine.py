import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config

@st.cache_resource
def load_embedding():
    try:
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    except Exception as e:
        print("❌ EMBEDDING ERROR:", e)
        return None


@st.cache_resource
def load_retriever():
    try:
        if not os.path.exists(Config.DB_PATH):
            print("⚠️ FAISS not found")
            return None

        embedding_model = load_embedding()

        if embedding_model is None:
            return None

        db = FAISS.load_local(
            Config.DB_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        return db.as_retriever(search_kwargs={'k': 3})

    except Exception as e:
        print("❌ FAISS ERROR:", e)
        return None


retriever = load_retriever()


def search_pdf(query):
    if retriever is None:
        return None, 0

    try:
        docs = retriever.invoke(query)

        if not docs:
            return None, 0

        context = " ".join([d.page_content[:200] for d in docs])
        score = len(context)

        return context, score

    except Exception as e:
        print("❌ SEARCH ERROR:", e)
        return None, 0
