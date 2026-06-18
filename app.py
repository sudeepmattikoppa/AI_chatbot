import streamlit as st

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 My First AI Chatbot")

name = st.text_input("What's your name?")

if name:
    st.success(f"Hello, {name}! Welcome to your chatbot project.")