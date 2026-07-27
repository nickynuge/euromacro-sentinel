# EuroMacro Sentinel

An AI-powered research agent designed to support Flow Macro style analysis focused on European market hours.

## What it does

- Monitors geopolitical and macroeconomic developments
- Distills market sentiment
- Connects seemingly unrelated events
- Produces structured analysis and a Daily Brief for European trading hours

## Motivation

This project was built from scratch as a personal learning project to deeply understand LLMs, tool-using agents, and real-time macro/geopolitical analysis — inspired by the Junior Strategy & Operations Analyst (Flow Macro) role.

## Features

- Professional Flow Macro analyst persona
- Conversation memory
- Web search tool (Tavily)
- Economic calendar tool
- One-command Daily Brief generation

## Tech Stack

- Python
- Groq (Llama 3.3 70B)
- Tavily Search
- Custom agent loop with tool calling

## How to run

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Add your API keys to a `.env` file
5. Run: `python src/main.py`

## Status

Active development – core agent is working. Next steps include improved prompting, better tool reliability, and expanded research capabilities.