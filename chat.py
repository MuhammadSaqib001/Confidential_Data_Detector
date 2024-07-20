import streamlit as st
import pandas as pd
import time
from nlp_model import check_for_confidential_info

def display_chat_history(messages):
    for _, message_ in enumerate(messages):

        with st.chat_message(message_["role"]):
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

def auto_refresh():
    time.sleep(2)
    st.rerun()

def get_name_of_recepient():
    chat_ids = pd.read_csv("data/chat_ids.csv")
    name_1, name_2 = chat_ids[chat_ids['chat_id'] == st.session_state.chat_id]['user1'].to_list()[0],chat_ids[chat_ids['chat_id'] == st.session_state.chat_id]['user2'].to_list()[0]

    if name_1==st.session_state['username']:
        return name_2
    return name_1

def chat():

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please login first.")
        return

    if 'chat_id' not in st.session_state:
        st.error("Please create or join a chat first.")
        return

    chat_id = st.session_state['chat_id']
    st.title("Welcome to chat.io")

    # Add chat ID to the sidebar
    st.sidebar.title("Chat ID")
    st.sidebar.code(chat_id, language='')

    # Add chat ID to the sidebar
    st.sidebar.title("Sender User Name")
    st.sidebar.code(st.session_state['username'] , language='')

    st.sidebar.title("Recipient User Name")
    st.sidebar.code(get_name_of_recepient(), language='')

    messages_df = pd.read_csv("data/messages.csv")
    filtered_messages_df = messages_df.loc[messages_df['chat_id'] == chat_id]
    messages_list = filtered_messages_df.to_dict('records')
    messages_list = assign_roles(messages_list)
    display_chat_history(messages_list)

    user_message = st.chat_input("Enter your message:")

    if user_message:
        if check_for_confidential_info(user_message):
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
            st.error("Your message contains confidential/private information and cannot be sent.")

        else:
            new_message = pd.DataFrame({'chat_id': [chat_id], 'user_id': [st.session_state['username']], 'message_content': [user_message]})
            message_all = pd.concat([messages_df, new_message], ignore_index=True)

            # Save the updated DataFrame to the CSV file
            message_all.to_csv("data/messages.csv", index=False)
    auto_refresh()
