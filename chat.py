import streamlit as st
import pandas as pd
import time
from nlp_model import check_for_confidential_info

def display_chat_history(messages):
    for _, message_ in enumerate(messages):
        if message_["role"]!='user':
            with st.chat_message(message_["role"]):
                st.html(f"<span class='chat-{message_['role']}'></span>")
                st.write(message_["message_content"])
        else:
            with st.chat_message(message_["user_id"]):
                st.html(f"<span class='chat-{message_['role']}'></span>")
                st.write(message_["message_content"])
    st.html(
        """
        <style>
            .stChatMessage:has(.chat-assistant) {
                flex-direction: row-reverse;
                text-align: right;
            }
        </style>
        """
    )

def assign_roles(messages):
    for each_message in messages:
        if each_message['user_id'] == st.session_state['username']:
            each_message['role'] = 'assistant'
        else:
            each_message['role'] = 'user'
    return messages

def on_YES_confirmation(user_message):
    messages_df = pd.read_csv("data/messages.csv")
    new_message = pd.DataFrame({'user_id': [st.session_state['username']], 'message_content': [user_message]})
    message_all = pd.concat([messages_df, new_message], ignore_index=True)
    message_all.to_csv("data/messages.csv", index=False)
    del st.session_state.confirm_confidential

def on_NO_confirmation(user_message, response):
    confidential_message = pd.DataFrame({'user_id': [st.session_state['username']], 'message_content': [user_message] , 'model_response': [response]})
    confidential_message_all = pd.read_csv("data/flagged_messages.csv")
    confidential_message_all = pd.concat([confidential_message_all, confidential_message], ignore_index=True)
    confidential_message_all.to_csv("data/flagged_messages.csv", index=False)
    del st.session_state.confirm_confidential

def auto_refresh():
    time.sleep(2)
    st.rerun()

def chat():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please login first.")
        return        

    st.title("Welcome to chat.io")

    st.sidebar.title("User Name")
    st.sidebar.code(st.session_state['username'], language='')

    messages_df = pd.read_csv("data/messages.csv")
    messages_list = messages_df.to_dict('records')
    messages_list = assign_roles(messages_list)
    display_chat_history(messages_list)

    user_message = st.chat_input("Enter your message:")

    if user_message:
        if 'confirm_confidential' not in st.session_state:
                st.session_state['confirm_confidential'] = False

        model_response = check_for_confidential_info(user_message)
        if model_response != 'public':
            if not st.session_state['confirm_confidential']:
                with st.chat_message('assistant'):
                    st.html(f"<span class='chat-assistant'></span>")
                    st.write(user_message)
                st.html(
                    """
                    <style>
                        .stChatMessage:has(.chat-assistant) {
                            flex-direction: row-reverse;
                            text-align: right;
                        }
                    </style>
                    """
                )
                error, yes_button, no_button = st.columns([6, 0.5 , 0.5])
                with error:
                    st.error(f'Your message contains {model_response} information. Do you still want to send it?')
                with yes_button:
                    if st.button("Yes",use_container_width=True,on_click=on_YES_confirmation , args=(user_message,)):
                        print('Button Clicked')
                with no_button:
                    if st.button("No",use_container_width=True,on_click=on_NO_confirmation , args=(user_message,model_response)):
                        print('Button Clicked')
            time.sleep(2)
        else:
            new_message = pd.DataFrame({'user_id': [st.session_state['username']], 'message_content': [user_message]})
            message_all = pd.concat([messages_df, new_message], ignore_index=True)
            message_all.to_csv("data/messages.csv", index=False)
            st.experimental_rerun()
    auto_refresh()
