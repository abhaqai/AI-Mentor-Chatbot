from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
import google.generativeai as genai
from dotenv import load_dotenv
import os


# Load .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY not found in environment variables")

# Configure Google Gemini API
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-pro-latest")


# Streamlit page configuration
st.set_page_config(page_title="AI Mentor Chatbot")
st.title("👨‍🏫AI Mentor")
st.write("Welcome to the AI Mentor chatbot. How can I assist you today?")


# Initialize session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []  # AI Responses

if "past" not in st.session_state:
    st.session_state["past"] = []  # User Inputs

if "entered_prompt" not in st.session_state:
    st.session_state["entered_prompt"] = ""  # Corrected Default Value


# Build chat history messages
def build_message_list():
    messages = ["""
            your name is AI Mentor. You are an AI Technical Expert for Artificial Intelligence, here to guide and assist students with their AI-related questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone.

                1. Greet the user politely ask user name and ask how you can assist them with AI-related queries.
                2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, deep learning, natural language processing, computer vision, and related topics.
                3. you must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
                4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
                5. Be patient and considerate when responding to user queries, and provide clear explanations.
                6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
                7. Do Not generate the long paragarphs in response. Maximum Words should be 100.

                Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always prioritize their learning experience and well-being.
    """]
    
    for human_msg, ai_msg in zip_longest(st.session_state["past"], st.session_state["generated"]):
        if human_msg is not None:
            messages.append(f"User: {human_msg}")
        if ai_msg is not None:
            messages.append(f"AI Mentor: {ai_msg}")
    
    return messages


# AI Response Function
def generate_response():
    message_history = build_message_list()
    try:
        response = model.generate_content("\n".join(message_history))  # Fixed `/n` issue
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"



# User input submit function
def submit():
    st.session_state.entered_prompt = st.session_state.prompt_input
    st.session_state.prompt_input = ""  # Text box correctly clears



# Create text input
st.text_input("You: ", key="prompt_input", on_change=submit, placeholder="Type here...")


# # Generate AI Response
if st.session_state.entered_prompt != "":                  # Empty input check
    user_query = st.session_state.entered_prompt
    st.session_state.past.append(user_query)               # Store user query
    output = generate_response()                           # Get AI Response
    st.session_state.generated.append(output)              # Store AI response


# Display Chat History
if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")


# sidebar
with st.sidebar:
    st.title("👨‍🏫AI Mentor")