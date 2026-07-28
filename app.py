import streamlit as st
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import json

# Load API keys
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# System prompt
SYSTEM_PROMPT = """
You are a Junior Strategy and Operations Analyst on a real-time Flow Macro desk focused on European market hours.

Your core responsibilities:
- Distill market sentiment from geopolitical and economic events
- Connect seemingly unrelated events and explain possible market implications
- Think like a trader who wants to monetize market-moving information
- Be concise, structured, and clear

You have access to two tools:

1. web_search
   {
     "tool": "web_search",
     "query": "your search query"
   }

2. economic_calendar
   {
     "tool": "economic_calendar",
     "query": "Europe economic calendar this week"
   }

When you need a tool, respond with ONLY the JSON object.
After receiving tool results, provide structured analysis focused on European market implications.
"""

def web_search(query: str) -> str:
    try:
        response = tavily.search(query=query, search_depth="basic", max_results=6)
        results = response.get("results", [])
        if not results:
            return "No relevant results found."
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"{i}. {r.get('title')}\n   {r.get('content')}\n   Source: {r.get('url')}")
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Search error: {str(e)}"

def economic_calendar(query: str) -> str:
    try:
        calendar_query = f"{query} economic calendar data releases ECB CPI PMI"
        response = tavily.search(query=calendar_query, search_depth="basic", max_results=6)
        results = response.get("results", [])
        if not results:
            return "No calendar information found."
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"{i}. {r.get('title')}\n   {r.get('content')}\n   Source: {r.get('url')}")
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Calendar search error: {str(e)}"

def run_tool(tool_name: str, query: str) -> str:
    if tool_name == "web_search":
        return web_search(query)
    elif tool_name == "economic_calendar":
        return economic_calendar(query)
    return "Unknown tool."

def generate_daily_brief():
    news = web_search("Europe geopolitics macro economy energy ECB euro latest developments")
    calendar = economic_calendar("Europe economic calendar this week")

    brief_prompt = f"""
You are writing a short, professional Daily Brief for a Flow Macro desk focused on European market hours.

=== RECENT DEVELOPMENTS ===
{news}

=== ECONOMIC CALENDAR ===
{calendar}

Write a clean Daily Brief with these sections:
1. Market Sentiment Overview
2. Key Developments to Watch
3. Economic Calendar Highlights
4. Potential Trade Implications / Risks

Keep it concise, structured, and trader-focused.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": brief_prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# ---------- Streamlit UI ----------

st.set_page_config(page_title="EuroMacro Sentinel", page_icon="📊", layout="centered")

st.title("EuroMacro Sentinel")
st.caption("Flow Macro research agent for European market hours")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display previous messages (skip the system prompt)
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about geopolitics, macro events, or type 'brief'..."):
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Handle Daily Brief command
    if prompt.lower().strip() in ["brief", "daily brief", "morning brief"]:
        with st.chat_message("assistant"):
            with st.spinner("Generating Daily Brief..."):
                brief = generate_daily_brief()
                st.markdown(brief)
        st.session_state.messages.append({"role": "assistant", "content": brief})
    
    else:
        # Normal agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # First call
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    temperature=0.2
                )
                reply = response.choices[0].message.content.strip()

                # Check for tool use
                if '"tool":' in reply:
                    try:
                        start = reply.find("{")
                        end = reply.rfind("}") + 1
                        tool_call = json.loads(reply[start:end])
                        tool_name = tool_call.get("tool")
                        query = tool_call.get("query", "")

                        st.caption(f"Using tool: `{tool_name}` | Query: `{query}`")

                        tool_results = run_tool(tool_name, query)

                        st.session_state.messages.append({"role": "assistant", "content": reply})
                        st.session_state.messages.append({
                            "role": "user",
                            "content": f"Here are the tool results:\n\n{tool_results}\n\nNow provide your full analysis. Focus on market implications for European trading hours."
                        })

                        # Second call with tool results
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=st.session_state.messages,
                            temperature=0.3
                        )
                        reply = response.choices[0].message.content
                    except Exception as e:
                        reply = f"Error using tool: {e}"

                st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})