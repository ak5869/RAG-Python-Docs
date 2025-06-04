import streamlit as st
from rag_query import qa_chain
from db import insert_search, get_all_searches, clear_history
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import io
import speech_recognition as sr
import pyttsx3
import threading

st.set_page_config(page_title="Ask Python Docs", layout="centered")

st.title("Ask Python Docs")
st.markdown("""
An AI-powered assistant that helps you understand Python documentation in plain English.  
Use natural language to ask questions about the Python documentation.  
This app uses Retrieval-Augmented Generation (RAG) powered by Ollama and LangChain.
""")

with st.sidebar:
    st.markdown("## About")
    st.write("""
    This app uses RAG to search Python documentation using Ollama models.

    **Technologies:**
    - Streamlit
    - LangChain
    - Ollama
    - SQLite 
    """)

    model = st.selectbox("Choose Model", ["llama3", "mistral", "phi3"])
    query_depth = st.slider("Query Depth", 1, 5, value=2)

    st.markdown("---")
    st.markdown("## Chat History")

    history = get_all_searches()
    if st.button("Clear All History"):
        clear_history()
        st.success("History cleared.")
        st.experimental_rerun()

    if history:
        search_filter = st.text_input("Filter by keyword", key="sidebar_filter")
        st.markdown("#### Filter by Date Range")
        dates = [datetime.strptime(entry[2], "%Y-%m-%d %H:%M:%S") for entry in history]

        if dates:
            min_date, max_date = min(dates), max(dates)
            date_range = st.date_input(
                "Select date range:",
                (min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date(),
                key="sidebar_date"
            )
            start_date, end_date = date_range if isinstance(date_range, tuple) else (min_date.date(), max_date.date())
        else:
            start_date, end_date = datetime.today().date(), datetime.today().date()

        filtered_history = [
            (q, a, t) for (q, a, t) in history
            if search_filter.lower() in q.lower() and start_date <= datetime.strptime(t, "%Y-%m-%d %H:%M:%S").date() <= end_date
        ] if search_filter or start_date or end_date else history

        if filtered_history:
            for question, answer, timestamp in filtered_history:
                with st.expander(f"{timestamp} — {question}"):
                    st.markdown(answer, unsafe_allow_html=True)
        else:
            st.warning("No matches found.")
    else:
        st.info("No past searches yet.")

st.markdown("---")

query = st.text_input("Type your question or speak:", key="query_input")

if st.button("Speak"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        st.success(f"Recognized: {query}")
        st.session_state["query_input"] = query
    except sr.UnknownValueError:
        st.error("Could not understand audio.")
        query = ""
    except sr.RequestError:
        st.error("Speech recognition service is unavailable.")
        query = ""

if st.button("Search") and query:
    with st.spinner("Thinking..."):
        response = qa_chain.run({
            "query": query,
            "model": model,
            "depth": query_depth
        })

    if isinstance(response, dict):
        response_text = str(response.get("result", response))
    else:
        response_text = str(response)

    insert_search(query, response_text)
    st.session_state["response_text"] = response_text
    st.session_state["current_query"] = query
    st.session_state["read_button_rendered"] = False  # Reset button render flag

if "response_text" in st.session_state:
    st.markdown("### Answer")
    st.markdown(st.session_state["response_text"], unsafe_allow_html=True)

    def speak_text(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    #st.markdown("### 🔊 Audio Tools")
    if not st.session_state.get("read_button_rendered", False):
        if st.button("Read Aloud", key="read_aloud"):
            threading.Thread(target=speak_text, args=(st.session_state["response_text"],)).start()
            st.session_state["read_button_rendered"] = True

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 18)
            self.set_text_color(30, 30, 60)
            self.cell(0, 15, "RAG Q&A Report", ln=True, align="C")
            self.set_draw_color(0, 102, 204)
            self.set_line_width(1)
            self.line(10, 25, 200, 25)
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

        def add_metadata(self):
            self.set_font("Helvetica", "", 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            self.ln(5)

        def add_content(self, question, answer):
            self.set_font("Helvetica", "B", 14)
            self.set_fill_color(220, 230, 241)
            self.set_text_color(0, 51, 102)
            self.cell(0, 12, "Question:", ln=True, fill=True)
            self.set_font("Helvetica", "", 12)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 10, question)
            self.ln(6)

            self.set_font("Helvetica", "B", 14)
            self.set_fill_color(235, 245, 255)
            self.set_text_color(0, 51, 102)
            self.cell(0, 12, "Answer:", ln=True, fill=True)
            self.set_font("Helvetica", "", 12)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 10, answer)
            self.ln(10)

    pdf = PDF()
    pdf.add_page()
    pdf.add_metadata()
    pdf.add_content(st.session_state["current_query"], st.session_state["response_text"])
    pdf_buffer = io.BytesIO(pdf.output(dest='S').encode('latin1'))

    st.download_button(
        label="Download as PDF",
        data=pdf_buffer,
        file_name=f"rag_answer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )
