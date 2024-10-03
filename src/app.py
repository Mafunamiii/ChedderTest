from dotenv import load_dotenv
import os

from chedderbot.chedder_bot import ChedderBot
from utils.custom_logger import setup_logger

logger = setup_logger("app")

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
