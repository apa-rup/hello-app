


import streamlit as st
import pandas as pd
import os

from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI

st.write("hello")

template = """
    The following depicts a friendly conversation between a human and an AI. 
    You are from particular Country, therefore please try to articulate according to the Country.
    The AI, being talkative, asks several relevant questions based on the ongoing discussion.
    It aims to learn more about the daily activities of the user.
    If unfamiliar with the topic of conversation, the AI honestly admits its lack of knowledge.
    The AI exclusively utilizes information from the conversation to formulate questions that facilitate continued dialogue. 
    Moreover, don't mention that you are an AI-generated system. Behave like a normal human.
    

    
    Here are some examples example questions those could be used to continue the conversion

    - How do you usually start your day?
    - Do you have any morning routines that you stick to?
    - What does a typical workday look like for you?
    
    - How do you commute to your workplace?
    - What are some of the challenges you face in your daily routine?

    - Do you usually cook at home or eat out?
    - Do you have any bedtime practice that help you sleep better?

    - What type of movies you like most?
    - How do you usually spend your weekends?
    

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please go ahead with your conversion, and discussion should move forward not stick to the same topic so long.
    
    Below is the dialoge, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    user_text: {usertext}
    COUNTRY: {country}
    
    YOUR {dialect} RESPONSE:

    Please go ahead with your conversion, and discussion should move forward not stick to the same topic more than two or three turn.
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "country","usertext"],
    template=template,
)

# Define the model and parameters
# model_name = 'gpt-4'
temperature = 0.8
max_tokens = 2000

# Create a function to generate responses
def generate_response(prompt):
    # Use the OpenAI API to generate responses
    response = client.chat.completions.create( # Use create() method
        model= 'gpt-4',
        messages=[{"role": "user", "content": prompt}], # Pass prompt as messages
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content # Extract content from message






st.set_page_config(page_title="Daily Diaries", page_icon=":robot:")
st.header("Daily Diary")

col1, col2 = st.columns(2)



with col1:
    st.markdown("This is an AI-generated project designed to interact like a human. This will mostly discuss daily life topics, \
                 such as work-life balance, food habits, cultural practices, or anything special you want to share. It will not ask you anything very personal or intimidating \
                 but will focus on your day-to-day routine. \n\n  This tool will interact with you for mostly 5 to 8 minutes. \
                 Sometimes it will ask something predefined or sometimes it will ask you based on a recent conversation.\
                 Enjoy! This tool is powered by LLM, [LangChain](https://langchain.com/) and [OpenAI](https://openai.com).")
                 


with col2:
    st.image(image='U-M_Logo-Hex.png', width=250, caption='https://umich.edu/')

st.markdown("###### We typically response in few minutes. :tada: ")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

# openai_api_key = get_api_key()

os.environ['OPENAI_API_KEY'] = get_api_key()
client = OpenAI()
OpenAI.api_key = os.environ['OPENAI_API_KEY']


col1, col2, col3 = st.columns(3)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your conversation to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))
    

with col3:
    option_country = st.selectbox(
        'Select your country',
        ('India', 'Germany','Singaore','Italy','USA'))
    

def get_text():
    input_text = st.text_area(label="User Input", label_visibility='collapsed', placeholder="User Input...", key="user_input")
    return input_text

user_input = get_text()

if len(user_input.split(" ")) < 6:
    st.write("Please enter a longer text. The minimum length is 6 words.")
    st.stop()



st.markdown("##### System generated response:")

if user_input:


    response = generate_response(prompt.format(tone=option_tone, dialect=option_dialect,country=option_country ,usertext=user_input)) # Format the prompt
    
    st.write(response)
