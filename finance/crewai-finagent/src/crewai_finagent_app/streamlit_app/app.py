import streamlit as st
import time
from utils.fileProcessing import process_pdf
from utils.dashboard import build_dashboard
import os
from dotenv import load_dotenv

load_dotenv()

def applyStylesForTable():
    # Apply Custom CSS
    st.markdown("""
        <style>
            header[data-testid="stHeader"] {
                display: none !important;
            }
            .stMainBlockContainer {
              padding-top: 30px !important; 
            }
            [data-testid='stFileUploaderDropzone'] > [data-testid='baseButton-secondary'] {
                margin-top: 4px;
                margin-bottom: -1px;
                text-indent: -9999px;
                line-height: 0;
            }
            [data-testid='stFileUploaderDropzone'] > [data-testid='baseButton-secondary']::after {
                line-height: initial;
                content: "Browse";
                text-indent: 0;
            }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.markdown("""
        <style>
            header[data-testid="stHeader"] {
                display: none !important;
            }
            .stMainBlockContainer {
              padding-top: 30px !important; 
            }
        </style>
    """, unsafe_allow_html=True)


image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flo_torch_logo.png")
st.image(image_path, width=200)
st.title("Financial Document Analyzer")
st.subheader("FLOTorch RAG analyzes your Bank Statements or Credit Card statements and displays relevant consolidated sections. PDFs only")

def file_uploaded():
    """Callback when file is uploaded."""
    st.session_state["processing_file"] = True

if "processing_file" not in st.session_state:
    st.session_state["processing_file"] = False

uploaded_file = st.file_uploader("", type="pdf", label_visibility='collapsed', disabled=st.session_state.get("processing_file", False), key="file_uploader", on_change=file_uploaded)
st.markdown("""
    <style>
    div[data-testid="stFileUploader"] button[data-testid="stBaseButton-minimal"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)
# Use get() to ensure safe access to session state
uploaded_file_name = st.session_state.get("uploadedFileName", "")
data = st.session_state.get("data", {})
transactions = st.session_state.get("transactions", [])

if uploaded_file:
    # Only set processing to True if a new file is uploaded
    if uploaded_file.name != uploaded_file_name:
        try:
            st.session_state.uploadedFileName = uploaded_file.name  # Update session state
            st.session_state.pdf_buffer = None
            with st.spinner("Processing file... Please wait."):
                time.sleep(2)  # Simulating processing delay
                st.session_state.data, st.session_state.transactions = process_pdf(uploaded_file)
        except Exception as e:
            st.session_state.data = None
            st.session_state.pdf_buffer = None
            st.session_state.transactions = None
            st.session_state.uploadedFileName = ""
            st.error("We couldn't fetch the data. Please try again.")
        finally:
            st.session_state["processing_file"] = False
# Display dashboard only if data is available
if st.session_state.get("data"):
    build_dashboard(st.session_state["data"], st.session_state["transactions"])

