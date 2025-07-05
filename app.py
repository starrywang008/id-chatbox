import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # Or use environment variable

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "role" not in st.session_state:
    st.session_state.role = "Beginner"

# Greeting message
with st.chat_message("assistant"):
    st.markdown("👋 Hi! I'm your Smart Learning Assistant. Select your role below and ask me anything!")

# Sidebar: Role selection
st.sidebar.title("Choose Your Role")
role = st.sidebar.radio("I am a...", ["Beginner", "Teacher", "Grad Student"])
st.session_state.role = role

# Sidebar: Quick question buttons
quick_questions = {
    "Beginner": ["What is instructional design?", "How do I become an ID?", "What's ADDIE?"],
    "Teacher": ["How can I use AI in my lessons?", "What is UDL?", "Best tools for online teaching?"],
    "Grad Student": ["How to pick a thesis topic?", "Tips for academic writing?", "Research methods in EdTech?"]
}

st.sidebar.markdown("### Quick Questions")
for q in quick_questions[role]:
    if st.sidebar.button(q):
        st.session_state.messages.append({"role": "user", "content": q})

# Chat input
user_input = st.chat_input("Type your question here...")

# Handle input and generate assistant response
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a helpful assistant for a {st.session_state.role}."}
                    ] + st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")
