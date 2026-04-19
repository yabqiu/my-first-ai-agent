# My First AI Agent

An AI agent that monitors a cat shelter website and sends Telegram notifications when new cats become available for adoption.

## What it does

- Fetches the adoptable cat list from a shelter website
- Tracks which cats have already been seen (stored in `found_cat_ids.txt`)
- Sends a formatted Telegram message for each newly found cat, including name, sex, breed, age, photo, and a link to the full profile

## Tech stack

- Python 3.13+
- [LangChain](https://github.com/langchain-ai/langchain) — agent framework and tool definitions
- [LangChain AWS](https://github.com/langchain-ai/langchain-aws) — Claude via Amazon Bedrock (`claude-haiku-4-5`)
- [uv](https://github.com/astral-sh/uv) — package and project management
- Telegram Bot API — notifications

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file with your Telegram credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

3. Run the agent:
   ```bash
   uv run python -m my_first_ai_agent.cat_agent
   ```

## Project structure

```
src/my_first_ai_agent/
├── cat_agent.py        # Main agent: task prompt and streaming loop
├── tools.py            # LangChain tools: read_file, write_file, web_fetch
├── telegram.py         # LangChain tool: send_message_to_telegram_bot
└── found_cat_ids.txt   # Persisted list of already-seen cat IDs
```