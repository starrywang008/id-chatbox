import streamlit as st
from openai import OpenAI

# ✅ Use your own API key for testing (replace with your actual key)
client = OpenAI(api_key="your-api-key-here")  # 你可以先硬编码测试用的 Key

# --- Page setup ---
st.set_page_config(page_title="Smart Learning Assistant", layout="wide")
st.title("📚 Smart Learning Assistant")
st.write("Select your role and ask anything!")

# --- Role selection ---
st.sidebar.title("Choose Your Role")
role = st.sidebar.radio("I am a...", ["Beginner", "Teacher", "Grad Student"])

# --- Quick question buttons ---
st.sidebar.subheader("Quick Questions")

if st.sidebar.button("How can I use AI in my lessons?"):
    st.session_state.messages.append({"role": "user", "content": "How can I use AI in my lessons?"})
    st.session_state.submit_button = True

if st.sidebar.button("What is UDL?"):
    st.session_state.messages.append({"role": "user", "content": "What is UDL?"})
    st.session_state.submit_button = True

if st.sidebar.button("Best tools for online teaching?"):
    st.session_state.messages.append({"role": "user", "content": "Best tools for online teaching?"})
    st.session_state.submit_button = True

# --- AI assistant response for button-triggered questions ---
if st.session_state.get("submit_button", False):
    prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.submit_button = False

# --- Chat history state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Clear Chat Button ---
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []

# --- Display message history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input box ---
user_prompt = st.chat_input("Type your question here...")
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
