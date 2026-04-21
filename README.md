MedChat Streamlit is a Python application that connects patients and healthcare professionals through a secure, responsive chat interface. It pairs a Streamlit frontend with a Flask-style backend and a three-layer fallback system (CSV → TXT → Gemini) orchestrated by a RAG engine to provide reliable, context-aware responses.

Repository Layout
Code
medchat-streamlit/
├── app.py                 # Main Streamlit frontend
├── config.py              # Configuration settings
├── csv_engine.py          # CSV data layer
├── txt_engine.py          # TXT data layer
├── gemini_engine.py       # Gemini AI layer
├── rag_engine.py          # RAG orchestration and fallback logic
├── requirements.txt       # Project dependencies
├── data/
│   ├── medical.csv        # Structured medical data (CSV Layer)
│   └── medical.txt        # Unstructured medical documents (TXT Layer)
├── vectorstore/           # Vector embeddings storage (for TXT/Gemini)
└── .streamlit/            # Streamlit configuration
Features
Three-layer fallback system: CSV → TXT → Gemini (AI) with RAG orchestration.

Real-time messaging: Streamlit UI with WebSocket-style updates (if implemented).

User authentication: Configurable via config.py.

Persistent chat history.

Search: Structured lookups (CSV) and full-text search (TXT) with vector embeddings for semantic search.

Extensible architecture: Separate engines for CSV, TXT, and Gemini layers and a central RAG orchestrator.

Installation
Prerequisites
Python 3.8 or later

pip (Python package manager)

Steps
Clone the repository

bash
git clone https://github.com/Abhyam007/medchat-streamlit.git
cd medchat-streamlit
Install dependencies

bash
pip install -r requirements.txt
Set environment variables (if using Gemini or other external APIs)

bash
export GOOGLE_API_KEY="your_gemini_api_key"
# export OTHER_API_KEY="value"   # add other keys as needed
Prepare data and vectorstore (see Data Preparation below).

Configuration
Edit config.py to customize:

API keys and endpoints (Gemini or other LLM providers)

Layer confidence thresholds and fallback behavior

Paths for data/ and vectorstore/

Authentication settings and database connection strings

Example config.py entries:

py
# config.py (example)
DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore"
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
CSV_CONFIDENCE_THRESHOLD = 0.85
TXT_CONFIDENCE_THRESHOLD = 0.7
Quick Start / Usage
Start backend services (if you have a separate backend)

bash
python backend/app.py
Run the Streamlit frontend

bash
streamlit run app.py
Open the app

Code
http://localhost:8501
Interact

Log in or create an account (if authentication is enabled).

Enter medical queries in the chat UI.

The system will route queries through CSV → TXT → Gemini layers automatically and return synthesized responses.

Data Preparation
CSV Layer Guidelines
Use consistent column names and types.

Include an id column for deterministic lookups.

Place CSV files in data/ (e.g., data/medical.csv).

Example data/medical.csv

csv
id,term,type,dosage,notes
1,Drug X,antihypertensive,50 mg once daily,Adjust for renal impairment
2,Drug Y,antibiotic,500 mg twice daily,Take with food
TXT Layer Guidelines
Store clinical notes and documents as plain text files in data/ (e.g., data/medical.txt).

Use a consistent filename convention and maintain a small metadata index (JSON or SQLite) linking documents to patient IDs, visit dates, and tags.

Preprocess text (tokenization, normalization) if you build a custom index.

Example data/medical.txt

Code
2025-04-01 | Patient A | Hypertension follow-up
Patient reports improved BP control on Drug X. Continue current dose. Monitor renal function.
Vectorstore / Embeddings
Use vectorstore/ to persist embeddings for semantic search (TXT layer).

Provide an ingestion script (e.g., scripts/ingest.py) to:

Read CSV and TXT files

Create or update vector embeddings for TXT documents

Populate any search indices used by csv_engine.py and txt_engine.py

Engines and Orchestration
csv_engine.py: Implements deterministic lookups and fuzzy matching on CSV datasets. Returns results with confidence scores and source references.

txt_engine.py: Implements full-text and semantic search over TXT documents using vector embeddings. Returns ranked snippets and confidence scores.

gemini_engine.py: Wraps calls to the configured LLM (Gemini or equivalent) to synthesize multi-source results, paraphrase, and generate user-facing explanations.

rag_engine.py: Orchestrates the fallback flow:

Query CSV layer → if confident, return.

Else query TXT layer → if confident, return.

Else call Gemini to synthesize CSV + TXT context and produce final response.

Each step returns a confidence score used by rag_engine.py to decide escalation and combination strategies.

Usage Examples
Example 1 — Dosage Lookup

User: "What is the recommended dose for Drug X?"

Flow: csv_engine.py finds a match in data/medical.csv → returns dosage and source reference.

Example 2 — Document Search

User: "Find information about hypertension management"

Flow: txt_engine.py performs semantic search over data/medical.txt and vectorstore → returns ranked snippets and references.

Example 3 — Synthesis

User: "Combine guidance on drug interactions with clinical notes"

Flow: rag_engine.py collects CSV and TXT results and calls gemini_engine.py to synthesize a cohesive explanation with confidence scoring.

Development & Contributing
Fork the repository.

Create a feature branch:

bash
git checkout -b feature/your-feature
Implement changes and add tests where applicable.

Commit and push:

bash
git commit -am "Add feature description"
git push origin feature/your-feature
Open a Pull Request with a clear description of changes.

Coding style: follow PEP8 and include docstrings for public functions. Add unit tests for new logic in engines and RAG orchestration.

Security and Privacy
Data Minimization: Store only the minimum required patient data.

Transport Security: Use TLS for all network traffic in production.

Encryption: Encrypt sensitive data at rest when deploying.

Access Control: Enforce authentication and role-based access.

Audit Logging: Log access and changes to sensitive records for compliance.

Disclaimer: The AI layer provides informational assistance only and is not a substitute for professional medical advice. Always consult a qualified healthcare professional for diagnosis and treatment.

License
This project is released under the MIT License. See the LICENSE file for details.

Contact
For questions or contributions:

Open an issue on the GitHub repository: https://github.com/Abhyam007/medchat-streamlit

Maintainer: Abhyam007
