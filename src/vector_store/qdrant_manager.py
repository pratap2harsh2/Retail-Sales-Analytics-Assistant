import streamlit as st
from qdrant_client import QdrantClient


@st.cache_resource
def get_qdrant_client():
    return QdrantClient(
        path="./qdrant_db"
    )