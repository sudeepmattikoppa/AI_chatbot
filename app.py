import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

# -----------------------------
# Create Gemini client
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# Streamlit page title
# -----------------------------
st.title("🤖 AI Chatbot")

# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
user_prompt = st.chat_input("Type your message...")

if user_prompt:

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Build conversation history
    conversation_history = ""

    for message in st.session_state.messages:
        role = message["role"].capitalize()
        conversation_history += f"{role}: {message['content']}\n"

    conversation_history += "Assistant:"

    try:
        # Generate response from Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation_history,
        )

        assistant_reply = response.text

    except Exception as e:
        assistant_reply = f"⚠️ Error: {e}"

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )
    
    
    #streamlit run app.py