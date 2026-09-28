import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


# Load local .env when running on your computer
load_dotenv()


# Try local environment first
API_KEY = os.getenv("GROQ_API_KEY")


# If running on Streamlit Cloud,
# get the key from Streamlit Secrets
if not API_KEY:

    try:
        API_KEY = st.secrets["GROQ_API_KEY"]

    except Exception:
        API_KEY = None


# Make sure the key exists
if not API_KEY:

    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to .env locally or Streamlit Secrets when deployed."
    )


# Groq OpenAI-compatible client
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def ask_groq(question):

    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=question
    )

    return response.output_text