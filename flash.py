
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
# from transformers import pipeline
from langchain_core.prompts import PromptTemplate


load_dotenv()
genai.configure(api_key=os.environ["api_key"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def butt():
    response = chat_session.send_message(f"""You are a great course designer. Now desgin a specific course to learn the {sub_input} in the {time} to {time+2} hours. Include all topics from beginner level to advanced level. Write your output in tabular format.  """)
    st.markdown(response.text)


sub_input = st.text_input("Enter the name of subject: ")
time = int(st.number_input("Enter the time in hours:"))
st.button("Generate", on_click=butt)

# response = chat_session.send_message(f"""You are a great course designer. Now desgin a specific course to learn the {sub_input} in the {time} to {time+2} hours. Include all topics from beginner level to advanced level. Write your output in tabular format.  """)

# st.markdown(response.text)
