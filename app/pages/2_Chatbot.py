from openai import OpenAI
import streamlit as st
import os
# page config
st.set_page_config(page_title="Plumbot",
                   page_icon=':sparkles:',
                   layout='centered',
                   initial_sidebar_state='expanded')

st.title("Plumbot :robot_face:")
st.subheader("Ask me for my help! Examples include: \n - Write a business proposal for X \n - Proofread the following text \n - Summarise this text \n - Write a risk assessment for X \n Work smart not hard Dad ")

password = st.sidebar.text_input("Niki's password she gave you" )

if password == os.getenv('APP_PASSWORD'):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-0125-preview"

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant who answers questions in a friendly concise way. Your job is to assist Paul at his job as a Project Manager to work efficiently and effectively. Your name is Plumbot."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})