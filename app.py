import streamlit as st
import openai

st.set_page_config(page_title="Instructional Design Expert Chatbot", page_icon="🎓")
st.title("🎓 Instructional Design Career Coach Chatbot")

# Ask user to input their own API key
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

st.session_state.user_api_key = st.text_input(
    "🔑 Please enter your OpenAI API Key to continue:", 
    type="password", 
    value=st.session_state.user_api_key
)

# Check if key is valid
if not st.session_state.user_api_key.startswith("sk-"):
    st.warning("Please enter a valid OpenAI API key to start chatting.")
    st.stop()

# Set API key
openai.api_key = st.session_state.user_api_key

# Set system role: Instructional Design Expert
SYSTEM_PROMPT = """
You are an experienced Instructional Designer and career mentor. Your role is to help users:

- Understand the core skills and knowledge required to become an Instructional Designer (ID)
- Recommend tools and platforms (e.g., Articulate Rise, Storyline, Canva, LMS, etc.)
- Provide actionable advice for creating a portfolio and resume
- Suggest learning paths based on user background (e.g., teachers, students, career changers)
- Share relevant learning resources (theories, templates, courses)

Please tailor your answers based on user background and questions. Be clear, encouraging, and structured.
"""

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Input box for user messages
user_input = st.chat_input("💬 Ask your question about Instructional Design...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Generating response..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat history
for msg in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Safety footer
st.caption("🔐 Your API key is only used for this session and is not stored or shared.")
