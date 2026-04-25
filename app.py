import streamlit as st
import os
import tempfile

from src.pipeline import RAGPipeline
from config import VECTORSTORE_PATH, TOP_K


#----------Helper function ----------------------
def save_uploaded_files(uploaded_files):
    file_paths = []

    for file in uploaded_files:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.write(file.read())
        file_paths.append(temp_file.name)

    return file_paths

st.set_page_config(page_title="RAG Demo", layout="wide")

st.sidebar.title("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF(s)",
    type=["pdf"],
    accept_multiple_files=True,
    key="pdf_uploader"
)

# Load pipeline
@st.cache_resource
def load_pipeline():
    pipeline = RAGPipeline()

    if not os.path.exists(VECTORSTORE_PATH):
        pipeline.build()
    else:
        pipeline.load()

    return pipeline

pipeline = load_pipeline()

# Input
query = st.text_input("Ask a question:")

if st.button("Search") and query:
    answer, results = pipeline.query(query, top_k=TOP_K)
    print("[DEBUG] TOP_K from config:", TOP_K)

    st.subheader("💡 Answer")
    st.write(answer)

    st.subheader("🔍 Sources (Debug View)")

    for i, res in enumerate(results, start=1):
        with st.expander(f"Source {i} | Page {res['page']} | Chunk {res['chunk_index']}"):
            
            # show score if you add later (optional)
            # st.write(f"Score: {res.get('score', 'N/A')}")
            st.markdown("**Preview:**")
            st.write(res["text"][:300] + "...")

            st.markdown("---")
            st.markdown("**Full Chunk:**")
            st.write(res["text"])