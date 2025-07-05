import streamlit as st
import time
from openai import OpenAI

# Get user's API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Initialize OpenAI client
if api_key:
    client = OpenAI(api_key=api_key)

    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show welcome animation
    with st.chat_message("assistant"):
        placeholder = st.empty()
        welcome_text = "Hi there! I'm your AI career coach for Instructional Design."
        animated_text = ""
        for char in welcome_text:
            animated_text += char
            placeholder.markdown(animated_text)
            time.sleep(0.02)

    # User input
    user_input = st.chat_input("Type your question here...")

    if user_input:
        # Display user message
        st.chat_message("user").markdown(user_input)

        # Append to history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                ai_reply = response.choices[0].message.content
                st.markdown(ai_reply)

        # Append AI response to history
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
