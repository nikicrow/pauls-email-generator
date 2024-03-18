from openai import OpenAI
import streamlit as st
import os

# function to get response from model
def getresponse(input_text,response_summary,no_words):
    client = OpenAI()
    
    # Prompt template
    template = f"""
                Act as a professional and senior project manager.
                You will be given an email in the below text. Your text is to create an appropriate and professional response.
                Remember to start with Dear 'name of person you are responding to' and sign off with 'Regards,'
                [EMAIL INPUT START]
                ```
                {input_text} 
                ```
                [EMAIL INPUT END]
                Use the below response summary to give you an idea on what to say.
                Be polite, professional and concise.
                [RESPONSE SUMMARY START]
                ```
                {response_summary}
                ```
                [RESPONSE SUMMARY END]
                Write the email in less than {no_words}
                """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": template},
            {"role": "user", "content": "Can you generate a good email response?"}
        ]
    )
    print(response)

    return response

# page config
st.set_page_config(page_title="Email generator",
                   page_icon=':email:',
                   layout='centered',
                   initial_sidebar_state='expanded')

st.header("Paul's personal email assistant")

# input from user
password = st.sidebar.text_input("Niki's password she gave you" )
input_text=st.text_area("Paste the contents of the email(s) you would like me to respond to", height=10)
response_summary=st.text_area("Enter a brief summary of the response you want me to write (e.g. no worries)", height=5)
no_words = st.text_input('Maximum number of words for the email you want me to write')

submit = st.button("Generate response")

if password != st.secrets['APP_PASSWORD']:
    st.warning('Check password', icon="⚠️")
elif submit and password == st.secrets['APP_PASSWORD']: 
    with st.status('Writing your email...', expanded=True) as status:
        email_response = getresponse(input_text,response_summary,no_words)
        st.header('Your response')
        st.write(email_response.choices[0].message.content)
        