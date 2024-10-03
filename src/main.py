from dotenv import load_dotenv
import os
import streamlit as st
from chedderbot.chedder_bot import ChedderBot
from utils.custom_logger import setup_logger

if __name__ == "__main__":

    logger = setup_logger("Main")

    logger.info("Starting ChedderBot")
    try:
        logger.info("Loading environment variables")
        load_dotenv()
        logger.info("Loaded environment variables")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        logger.info("API Key loaded")
    except Exception as e:
        logger.error(f"Error loading environment variables: {str(e)}")
        raise Exception(f"Error loading environment variables: {str(e)}")

    logger.info("Initializing ChedderBot")
    chedder_bot = ChedderBot()
    logger.info("ChedderBot initialized")
    chedder_bot.chat("Hello")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.title("Chedder!")

    def handle_input():
        logger.info("Handling user input")
        user_input = st.session_state.user_input
        logger.info(f"User input: {user_input}")
        bot_response = chedder_bot.chat(user_input)
        logger.info(f"Bot response: {bot_response}")
        bot_output = bot_response.get('output', 'No response available')
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": bot_output})

        st.session_state.user_input = ""

    st.text_input("You: ", key="user_input", on_change=handle_input)

    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Chedder:** {msg['content']}")

            st.markdown("---")