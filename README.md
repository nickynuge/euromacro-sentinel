# EuroMacro Sentinel

An AI-powered research agent focused on European macro and geopolitical developments.

It monitors events, distills market sentiment, connects seemingly unrelated developments, and produces structured analysis relevant to European trading hours.

## Motivation

This project was built from scratch as a personal learning project to deeply understand large language models, tool-using agents, and real-time macro/geopolitical analysis. The goal was to go beyond simple chatbots and build something that can actively gather information, reason over it, and produce trader-relevant insight.

## Features

- Professional analyst persona focused on European market hours
- Conversation memory
- Web search tool for current geopolitical and macro news
- Economic calendar tool for upcoming data releases and central bank events
- One-command **Daily Brief** generation
- Custom agent loop with tool selection and multi-step reasoning

## Tech Stack

- Python
- Groq (Llama 3.3 70B)
- Tavily Search API
- Custom agent orchestration (no heavy frameworks)

## Project Structure

```text
euromacro-sentinel/
├── src/
│   └── main.py          # Main agent loop
├── .env                 # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md

## How to Run

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Create a .env file with your API keys:
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
5. Run the agent
python src/main.py

## Usage

Type any question about geopolitics, macro events, or European markets
Type brief to generate a structured Daily Brief
Type exit to quit

## Status

Core agent is working. Current focus areas for improvement:

Better tool selection and query quality
Stronger structured output for analysis
Expanded research capabilities
Cleaner modular code structure

## What I Learned

How to build a tool-using agent from scratch
Prompt design for reliable tool calling
Managing conversation memory
Integrating external search into an LLM workflow
Turning open-ended research questions into structured market-relevant analysis