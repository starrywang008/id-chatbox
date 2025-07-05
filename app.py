import streamlit as st
import openai
import time

st.set_page_config(page_title="Instructional Design Chatbot", page_icon="🎓")
st.title("🎓 Instructional Design Career Coach Chatbot")

# Welcome animation
with st.chat_message("assistant"):
    for word in "Hi there! I'm your AI career coach for Instructional Design. Ask me anything to get started! 💬":
        st.write(word, end="")
        time.sleep(0.02)

# Ask user to input their own API key
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

st.session_state.user_api_key = st.text_input(
    "🔑 Please enter your OpenAI API Key:",
    type="password",
    value=st.session_state.user_api_key
)

if not st.session_state.user_api_key.startswith("sk-"):
    st.warning("Please enter a valid OpenAI API key to continue.")
    st.stop()

openai.api_key = st.session_state.user_api_key

# User role selector
user_role = st.selectbox(
    "🎯 What's your background?",
    ["Beginner", "Teacher transitioning to ID", "Grad student in ID", "Career switcher"]
)

# Inject system prompt based on role
role_prompts = {
    "Beginner": "You are an encouraging ID coach helping absolute beginners understand what Instructional Design is, and how to start from scratch.",
    "Teacher transitioning to ID": "You are helping a classroom teacher understand how their experience translates to ID roles, and what tools and portfolio items to build.",
    "Grad student in ID": "You are advising a graduate student currently studying ID, helping them build experience and prepare for job search.",
    "Career switcher": "You are helping someone from another field learn how to shift into Instructional Design, including what skills to learn and how to reframe past experience."
}

SYSTEM_PROMPT = role_prompts[user_role] + "\nBe practical, structured, and always include tools, learning paths, or action steps."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Common question buttons
st.markdown("**Quick Questions:**")
cols = st.columns(3)
with cols[0]:
    if st.button("What tools should I learn?"):
        st.session_state.messages.append({"role": "user", "content": "What tools should I learn to become an instructional designer?"})
with cols[1]:
    if st.button("How do I build a portfolio?"):
        st.session_state.messages.append({"role": "user", "content": "How do I build a portfolio as an aspiring instructional designer?"})
with cols[2]:
    if st.button("What is ADDIE?"):
        st.session_state.messages.append({"role": "user", "content": "What is the ADDIE model in instructional design?"})

# Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# Generate reply
if len(st.session_state.messages) > 1 and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat
for msg in st.session_state.messages[1:]:  # skip system
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.caption("🔐 Your API key is only used for this session and is not stored or shared.")
