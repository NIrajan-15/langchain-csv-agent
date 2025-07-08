# LangChain CSV Query Engine

## Overview
LangChain CSV Query Engine is an AI-powered tool designed to interact with CSV files using natural language. It can:

- **Translate Natural Language**: Convert plain English questions into precise SQL queries.
- **Query CSV Data**: Use the DuckDB engine to execute these SQL queries directly on a local CSV file.
- **Synthesize Answers**: Provide final answers in plain English, not just raw data tables.

## Features

### Natural Language Interface:
- Ask complex questions about your data, including filtering, aggregation, and grouping.
- Understands the context of your CSV's columns to generate accurate queries.

### Data Engine:
- Uses DuckDB for high-performance, in-memory SQL execution.
- No need for a separate database server; all processing is done locally.

### Intelligent & Safe:
- The self-contained chain automatically handles the entire workflow from question to answer.
- Gracefully handles errors from invalid SQL queries and provides helpful feedback.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd <repository-name>
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Usage

Run the main program from your terminal, providing the path to your CSV file as an argument:

```bash
python main.py "path/to/your/data.csv"
```

Follow the prompts to ask questions about your data:

```plaintext
✅ CSV Agent is ready to query 'your_data.csv'.
   Type 'exit' or press Ctrl+C to quit.

> What is the average price for laptops?
```

## Configuration

Environment variables can be set in the `.env` file. Create this file in the root of the project. For example:

```plaintext
OPENAI_API_KEY="your-openai-api-key"
```

## Requirements

- Python 3.9 or higher
- Poetry for dependency management

