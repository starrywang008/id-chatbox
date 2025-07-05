# app.py

import streamlit as st
import openai

# 页面设置
st.set_page_config(page_title="ID学习资源专家", page_icon="🎓")
st.title("🎓 Instructional Design 学习资源专家 Chatbot")

# 设置 OpenAI API 密钥（部署时通过 .streamlit/secrets.toml 注入）
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 系统角色 prompt（定义 GPT 的角色和回答风格）
SYSTEM_PROMPT = """
你是一位经验丰富的 Instructional Designer 和职业导师，你的任务是帮助用户了解：
- Instructional Design 所需的核心技能和知识
- 常用工具与平台（如 Articulate Rise, Storyline, Canva 等）
- 如何准备作品集与简历
- 不同背景转行 ID 的路径与建议（如老师、学生、设计师等）
- 推荐学习资源（理论、课程、模板）
请根据用户的背景和提问来个性化回答，用清晰结构和实际行动建议帮助他们继续学习。
"""

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 用户输入区域
user_input = st.chat_input("请输入你的问题（例如：我是老师，想转ID，需要从哪学起？）")

# 处理输入并调用 API
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("生成回答中..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

# 显示对话记录
for msg in st.session_state.messages[1:]:  # 不显示 system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
