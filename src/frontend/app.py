import requests
import streamlit as st
import os 
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
print(f"Frontend sending request to Backend URL: {BACKEND_URL}")

st.set_page_config(page_title="Resume Critic", page_icon="📄")

st.markdown(
    """
    <style>
    button[kind="primary"] {
        background-color: #21a366;
        border-color: #21a366;
    }
    button[kind="primary"]:hover {
        background-color: #1c8a56;
        border-color: #1c8a56;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Resume Critic")

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "result" not in st.session_state:
    st.session_state.result = None

uploaded_file = st.file_uploader("Choose your resume", type=["pdf", "docx", "txt"])

if st.button("Upload", disabled=uploaded_file is None):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    try:
        response = requests.post(f"{BACKEND_URL}/upload/", files=files)
        response.raise_for_status()
        st.session_state.uploaded = True
        st.session_state.result = None
    except requests.RequestException as e:
        st.session_state.uploaded = False
        st.error(f"Upload failed: {e}")

if st.session_state.uploaded:
    if st.button("✅ File uploaded successfully, ready for processing", type="primary"):
        with st.spinner("Analyzing resume..."):
            try:
                response = requests.post(f"{BACKEND_URL}/invoke")
                response.raise_for_status()
                st.session_state.result = response.json()
            except requests.RequestException as e:
                st.error(f"Processing failed: {e}")

if st.session_state.result:
    st.subheader("Score")
    st.write(st.session_state.result["score"])

    st.subheader("Missing Keywords")
    for keyword in st.session_state.result["missing_keywords"]:
        st.write(f"- {keyword}")
