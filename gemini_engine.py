import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(query, context):
    prompt = f"""
You are a medical assistant.

STRICT RULES:
- Use ONLY the given context
- Be medically accurate
- Answer in 2–3 lines
-if get bye then end with byee
- No hallucination
- If unsure say "I don't know"
- End with: Consult a doctor if symptoms persist

Context:
{context}

Question:
{query}

Answer:
"""
    try:
        resp = model.generate_content(prompt)
        return (resp.text or "").strip()
    except:
        return " server unavailable. Try again."