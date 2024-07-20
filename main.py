import streamlit as st
import pandas as pd
import uuid

def main():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Please login first.")
        return

    st.title("Welcome, " + st.session_state['username'])

    option = st.radio("Select an option:", ("Create a new chat", "Join an existing chat"))

    if option == "Create a new chat":
        if st.button("Create Chat"):
            chat_id = str(uuid.uuid4())
            st.session_state['chat_id'] = chat_id

            # Read the chat IDs from CSV file
            try:
                chat_ids_df = pd.read_csv("data/chat_ids.csv")
            except FileNotFoundError:
                chat_ids_df = pd.DataFrame(columns=['chat_id', 'user1', 'user2'])

            # Append the new chat ID to the DataFrame with the current user as user1
            new_chat_id = pd.DataFrame({'chat_id': [chat_id], 'user1': [st.session_state['username']], 'user2': [None]})
            chat_ids_df = pd.concat([chat_ids_df, new_chat_id], ignore_index=True)

            # Save the updated DataFrame to the CSV file
            chat_ids_df.to_csv("data/chat_ids.csv", index=False)

            st.success(f"Chat created successfully! Your chat ID is: {chat_id}")
            st.info("Share this chat ID with others to join the chat.")
            st.experimental_rerun()

    elif option == "Join an existing chat":
        chat_id = st.text_input("Enter chat ID")

        if st.button("Join Chat"):
            try:
                chat_ids_df = pd.read_csv("data/chat_ids.csv")
                if chat_id in chat_ids_df['chat_id'].values:
                    chat_row = chat_ids_df.loc[chat_ids_df['chat_id'] == chat_id]
                    if pd.isna(chat_row['user2'].values[0]):
                        # Update the DataFrame with the current user as user2
                        chat_ids_df.loc[chat_ids_df['chat_id'] == chat_id, 'user2'] = st.session_state['username']
                        chat_ids_df.to_csv("data/chat_ids.csv", index=False)
                        st.session_state['chat_id'] = chat_id
                        st.experimental_rerun()
                    else:
                        st.error("Chat is already full. Only two users are allowed per chat.")
                else:
                    st.error("Invalid chat ID.")
            except FileNotFoundError:
                st.error("No chats available. Please create a new chat first.")
