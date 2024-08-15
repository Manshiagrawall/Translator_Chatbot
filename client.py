import requests
import streamlit as st
import pyperclip
from gtts import gTTS

# Function to get Groq response from the backend
def get_groq_response(input_text, language):
    backend_url = "https://serve.herokuapp.com/chain/invoke"
    json_body = {
        "input": {
            "language": language,
            "text": f"{input_text}"
        },
        "config": {},
        "kwargs": {}
    }
    try:
        BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
        response = requests.post(f"{BACKEND_URL}/chain/invoke", json=json_body)
        response.raise_for_status()  # Check if the request was successful
        response_json = response.json()
        output = response_json["output"]
        return output
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return ""

# Set page configuration
st.set_page_config(page_title="LCEL Translation App", page_icon="🌐", layout="wide")

# Custom CSS for improved styling
st.markdown("""
    <style>
    body {
        background-color: #f4f4f4;
        color: #333;
    }
    .stApp {
        max-width: 800px;
        margin: auto;
        padding: 2rem;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTextInput>div>input {
        border: 2px solid #007bff;
        border-radius: 10px;
        padding: 15px;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #007bff;
        color: #fff;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 18px;
        margin-top: 10px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .response-box {
        margin-top: 20px;
        padding: 20px;
        background-color: #f1f1f1;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.title("🌐 LCEL Translation Application")
st.subheader("Convert your text to the selected language using the Gemma model")

# Define language mappings for gTTS
language_mapping = {
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Chinese": "zh"
}

# Language selection
language = st.selectbox("Select the language", list(language_mapping.keys()))

# Text input
input_text = st.text_area("Enter the text you want to translate", height=150)

# Initialize translation history if not present
if 'translation_history' not in st.session_state:
    st.session_state['translation_history'] = []

# Translation action
if st.button("Translate") and input_text:
    with st.spinner("Translating..."):
        translation = get_groq_response(input_text, language)
        if translation:
            st.session_state['translation_history'].append((input_text, translation))
            st.markdown(f"<div class='response-box'><strong>Translation:</strong> {translation}</div>", unsafe_allow_html=True)

            # Copy to Clipboard
            if st.button('Copy to Clipboard'):
                pyperclip.copy(translation)
                st.success("Text copied to clipboard!")

            # Text-to-Speech
            lang_code = language_mapping.get(language, "en")  # Default to English if not found
            tts = gTTS(translation, lang=lang_code)
            tts.save("translation.mp3")
            audio_file = open("translation.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

# Display translation history
if st.session_state['translation_history']:
    st.subheader("Translation History")
    for original, translated in st.session_state['translation_history']:
        st.write(f"**Original:** {original}")
        st.write(f"**Translated:** {translated}")
        st.write("---")
