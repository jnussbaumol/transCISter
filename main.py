from pypdf import PdfReader
from tiktoken import encoding_for_model
from openai import OpenAI

TOKEN_BUDGET: int = 4096
SYSTEM_PROMPT: str = """
You are a helpful AI assistant that transforms text that has been OCR'd from a PDF and pull out information on the requirements for a security configuration benchmark.
The user's messages will comprise of the text that is to be analyzed. You are to divide the Recommendations into two categories:

- Level 1
- Level 2

Respond to the user with a list of every Level 1 recommendation, and a second list of every Level 2 recommendation.
"""
MODEL = "gemma-3-27b-it"
TEMPERATURE = 0.7


def over_budget(token_count: int) -> bool:
    return token_count > TOKEN_BUDGET


def budget_count(token_count: int) -> int:
    return TOKEN_BUDGET - token_count


def main(pdf: str, local: bool = True) -> None:
    reader: PdfReader = PdfReader(pdf)
    result: str = ""

    encoding = encoding_for_model("gpt-4o")
    total_tokens = 0

    for page in reader.pages:
        running_tokens = total_tokens
        contents: str = page.extract_text()
        result += contents
        token_count = len(encoding.encode(contents))
        total_tokens += token_count
        if over_budget(total_tokens):
            print(f"over budget by {budget_count(total_tokens)}")
    # with open("output.txt", "w") as file:
    #     file.write(result)
    print(total_tokens)

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
            ],
            temperature=TEMPERATURE,
        )
        print(completions.choices[0].message)
    else:
        print("too big")


if __name__ == "__main__":
    main("CIS_Oracle_MySQL_Enterprise_Edition_8.0_Benchmark_v1.3.0.pdf")
