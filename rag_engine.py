from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config

# Load once (IMPORTANT)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    Config.DB_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={'k': 3})

def search_pdf(query):
    try:
        docs = retriever.invoke(query)

        if not docs:
            return None, 0

        context = " ".join([d.page_content[:200] for d in docs])

        # confidence = length heuristic
        score = len(context)

        return context, score

    except Exception:
        return None, 0