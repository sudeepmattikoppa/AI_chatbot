import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------------------------
# Streamlit Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------
# Load Environment Variables
# ---------------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in your .env file.")
    st.stop()

# ---------------------------------
# Create Gemini Client
# ---------------------------------
client = genai.Client(api_key=api_key)

# ---------------------------------
# Initialize Chat History
# ---------------------------------
if "messages" not in st.session_state:
    try:
        with open("chat_history.json", "r") as file:
            st.session_state.messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.messages = []

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.write("Built by Sudeep")

    st.markdown("---")

    st.info(
        "This chatbot uses Google Gemini and "
        "stores conversation history locally."
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

        with open("chat_history.json", "w") as file:
            json.dump([], file)

        st.rerun()

# ---------------------------------
# Main Page
# ---------------------------------
st.title("🤖 AI Chatbot")
st.caption("Powered by Gemini • Built with Streamlit")

# ---------------------------------
# Display Previous Messages
# ---------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------
# Chat Input
# ---------------------------------
user_prompt = st.chat_input("Type your message...")

if user_prompt:

    # Display user message
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

    # Generate response
    try:
        with st.spinner("🤔 Gemini is thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=conversation_history,
            )

            assistant_reply = response.text

    except Exception as e:
        assistant_reply = f"⚠️ Error: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    # Save chat history to file
    with open("chat_history.json", "w") as file:
        json.dump(st.session_state.messages, file, indent=4)

    #streamlit run app.py