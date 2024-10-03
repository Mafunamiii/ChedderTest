import json

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.utils.custom_logger import setup_logger
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = setup_logger("Utilities")

def request_api(url, params=None):
    logger.info(f"Requesting {url}")
    response = requests.get(url, params=params)
    logger.info(f"Response status code: {response.status_code}")
    if response.ok:
        return response.json()
    else:
        logger.error(f"Error: Request failed with status code {response.status_code}")
        raise Exception(f"Error: Request failed with status code {response.status_code}")

def read_json(file_path):
    logger.info(f"Reading JSON from {file_path}")
    with open(file_path, 'r') as file:
        return json.load(file)

def read_csv(file_path):
    logger.info(f"Reading CSV from {file_path}")
    return pd.read_csv(file_path)

def scrape(url):
    logger.info(f"Scraping {url}")
    response = requests.get(url)
    if response.status_code == 200:
        logger.info("Parsing HTML")
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    else:
        logger.error(f"Error: Unable to access {url}, Status Code: {response.status_code}")
        raise Exception(f"Error: Unable to access {url}, Status Code: {response.status_code}")