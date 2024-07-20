import streamlit as st
import pandas as pd

def check_credentials(username, password, users_df):
    if username in users_df['username'].values:
        if password == users_df[users_df['username'] == username]['password'].values[0]:
            return True
    return False

def login():
    st.title("Login")

    # Read user credentials from CSV
    users_df = pd.read_csv("data/user_credentials.csv")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_credentials(username, password, users_df):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")
