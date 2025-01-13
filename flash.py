import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import json
from langchain_core.prompts import PromptTemplate
from youtube_search import YoutubeSearch

# Load environment variables
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

chat_session = model.start_chat(history=[])

# Function to process button click
def generate_course(sub_input, time):
    if not sub_input or time <= 0:
        st.error("Please enter valid subject and time.")
        return

    # Send the prompt to Generative AI model
    response = chat_session.send_message(f"""
    You are a great course designer. Now design a specific course to learn {sub_input} in {time} to {time + 2} hours.
    Include all topics from beginner level to advanced level. Write your output in only JSON format and no extra text.

    example of output:
    {{
      "course_title": "",
      "description": "",
      "required_time": "",
      "modules": [
        {{
          "module_title": "",
          "elapsed_time": "",
          "topics": [
              "",
              "",
              "",
              "",
              ...
          ]
        }},
        {{
          "module_title": "",
          "elapsed_time": "",
          "topics": [
              "",
              "",
              "",
              "",
              ...
          ]
        }},
        ...
      ],
      "prerequisites": "",
    }}
    """)

    # Parse response to JSON
    try:
        res = json.loads(response.text[8:-5])  # Assuming `response` is a valid JSON string
    except Exception as e:
        st.error(f"Failed to parse the response: {e}")
        return

    # Add YouTube links for each module
    for module in res["modules"]:
        search_term = module["module_title"]
        results = YoutubeSearch(search_term, max_results=10).to_dict()
        module['ytlink'] = f"https://youtu.be/{results[0]['id']}" if results else "No link available"

    # Generate Markdown
    markdown = f"# {res['course_title']}\n\n"
    markdown += f"**Description:** {res['description']}\n\n"
    markdown += "## Prerequisites\n\n"
    markdown += f"{res['prerequisites']}\n\n"
    markdown += "## Modules\n\n"
    markdown += "| Module Titles |Elapsed time | Topics | YouTube Link |\n"
    markdown += "|---------------|-------------|--------|--------------|\n"
    

    for module in res["modules"]:
        topics = "<br>".join(module["topics"])
        ytlink = module.get("ytlink", "No link available")
        markdown += f"| {module['module_title']} |{module['elapsed_time']}| {topics} | [Watch here]({ytlink}) |\n"

    # Display Markdown
    st.markdown(markdown,unsafe_allow_html=True)  

# Streamlit UI
# st.title("Roadmap generator ")

# sub_input = st.text_input("Enter the name of subject:", placeholder = 'Generate a roadmap for...')
# time = st.number_input("Enter the time in hours:",min_value=5, step=1)

st.title("Roadmap Generator")
st.write("Generate a detailed learning roadmap for any subject!")

sub_input = st.text_input("Enter the subject name:", placeholder="E.g., Data Science, Web Development")
time = st.number_input("Enter the time in hours:", min_value=5, step=1)


if st.button("Generate"):
    generate_course(sub_input, int(time))

st.write(""" <hr> 
        <Style>
         body{
        color: white;
        
         }
         a{
         color: white;
         text-decoration: none;
         }
         hr{
        left:0;
         bottom:0;
         }
        </style>
         """, unsafe_allow_html=True)
st.write("""Created with ❤️ by <a href = "https://github.com/gpsworld">gpsworld</a>""", unsafe_allow_html=True)
st.write("""Created with ❤️ by <a href = "https://github.com/gpsworld">gpsworld</a>""", unsafe_allow_html=True)
