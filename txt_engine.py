from config import Config

def load_txt():
    try:
        with open(Config.TXT_PATH, "r", encoding="utf-8") as f:
            return f.read().lower()
    except:
        return ""

text_data = load_txt()

def search_txt(query):
    if query.lower() in text_data:
        return "Relevant medical information found.", 1
    return None, 0