import google.generativeai as genai
from config import Config

if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

def ask_gemini(query, context):
    if not model:
        return "⚠️ API key missing."

    prompt = f"""
You are a medical assistant.

Use context if helpful, otherwise answer normally.

Context:
{context}

Question:
{query}

Answer briefly (2–3 lines).
End with: Consult a doctor if symptoms persist.
"""

    try:
        resp = model.generate_content(prompt)
        return (resp.text or "⚠️ Empty response").strip()

    except Exception as e:
        print("🚨 GEMINI ERROR:", str(e))   # IMPORTANT DEBUG
        return "⚠️ AI service temporarily unavailable."
