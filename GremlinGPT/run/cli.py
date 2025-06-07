#!/usr/bin/env python3

# CLI entrypoint to talk to the GremlinGPT NLP engine
import readline
import sys
import os

# --- Dynamic project root ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from nlp_engine.parser import parse_nlp
from loguru import logger
from backend.api.chat_handler import chat
import nltk

# --- NLTK Data Config (Always Available) ---
NLTK_DATA_DIR = os.path.expanduser('~/nltk_data')
nltk.data.path.append(NLTK_DATA_DIR)

def ensure_nltk_resources():
    resources = [
        ("punkt", "tokenizers/punkt"),
        ("averaged_perceptron_tagger", "taggers/averaged_perceptron_tagger"),
        ("wordnet", "corpora/wordnet"),
        ("stopwords", "corpora/stopwords"),
    ]
    for pkg, res_path in resources:
        try:
            nltk.data.find(res_path)
        except LookupError:
            nltk.download(pkg, download_dir=NLTK_DATA_DIR)

# Ensure resources only if missing (fast startup)
ensure_nltk_resources()

BANNER = """
🌩️  GremlinGPT Terminal v1.0.3 [NLP-Only Mode]
Type your command. Type 'exit' to leave.
"""

def main():
    print(BANNER)
    while True:
        try:
            user_input = input("👤 > ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("GremlinGPT going dark.")
                break

            logger.info(f"[CLI] Received input: {user_input}")
            result = parse_nlp(user_input)

            print("\n🧠 NLP Engine Output:")
            print(f"- Intent route: {result['route']}")
            print(f"- Tokens: {result['tokens']}")
            print(f"- POS tags: {result['pos'][:5]}...")  # show sample
            print(f"- Entities: {result['entities']}")
            print(f"- Financial terms: {result['financial_hits']}")
            print(f"- Code structures: {result['code_entities']}")

            # Call GremlinGPT's chat handler
            response = chat(user_input)
            print("🤖 GremlinGPT:", response.get("message", "[No response]"))

            print("-" * 40)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Shutting down.")
            break
        except Exception as e:
            logger.error(f"[CLI] Error during input handling: {e}")

if __name__ == "__main__":
    main()
