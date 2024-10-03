import sys
import os
from venv import logger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from IPython.core.display import Markdown
from IPython.core.display_functions import display
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI

from src.chedderbot.agents.zoopAgent import create_zoop_agent
from src.config.guardrail_prompts import self_check_input_prompt, self_check_output_prompt
from src.utils.custom_logger import setup_logger
from src.config.prompts import zoop_agent_prompt
from src.tools.tools import tools




class ChedderBot():
    def __init__(self):
        self.conversation_memory = ConversationBufferWindowMemory(k=3)
        self.logger = setup_logger("ChedderBot")
        self.logger.info("Initializing ChedderBot")
        self.logger.info("Setting up memory")

        self.model = ChatOpenAI(
            temperature=0.4,
            top_p=0.8,
            n=1,
            streaming=True,
            model="gpt-4o-mini",
            max_tokens=256
        )

        self.logger.info(f"Model: {self.model}")

        self.tools = tools
        self.zoop_prompt = zoop_agent_prompt
        self.check_input_prompt = self_check_input_prompt
        self.check_output_prompt = self_check_output_prompt

        self.zoopAgent = create_zoop_agent(self.model, self.tools, self.zoop_prompt)


    def chat(self, user_input):
        # Check user input against guardrails
        logger.info(f"User input: {user_input}")
        if self.self_check_input(user_input):
            self.logger.warning("User input blocked by self-check")
            return {"output": "Your message violates the policy."}

        recent_context = self.conversation_memory.load_memory_variables({})
        context_input = {
            "input": user_input,
            "previous_context": recent_context
        }

        self.logger.info(f"Context input: {context_input}")
        response = self.zoopAgent.invoke(context_input)

        # Check bot response against guardrails
        if self.self_check_output(response.get('output', '')):
            self.logger.warning("Bot response blocked by self-check")
            return {"output": "The bot's response violates the policy."}

        self.logger.info(f"Response: {response}")

        self.conversation_memory.save_context(
            {"input": user_input},
            {"output": response.get('output', 'No output available')}
        )

        return response

    def self_check_input(self, user_input):
        # Prepare the input check prompt
        logger.info(f" - self_check_input - User input: {user_input}")
        input_check = self.check_input_prompt.format(user_input=user_input)
        self.logger.info(f"Input check: {input_check}")
        input_check_result = self.model.invoke(input_check)

        # Check if the result indicates blocking
        self.logger.info(f" - self_check_input - Input check result: {input_check_result}")
        is_blocked = "Yes" in input_check_result.content
        return is_blocked

    def self_check_output(self, bot_response):
        # Prepare the output check prompt
        logger.info(f" - self_check_output - Bot response: {bot_response}")
        output_check = self.check_output_prompt.format(bot_response=bot_response)
        self.logger.info(f" - self_check_output - Output check: {output_check}")
        output_check_result = self.model.invoke(output_check)

        # Check if the result indicates blocking
        self.logger.info(f"Output check result: {output_check_result}")
        is_blocked = "Yes" in output_check_result.content
        return is_blocked

    def reset_memory(self):
        self.conversation_memory.reset_memory()
        self.logger.info("Memory reset")

    def chat_with_display(self, user_input):
        self.logger.info(f"User input: {user_input}")
        response = self.chat(user_input)

        input_query = response.get('input', 'No input provided')
        output_response = response.get('output', 'No output available')

        markdown_output = f"### User: \n\n> {input_query}\n\n### Zoop: \n\n{output_response.strip()}\n"

        return display(Markdown(markdown_output))

