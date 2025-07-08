import os
import argparse  # Import the argument parsing library
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from query import create_csv_runner # Make sure your file is named chain.py

def main():
    """Demonstrates how to use the self-contained CSV runner chain."""
    load_dotenv()

    # 1. Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Query a CSV file using natural language.")
    parser.add_argument("csv_path", type=str, help="The full path to the CSV file you want to query.")
    args = parser.parse_args()

    # 2. Validate that the provided file path exists
    csv_file_path = args.csv_path
    if not os.path.exists(csv_file_path):
        print(f"Error: The file '{csv_file_path}' was not found.")
        return

    # 3. Initialize the Language Model
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 4. Create the CSV runner, passing the user-provided file path
    csv_runner = create_csv_runner(llm, path=csv_file_path)

    print(f"\n✅ CSV Agent is ready to query '{os.path.basename(csv_file_path)}'.")
    print("   Try asking: 'What was the total revenue?' or 'Which product sold the most units?'")
    print("   Type 'exit' or press Ctrl+C to quit.")

    # 5. Start the interactive loop
    while True:
        try:
            question = input("\n> ")
            if question.lower() == "exit":
                break

            # Invoke the full chain and get the final answer directly
            result = csv_runner.invoke({"question": question})
            print(f"🤖 Answer: {result}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()