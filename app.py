import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load variables from the .env file
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")

# Create the Gemini client
client = genai.Client(api_key=api_key)

# Build the Streamlit page
st.title("🤖 AI Chatbot")

# Get input from the user
user_prompt = st.text_input("Ask me anything:")

# If the user entered something, send it to Gemini
if user_prompt:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
    )

    st.write("### AI_chatbot Response...")
    st.write(response.text)