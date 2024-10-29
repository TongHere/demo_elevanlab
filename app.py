import os
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()

# Configure page settings at the very beginning
st.set_page_config(
    page_title="Single-Shot Prompt",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def generate_gpt_response(prompt):
    try:
        llm = ChatOpenAI(model='gpt-4', temperature=0.7)
        
        prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template="{prompt}"
        )
        
        chain = LLMChain(llm=llm, prompt=prompt_template)
        
        response = chain.run(prompt=prompt)
        return response
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

def main():
    # Initialize session state for the prompt if it doesn't exist
    if 'prompt' not in st.session_state:
        st.session_state.prompt = "Write a short email."

    # Custom CSS for styling
    st.markdown("""
        <style>
        .reportview-container .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        .stButton > button {
            color: white;
            background-color: red;
            border-color: red;
        }
        .stButton > button:hover {
            color: white;
            background-color: darkred;
            border-color: darkred;
        }
        .element-container iframe {
            border: none !important;
            min-height: 600px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add ElevenLabs ConvAI widget with proper styling and configuration
    elevenlabs_widget = """
        <div style="margin: 20px 0; padding: 10px; border-radius: 10px;">
            <elevenlabs-convai agent-id="f2rYWbsoInaOzCea6BTu"></elevenlabs-convai><script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
        </div>
    """



    components.html(elevenlabs_widget, height=650, scrolling=True)

    # Small input box for the prompt
    prompt = st.text_input("Please click Run.", 
                          value=st.session_state.prompt,
                          placeholder="Write an short email.")

    # Update session state when the prompt changes
    if prompt != st.session_state.prompt:
        st.session_state.prompt = prompt

    # Run button
    if st.button("Run"):
        if st.session_state.prompt:
            with st.spinner("Generating response..."):
                response = generate_gpt_response(st.session_state.prompt)
                if response:
                    st.write(response)
        else:
            st.warning("Please enter a prompt before running.")

if __name__ == '__main__':
    main()