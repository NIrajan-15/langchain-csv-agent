# query.py
"""Contains the function for creating the self-contained CSV runner chain."""

from __future__ import annotations
from operator import itemgetter
import re

from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough, RunnableLambda
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine

from prompt import PROMPT

# --- Internal Helper Functions ---

def _extract_sql_from_markdown(sql_string: str) -> str:
    """Extracts a SQL query from within a markdown code block."""
    match = re.search(r"```(?:sql\n)?(.*?)```", sql_string, re.DOTALL)
    if match:
        return match.group(1).strip()
    return sql_string.strip()

def _execute_query_safely(db: SQLDatabase, query: str) -> str:
    """Executes a SQL query and returns the result or an error message."""
    try:
        return db.run(query)
    except Exception as e:
        return f"Error: The following query failed to execute:\n{query}\n\nError details: {e}"

def _create_query_generation_chain(
    llm: BaseLanguageModel,
    db: SQLDatabase,
) -> Runnable:
    """Creates a low-level chain for generating SQL queries from a question."""
    table_info = db.get_table_info(table_names=['data'])
    inputs = {"input": RunnablePassthrough(), "table_info": lambda _: table_info}
    return inputs | PROMPT | llm | StrOutputParser()


# --- Public-Facing Factory Function ---

def create_csv_runner(
    llm: BaseLanguageModel,
    path: str,
) -> Runnable:
    """
    Creates a self-contained, high-level chain that can answer questions about a CSV file.

    This function handles all database setup internally. The user only needs to provide
    an LLM and the path to the CSV file.

    Args:
        llm: The language model to use.
        path: The file path to the CSV file.

    Returns:
        A runnable chain that takes a dictionary with a "question" key and returns a
        natural language answer.
    
    Example:
        .. code-block:: python

            from langchain_openai import ChatOpenAI
            from chain import create_csv_runner

            llm = ChatOpenAI(model="gpt-4o")
            csv_runner = create_csv_runner(llm, path="sales.csv")
            result = csv_runner.invoke({"question": "what was the total revenue?"})
            print(result)
    """
    # 1. Handle all database setup internally
    engine = create_engine(f"duckdb:///:memory:")
    db = SQLDatabase(engine)
    
    # 2. Use DuckDB's ability to query a file directly and create a VIEW.
    # A VIEW is a virtual table that makes it easier for the LLM to query.
    db.run(f"CREATE OR REPLACE VIEW data AS SELECT * FROM read_csv_auto('{path}')")
    
    # 3. Create the necessary chains
    query_generation_chain = _create_query_generation_chain(llm, db)

    answer_prompt = PromptTemplate.from_template(
        """Given the user's question, the corresponding SQL query, and the SQL result, formulate a final natural language answer. If the SQL Result contains an error message, explain the error to the user in a helpful way.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer:"""
    )

    # 4. Assemble the final, self-contained chain
    runner = (
        RunnablePassthrough.assign(
            query=query_generation_chain | RunnableLambda(_extract_sql_from_markdown)
        )
        .assign(result=lambda x: _execute_query_safely(db, x["query"]))
        | answer_prompt
        | llm
        | StrOutputParser()
    )
    
    return runner