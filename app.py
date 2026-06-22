import os
import json
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
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
# Gemini Client
# ---------------------------------
client = genai.Client(api_key=api_key)

# ---------------------------------
# System Prompt
# ---------------------------------
SYSTEM_PROMPT = """
You are an expert AI assistant.

Rules:
- Give beginner-friendly explanations.
- Use Markdown formatting.
- Use uploaded PDF content whenever relevant.
- If the answer exists in the uploaded PDF, answer from it.
- If it does not exist in the PDF, say so and answer normally.
"""

# ---------------------------------
# Initialize chat history
# ---------------------------------
if "messages" not in st.session_state:
    try:
        with open("chat_history.json", "r") as file:
            st.session_state.messages = json.load(file)
    except:
        st.session_state.messages = []

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:

    st.title("🤖 AI Chatbot")
    st.write("Built by Sudeep")

    st.markdown("---")

    st.info(
        "This chatbot uses Google Gemini and stores conversation history locally."
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        if "pdf_text" in st.session_state:
            del st.session_state["pdf_text"]

        with open("chat_history.json", "w") as file:
            json.dump([], file)

        st.rerun()

    uploaded_file = st.file_uploader(
        "📄 Upload a PDF",
        type=["pdf"],
        key="pdf_upload"
    )

    if uploaded_file is not None:

        pdf_reader = PdfReader(uploaded_file)

        pdf_text = ""

        for page in pdf_reader.pages:
            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

        # IMPORTANT: Save PDF text
        st.session_state.pdf_text = pdf_text

        st.success("✅ PDF uploaded successfully!")

# ---------------------------------
# Main Page
# ---------------------------------
st.title("🤖 AI Chatbot")
st.caption("Powered by Gemini • Built with Streamlit")

# ---------------------------------
# Display chat history
# ---------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------
# Chat Input
# ---------------------------------
user_prompt = st.chat_input("Type your message...")

if user_prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # ---------------------------------
    # Build prompt
    # ---------------------------------

    conversation_history = SYSTEM_PROMPT + "\n\n"

    # Inject PDF if uploaded
    if "pdf_text" in st.session_state:

        conversation_history += (
            "The user uploaded the following PDF.\n"
            "Use it as the primary source when answering.\n\n"
        )

        conversation_history += st.session_state.pdf_text + "\n\n"

    # Add previous messages
    for msg in st.session_state.messages:

        role = msg["role"].capitalize()

        conversation_history += (
            f"{role}: {msg['content']}\n"
        )

    conversation_history += "Assistant:"

    # ---------------------------------
    # Generate streaming response
    # ---------------------------------

    assistant_reply = ""

    try:

        with st.chat_message("assistant"):

            placeholder = st.empty()

            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=conversation_history,
            ):

                if chunk.text:
                    assistant_reply += chunk.text
                    placeholder.markdown(assistant_reply + "▌")

            placeholder.markdown(assistant_reply)

    except Exception as e:

        assistant_reply = f"⚠️ {e}"

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    # Save chat locally
    with open("chat_history.json", "w") as file:
        json.dump(
            st.session_state.messages,
            file,
            indent=4
        )

    #streamlit run app.py