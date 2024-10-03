from langchain_core.tools import Tool
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.math_operations import pemdas_tool
from src.utils.utilities import scrape, read_json, request_api

webscrape_tool = Tool(
    name="Web Scrape",
    func=scrape,
    description="Scrape web pages for content"
)

file_read_tool = Tool(
    name="Read JSON File",
    func=read_json,
    description="Read data from a JSON file"
)

requestAPI_tool = Tool(
    name="API Request",
    func=request_api,
    description="Make API requests to specified URLs"
)

pemdas_tool_definition = Tool(
    name="PEMDAS Calculator",
    func=pemdas_tool,
    description="Evaluates mathematical expressions following the PEMDAS order of operations."
)

tools = [webscrape_tool, file_read_tool, requestAPI_tool, pemdas_tool_definition]