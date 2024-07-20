import streamlit as st
from login import login
from main import main
from chat import chat

st.set_page_config(page_title="Chat.io", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    if 'chat_id' in st.session_state:
        chat()
    else:
        main()
else:
    login()
