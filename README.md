# MedChat Streamlit

## Project Overview
MedChat Streamlit is designed to provide an interactive platform for users to communicate with AI in a medical context. The system implements a 3-layer fallback modes system to ensure information retrieval is efficient and reliable.

## 3-Layer Fallback Modes System
The system employs the following layers:

1. **CSV Layer:**
   - Description: Utilizes data stored in CSV format for quick access and retrieval. Ideal for simple queries where structured data is already in place.
   - Use Cases: Basic information requests where detailed computational analysis is not required.

2. **TXT Layer:**
   - Description: This layer processes unstructured text data, allowing for more complex queries that may not have a direct CSV representation.
   - Use Cases: Situations where the information is embedded in free text, requiring natural language processing.

3. **Gemini Layer:**
   - Description: The advanced layer that integrates both CSV and TXT data, providing a holistic approach to query resolution. Utilizes AI to interpret and present the information cohesively.
   - Use Cases: Comprehensive inquiries that necessitate data from multiple formats and require contextual understanding.

## Features
- Interactive UI built with Streamlit for responsiveness.
- Robust AI algorithms for accurate information retrieval.
- Seamless integration with multiple data formats (CSV, TXT, Gemini).

## Architecture
- The architecture is designed to be modular, allowing for easy upgrades and maintenance across the different layers of data processing. 
- Each layer is independently maintainable but interconnected through a unified query processing interface.

## Installation
To set up the project, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/Abhyam007/medchat-streamlit.git
   ```
2. Change the directory:
   ```bash
   cd medchat-streamlit
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Instructions
After installation, run the Streamlit app using the following command:
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your web browser to access the application.