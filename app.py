import streamlit as st
from login import login
from chat import chat
import os
import uuid
import tempfile

st.set_page_config(page_title="Chat.io", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    chat()
else:
    login()
