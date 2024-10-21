# Confidential Data Detector

## Overview

The **Confidential Data Detector** is a Streamlit application that enables users to create and join chat sessions securely. Users can generate unique chat IDs and share them with others to facilitate private conversations. The application maintains a record of active chats in a CSV file, ensuring that only two users can participate in each chat.

## Features

- **User Authentication**: Ensures users are logged in before they can create or join chats.
- **Create New Chat**: Generate a unique chat ID for a new conversation and share it with others.
- **Join Existing Chat**: Join a chat by entering an existing chat ID.
- **CSV Storage**: Stores chat IDs and associated users in a CSV file for persistence.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Streamlit
- Pandas
