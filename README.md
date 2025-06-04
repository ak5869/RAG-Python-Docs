#  Ask Python Docs – AI-Powered Python Documentation Assistant

An AI-powered assistant that answers your questions about Python documentation in plain English using **Retrieval-Augmented Generation (RAG)**.

![Screenshot](https://github.com/user-attachments/assets/a1e9eac8-8f99-4e18-8fa3-77838f989e86)

![Screenshot](https://github.com/user-attachments/assets/d817a44d-1321-41a3-861d-cf0a365d64fd)


---

##  Features

-  Ask natural language questions about Python
-  Searches official Python docs using RAG
-  Powered by LangChain and Ollama models (LLaMA 3, Mistral, Phi3)
-  Voice input using microphone
-  Read answers aloud (text-to-speech)
-  Download Q&A as PDF
-  Full search history with date filtering
-  Built-in SQLite database for storing searches

---

##  Technologies

- **Frontend:** Streamlit
- **Backend:** LangChain, Python
- **Models:** Ollama (LLaMA 3, Mistral, Phi3)
- **Database:** SQLite
- **Voice:** SpeechRecognition + pyttsx3
- **PDF Export:** fpdf

---

##  Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/RAG-Python-Docs.git
   cd RAG-Python-Docs
   ```
2. Create a virtual environment:
  ```bash
  python -m venv rag_env
  source rag_env/bin/activate  # on Windows: rag_env\Scripts\activate
  ```
3. Install requirements:
  ```bash
  pip install -r requirements.txt
  ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```
