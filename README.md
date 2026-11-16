# CLI-Driven AI Chat Execution Prototype

A conversational AI application that translates natural-language requests into safe, parameterized CLI executions (`crawler_cli.py`) via Python `subprocess`, captures `stdout`/`stderr`/exit codes, and returns a verified summary alongside structured JSON.

## Architecture
1. **Chat UI (Streamlit):** Captures user prompts and displays execution status, summaries, and JSON.
2. **Intent Layer (Gemini 2.5 Flash Structured Outputs):** Extracts `target_url` and task parameters safely.
3. **Backend Orchestrator (`subprocess.run`):** Executes `crawler_cli.py` with `shell=False`, strict URL validation, and a 15s timeout.
4. **CLI Tool (`crawler_cli.py`):** Fetches the target page, parses DOM elements via BeautifulSoup, and outputs validated JSON to `stdout`.

## Setup & Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run app: `streamlit run app.py`
3. Enter your `GEMINI_API_KEY` in the sidebar and test with:
   `Crawl https://example.com, extract the important information, give me a summary, and return the extracted data in JSON format.`

## AI Tools Disclosure
Built using Python, Streamlit, Google Gemini API (`google-genai`), and AI coding assistance for rapid prototyping.