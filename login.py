import streamlit as st
import pandas as pd


def login():
    st.title("Login Page")

    # Read user credentials from CSV
    username = st.text_input("Username")

    if st.button("Join the Chat"):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.experimental_rerun()
