# This app was adapted from: https://github.com/zhaojj1014/PubMed_Pal
# Original author: @zhaojj1014
# Licensed under the MIT License
# Modified for interactive learning assistant use in instructional design.

import streamlit as st
import openai
from openai import OpenAI

# Function to get OpenAI response
def get_completion(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
    )
    return response.choices[0].message["content"]

# Sidebar Configuration
st.sidebar.title("📚 Smart ID Career Coach")

st.sidebar.write('''🎓 Welcome!

This is a prototype learning assistant designed to help you explore careers in instructional design (ID). Whether you're just starting out, switching careers, or already in EdTech, this tool is here to support you.

💡 You can ask questions like:
- What skills do I need to become an instructional designer?
- How do I build an ID portfolio?
- What are the common tools used in corporate learning?

*This is an early prototype—expect bugs and surprises!*''')

st.sidebar.divider()

api_key = st.sidebar.text_input(
    "Enter your OpenAI API key:",
    type="password",
    placeholder="Paste your OpenAI API key here (sk-...)",
    help="You can get your API key from https://platform.openai.com/account/api-keys."
)

st.sidebar.divider()

if api_key:
    client = OpenAI(api_key=api_key)

    st.header("🎯 ID Career Coach – Your Background")

    # Collect user input
    education = st.text_input("What is your education background?", placeholder="e.g., Master's in Educational Technology")
    experience = st.text_input("What work experience do you have?", placeholder="e.g., 2 years teaching + 3-month ID internship")

    tools = st.multiselect(
        "Which tools have you used? (Select all that apply)",
        ["Articulate Rise", "Storyline", "Figma", "Canva", "ChatGPT", "Moodle", "Canvas", "Brightspace"],
        placeholder="Choose the tools you're familiar with"
    )

    other_tools = st.text_input("Any other tools or skills you'd like to mention?", placeholder="e.g., Notion, Trello, GitHub")

    target_sector = st.selectbox(
        "Which industry are you aiming for as an ID?",
        ["Higher Education", "Corporate", "K-12", "Nonprofit", "Not sure yet"]
    )

    job_descriptions = st.text_area(
        "Paste 2–3 job descriptions for your dream ID roles:",
        placeholder="Copy from LinkedIn or Indeed and paste here..."
    )

    generate_button = st.button("📌 Generate Career Suggestions")

    if generate_button:
        with st.spinner("Analyzing your background and generating a career development plan..."):
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert career coach specialized in helping international students break into the instructional design (ID) industry in North America. Your style is clear, supportive, and structured. You provide tailored roadmaps based on users’ current background and career goals. You avoid generic advice and instead give realistic, specific, and action-oriented suggestions."
                },
                {
                    "role": "user",
                    "content": f"""
The user is aiming for a career in **{target_sector} instructional design.

📄 **Job Descriptions**:
```{job_descriptions}```

🙋‍♀️ **User's Background**:
- 🎓 Education: {education}
- 💼 Work experience: {experience}
- 🧰 Tools used: {tools}
- 🧠 Other skills: {other_tools}

🎯 **Your Tasks**:
1. 🔍 **Summary**: Briefly describe the user's current position and potential.
2. 🧭 **Gap Analysis**: Compare the user’s profile with the job descriptions above. What are the gaps in skills, tools, and experience?
3. 🚀 **Action Plan**: Give a clear 3–6 month roadmap to become job-ready, including tool suggestions, portfolio ideas, content creation tips, and networking steps.

Format using clear sections, bullet points, and simple language. Speak directly to the user (use “you”).
"""
                }
            ]

            response = get_completion(messages)

            st.success("Career Report Generated!")
            st.markdown("### 📘 Your Instructional Design Career Roadmap")
            st.markdown(response)

else:
    st.text("Please enter your OpenAI API key to proceed.")
