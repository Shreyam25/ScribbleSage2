import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

import os
import warnings
warnings.filterwarnings("ignore")
import replicate
from replicate.client import Client

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

replicate = Client(api_token=os.getenv("REPLICATE_API_TOKEN"))





st.set_page_config(page_title="ScribbleSage",
                   page_icon="https://i.pinimg.com/564x/7c/a7/2e/7ca72eaaa467e466cff1a24f9b0f8cf9.jpg",
                   layout="centered",
                   initial_sidebar_state="collapsed")


page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://i.pinimg.com/originals/b1/8d/51/b18d5124d08c77a110323493464ff7ae.gif");
#   background-size: 100%;
}
 body {
        text: white;
    }

</style>
"""
st.markdown(page_element, unsafe_allow_html=True)
# Set the title text with custom CSS styling for color
st.markdown(
    f"""
    <h1 style="color:white;font-family: cursive;">ScribbleSage</h1>
    """,
    unsafe_allow_html=True
)


# Apply custom styling using Markdown with HTML and CSS syntax
st.markdown(
    """
    <style>
    ::placeholder { /* Change placeholder color */
      color: white; /* Set the desired color */
      opacity: 1; /* Set opacity to make the text fully visible */
    }
    .stTextInput label { /* Change input label color */
      color: white !important; /* Set the desired color */
      font-family: cursive;
    }
    .stSelectbox label { /* Change select box label color */
      color: white !important; /* Set the desired color */
      font-family: cursive;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input field for entering the blog topic
input_text = st.text_input("Enter Blog Topic", "")

# Create four columns layout
col1, col2, col3, col4 = st.columns([5, 5, 5, 5])

# Input field for number of words
with col1:
    no_words = st.selectbox(label="Blog size",options=
                            ["Short ", "Medium", "Long"],
                            index=0,)




# Select box for audience
with col2:
    blog_style = st.selectbox("Audience",
                              ["Beginners", "Experts", "General", "Young adults", "Professionals", "Parents",
                               "Students", "Seniors"],
                              index=0)

# Select box for tone and style
with col3:
    tone_style = st.selectbox("Tone and Style",
                              ["Formal", "Informal", "Conversational", "Professional", "Humorous", "Educational",
                               "Inspirational", "Technical"],
                              index=0)

# Select box for content structure
with col4:
    content_structure = st.selectbox("Content Structure",
                                     [ "Opinion piece", "Case study", "News update",
                                      "Comparison/Review", "Q&A format","Listicle","How-to guide"],
                                     index=0)

# Preferred language selection
preferred_language = st.selectbox("Preferred Language",
                                 ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean"],index=0)

# Generate button
# Generate button
generate_button = st.button("Generate")

# Check if the button is clicked
if generate_button:
    # Apply custom styling to change the button text color and background color
    st.markdown(
        """
        <style>
        /* Change button text color to black */
        .stButton>button {
            color: black !important;
            background-color: white !important;
            border-color: black !important;
        }

        /* Add animation for background color transition */
        @keyframes goldenTransition {
            0% { background-color: white; }
            100% { background-color: goldenrod; }
        }

        /* Apply animation to the button */
        .stButton>button:hover {
            animation: goldenTransition 0.5s forwards;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Process user input and generate response
    # Add your code to generate the response here
    
 

    # Define template for prompt


    st.markdown(
        """
        <style>
            .stMarkdown{
                color: white;
                font-family: cursive;
                font-size:15px;
            }
            .stMarkdown p:first-of-type{
            font-size:27px;
            font-weight: bold;
            color:#F2DD85
            }
        </style>
        """,
        unsafe_allow_html=True
        )
 
    prompt=PromptTemplate(input_variables=["blog_style", "input_text", "no_words","tone_style","content_structure","preferred_language"],
                            template="Write a {no_words} sized blog for the {blog_style} audience on the topic of {input_text} in a {tone_style} tone, using the {content_structure} format, and in {preferred_language}. Write a beautiful ending to each blog")
    output = replicate.run(
    "meta/llama-2-7b-chat",
    input={
        "debug": False,
        "top_p": 1,
        "prompt": prompt.format(blog_style=blog_style, input_text=input_text,no_words=no_words,content_structure=content_structure,preferred_language=preferred_language,tone_style=tone_style),
        "temperature": 0.75,
        "system_prompt": "You are a helpful, respectful and honest assistan who writes blogs in paragraphs with completes sentences and in a given size and ends blogs with conclusions.",
        "max_new_tokens": 800,
        "min_new_tokens": -1,
        "prompt_template": "[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
        "repetition_penalty": 1
    }
    )
    print(output)
    text = ''.join(output)

# Printing the resulting text
    print(text)
    st.markdown(text)



 

      
 