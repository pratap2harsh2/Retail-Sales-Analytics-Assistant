import streamlit as st
import cohere

co = cohere.Client(
    st.secrets["COHERE_API_KEY"]
)