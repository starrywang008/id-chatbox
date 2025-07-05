# This app was adapted from: https://github.com/zhaojj1014/PubMed_Pal
# Original author: @zhaojj1014
# Licensed under the MIT License
# Modified for interactive learning assistant use in instructional design.

import streamlit as st
from openai import OpenAI

# ========== Sidebar: Welcome & API Input ==========
st.sidebar.title("📚 Smart ID Career Coach")

st.sidebar.markdown('''
### 🎓 Welcome!

This is a prototype learning assistant designed to help you explore careers in instructional design (ID). Whether you're just starting out, switching careers, or already in EdTech, this tool is here to support you with quick and smart answers.

💡 You can ask questions like:
- What skills do I need to become an instructional designer?
- How do I build an ID portfolio?
- What are common tools used in corporate learning?
---

*This is an early prototype—expect bugs and surprises!*
''')

# Sidebar: Select role
role = st.sidebar.radio(
    "🎭 Select Your Role",
    ("Beginner", "Teacher", "Grad Student"),
    help="Choose the role that best describes you. This will customize the assistant’s tone and advice."
)

# Temporary API key for testing – you can replace this with your own or user input
api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=api_key)


# ========== Session State Initialization ==========
# Define system message based on role
if role == "Beginner":
    system_prompt = (
        "You are a helpful career coach who explains the basics of instructional design to someone with no prior knowledge. "
        "Be encouraging, patient, and use simple language."
    )
elif role == "Teacher":
    system_prompt = (
        "You are an expert in helping K-12 or higher-ed teachers transition into instructional design roles. "
        "Focus on identifying transferable skills and giving actionable steps toward building a portfolio and switching careers."
    )
elif role == "Grad Student":
    system_prompt = (
        "You are a career mentor for graduate students studying instructional design. "
        "Offer advice on gaining real-world experience, building a strong portfolio, and navigating the job market."
    )

# Initialize chat history
if st.session_state.get("current_role") != role:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
    st.session_state.current_role = role


# ========== Main Chat Interface ==========
st.title("🧠 ID Learning Chatbox")

user_input = st.chat_input("Ask me anything about learning design or ID careers...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== Display Message History ==========
for msg in st.session_state.messages[1:]:  # Skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
