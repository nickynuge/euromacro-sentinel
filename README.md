# EuroMacro Sentinel

An AI-powered research agent that autonomously gathers current macroeconomic and geopolitical information, selects appropriate external tools, synthesises evidence, and generates structured market intelligence focused on European trading hours.

## Motivation

This project was built from scratch as a personal learning project to understand how modern AI agents perform planning, tool use, memory, and iterative reasoning — without relying on high-level orchestration frameworks such as LangChain or CrewAI.

The goal was to go beyond a simple chatbot and build a system that can actively research, decide when external information is needed, and produce trader-relevant analysis.

## Features

- Professional analyst persona focused on European market hours
- Conversation memory across turns
- Web search tool for current geopolitical and macro news (Tavily)
- Economic calendar tool for upcoming data releases and central bank events
- One-command **Daily Brief** generation
- Custom agent loop with tool selection and multi-step reasoning

## How the Agent Works

```text
User Question
      │
      ▼
Agent decides whether tools are required
      │
      ├──► Web Search (geopolitics / news)
      │
      └──► Economic Calendar (data releases / ECB events)
      │
      ▼
Tool results returned
      │
      ▼
Structured analysis generated
      │
      ▼
Conversation memory updated
The agent uses a lightweight custom orchestration loop rather than a pre-built agent framework. This makes the control flow explicit and easier to reason about.
Example: Daily Brief
text> brief

Daily Brief – European Hours

Market Sentiment Overview
Cautiously constructive, with attention on energy policy and geopolitical risk.

Key Developments
• New EU energy market rules coming into force
• Ongoing Russia–Ukraine related risks to energy infrastructure
• Regulatory developments in digital markets

Economic Calendar Highlights
• S&P Global Services PMI Flash
• ECB Consumer Inflation Expectations
• Eurozone Unemployment Rate

Potential Implications
• Energy-related volatility remains a key risk factor
• Data releases may drive short-term EUR and rates moves
• Geopolitical headlines continue to influence risk sentiment
Tech Stack

Python
Groq (Llama 3.3 70B)
Tavily Search API
Custom agent orchestration (no LangChain / CrewAI / AutoGen)

Project Structure
texteuromacro-sentinel/
├── src/
│   └── main.py          # Main agent loop + tools
├── .env                 # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
How to Run

Clone the repository
Create and activate a virtual environment
Install dependencies: pip install -r requirements.txt
Create a .env file with:textGROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
Run: python src/main.py

Usage

Type any research question about geopolitics, macro events, or European markets
Type brief to generate a structured Daily Brief
Type exit to quit

Current Limitations

Relies on the quality of external search results
Does not perform quantitative forecasting or price prediction
Analysis is informational only and should not be considered investment advice
Tool selection and query quality can still be improved

What I Learned

Designed and implemented an iterative tool-calling agent from scratch
Built conversation state / memory management
Engineered prompts for more reliable tool selection
Integrated external APIs into an LLM reasoning loop
Created a lightweight orchestration system without high-level agent frameworks
Turned open-ended research questions into structured market-relevant analysis

Status & Next Steps
Core agent is working. Planned improvements:

Better tool selection and search query quality
Cleaner modular code structure (tools/, prompts/, etc.)
Stronger structured output for analysis
Optional source ranking and event prioritisation
Expanded research capabilities