import re
from src.utils.custom_logger import setup_logger
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = setup_logger("Math Operations")

def evaluate_expression(expression):
    logger.info(f"Evaluating expression: {expression}")
    expression = expression.replace(' ', '')
    while '(' in expression:
        expression = re.sub(r'\(([^()]*)\)', lambda x: str(evaluate_simple_expression(x.group(1))), expression)
    logger.info(f"Expression after parentheses: {expression}")
    expression = re.sub(r'(\d+)\^(\d+)', lambda x: str(float(x.group(1)) ** float(x.group(2))), expression)
    expression = evaluate_mul_div(expression)
    logger.info(f"Expression after multiplication and division: {expression}")
    return evaluate_add_sub(expression)

def evaluate_simple_expression(expression):
    logger.info(f"Evaluating simple expression: {expression}")
    expression = re.sub(r'(\d+)\^(\d+)', lambda x: str(float(x.group(1)) ** float(x.group(2))), expression)
    logger.info(f"Expression after exponentiation: {expression}")
    expression = evaluate_mul_div(expression)
    logger.info(f"Expression after multiplication and division: {expression}")
    return evaluate_add_sub(expression)

def evaluate_mul_div(expression):
    logger.info(f"Evaluating multiplication and division: {expression}")
    while '*' in expression or '/' in expression:
        expression = re.sub(r'(\d+(\.\d+)?)\s*([*/])\s*(\d+(\.\d+)?)', lambda x: str(
            float(x.group(1)) * float(x.group(4)) if x.group(3) == '*' else float(x.group(1)) / float(x.group(4))
        ), expression)
    logger.info(f"Expression after multiplication and division: {expression}")
    return expression

def evaluate_add_sub(expression):
    logger.info(f"Evaluating addition and subtraction: {expression}")
    while '+' in expression or '-' in expression:
        expression = re.sub(r'(\d+(\.\d+)?)\s*([+-])\s*(\d+(\.\d+)?)', lambda x: str(
            float(x.group(1)) + float(x.group(4)) if x.group(3) == '+' else float(x.group(1)) - float(x.group(4))
        ), expression)
    logger.info(f"Expression after addition and subtraction: {expression}")
    return float(expression)

def pemdas_tool(expression: str) -> float:
    logger.info(f"Received expression: {expression}")
    try:
        logger.info("Evaluating expression")
        result = evaluate_expression(expression)
        logger.info(f"Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error evaluating expression: {str(e)}")
        return f"Error evaluating expression: {str(e)}"