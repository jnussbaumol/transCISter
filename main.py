from pathlib import Path
from pypdf import PdfReader
from tiktoken import encoding_for_model
from openai import OpenAI
from dotenv import load_dotenv

TOKEN_BUDGET: int = 128_000
SYSTEM_PROMPT: str = """
You are a helpful AI assistant that transforms text that has been OCR'd from a PDF and pull out information on the requirements for a security configuration benchmark.
"""
# MODEL = "gemma-3-27b-it"
MODEL = "gpt-4o"
TEMPERATURE = 0.7


def over_budget(token_count: int) -> bool:
    return token_count > TOKEN_BUDGET


def budget_count(token_count: int) -> int:
    return TOKEN_BUDGET - token_count


def main(pdf: str, local: bool = False) -> None:
    load_dotenv()
    reader: PdfReader = PdfReader(pdf)
    result: str = ""

    encoding = encoding_for_model("gpt-4o")
    total_tokens = 0

    for page in reader.pages:
        contents: str = page.extract_text()
        result += contents
        token_count = len(encoding.encode(contents))
        total_tokens += token_count
        if over_budget(total_tokens):
            print(f"over budget by {budget_count(total_tokens)}")
    print(total_tokens)

    with open("output.txt", "w") as file:
        file.write(result)
    # TODO: extract to factory for external vs lmstudio vs ollama
    if local:
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    else:
        client = OpenAI()
    if not over_budget(total_tokens):
        completions = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": result},
                {"role": "user", "content": "What are all the Level 1s?"},
            ],
            temperature=TEMPERATURE,
        )
        print(completions.choices[0].message.content)
    else:
        print("too big, parse it instead")
        with open("output.txt", "w") as file:
            file.write(result)


if __name__ == "__main__":
    main("CIS_Oracle_MySQL_Enterprise_Edition_8.0_Benchmark_v1.3.0.pdf")
