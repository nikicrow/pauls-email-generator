from openai import OpenAI
import streamlit as st
import os

# function to get response from model
def getresponse(input_text,no_words):
    client = OpenAI()
    
    # Prompt template
    template = f"""
                Act as a professional and senior project manager.
                You will be given an email or an email chain in the below text.
                Your task is to summarise it. Be succinct and accurate.
                Try and use dot points where possible.
                Don't make anything up.
                [EMAIL INPUT START]
                ```
                {input_text} 
                ```
                [EMAIL INPUT END]
                Be polite and concise and use a maximum of {no_words}
                """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": template},
            {"role": "user", "content": "Can you summarise these emails?"}
        ]
    )
    print(response)

    return response

# page config
st.set_page_config(page_title="Email summariser",
                   page_icon=':email:',
                   layout='centered',
                   initial_sidebar_state='expanded')

st.header("Paul's personal email assistant")

# input from user
password = st.sidebar.text_input("Niki's password she gave you" )
input_text=st.text_area("Paste the contents of the email(s) you would like to summarise", height=10)
no_words = 500

submit = st.button("Summarise email")

if password != st.secrets['APP_PASSWORD']:
    st.warning('Check password', icon="⚠️")
elif submit and password == st.secrets['APP_PASSWORD']: 
    with st.status('Summarising your email...', expanded=True) as status:
        email_response = getresponse(input_text,no_words)
        st.header('Your response')
        st.write(email_response.choices[0].message.content)
        