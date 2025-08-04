# Agentic AI System

This project is a full agentic AI system that uses Google's Gemini LLM and integrated tools to break down and execute multi-step tasks. It supports mathematical calculations, translations, and direct question answering in an interactive CLI environment.

## Features

- **Task Breakdown:** Automatically decomposes complex user requests into actionable steps.
- **Tool Integration:** Supports calculation, translation (German and other languages), and direct answering.
- **Interactive CLI:** User-friendly command-line interface with colored output.
- **Logging:** Logs all interactions and errors for debugging and traceability.

## Requirements

- Python 3.8+
- [Google Generative AI SDK](https://github.com/google/generative-ai-python)
- `colorama`
- `python-dotenv`
- Gemini API key

## Setup

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd AIBOT
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key:**
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your-gemini-api-key-here
     ```

## Usage

Run the agent in interactive mode:

```
python full_agent.py
```

### Example Inputs

- `Translate 'Good Morning' into German and then multiply 5 and 6.`
- `Add 10 and 20, then translate 'Have a nice day' into German.`
- `Tell me the capital of Italy, then multiply 12 and 12.`
- `Add 2 and 2 and multiply 3 and 3.`
- `What is the distance between Earth and Mars?`

Type `help` in the CLI for more examples.

## File Structure

- `full_agent.py` - Main agent logic and CLI
- `calculator_tool.py` - Calculation tool
- `translator_tool.py` - Translation tool
- `.env` - Environment variables (not tracked in version control)
- `agent.log` - Log file (generated at runtime)

## License

MIT License

## Acknowledgements

- Google Generative AI
- Colorama
- Python Dotenv

