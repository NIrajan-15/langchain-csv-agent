# prompt.py
"""Defines the prompt template for the CSV query chain."""

from langchain_core.prompts.prompt import PromptTemplate

_PROMPT_TEMPLATE = """You are a DuckDB expert. Given a user question, first create a syntactically correct DuckDB SQL query to run, then look at the results of the query and return the answer.

Unless the user specifies in the question a specific number of examples to obtain, do not limit your query.

You can only query the table named 'data'. This table represents the data from the user's CSV file.

{table_info}

Pay attention to use only the column names you can see in the table description. Do not query for columns that do not exist.

Write the SQL query that answers the following question:
Question: {input}"""

PROMPT = PromptTemplate.from_template(_PROMPT_TEMPLATE)