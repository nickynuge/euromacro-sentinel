from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import json

# Load keys
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

system_prompt = """
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
    print("\n[Generating Daily Brief for European hours...]")
    
    # Step 1: Get recent macro/geopolitical developments
    print("[1/3] Searching recent developments...")
    news = web_search("Europe geopolitics macro economy energy ECB euro latest developments")
    
    # Step 2: Get calendar
    print("[2/3] Checking economic calendar...")
    calendar = economic_calendar("Europe economic calendar this week")
    
    # Step 3: Ask the model to synthesize a proper desk brief
    print("[3/3] Synthesizing desk note...\n")
    
    brief_prompt = f"""
You are writing a short, professional Daily Brief for a Flow Macro desk focused on European market hours.

Here is the latest information:

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
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": brief_prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content

# Main conversation loop
conversation = [
    {"role": "system", "content": system_prompt}
]

print("EuroMacro Sentinel – Junior Strategy Analyst")
print("Commands: type any question, or 'brief' for Daily Brief, or 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Session ended.")
        break

    # Special command for Daily Brief
    if user_input.lower() in ["brief", "daily brief", "morning brief"]:
        brief = generate_daily_brief()
        print("\n" + "="*60)
        print(brief)
        print("="*60 + "\n")
        continue

    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation,
        temperature=0.2
    )

    reply = response.choices[0].message.content.strip()

    if '"tool":' in reply:
        try:
            start = reply.find("{")
            end = reply.rfind("}") + 1
            json_str = reply[start:end]
            tool_call = json.loads(json_str)
            
            tool_name = tool_call.get("tool")
            query = tool_call.get("query", "")

            print(f"\n[Using tool: {tool_name} | Query: {query}]")
            tool_results = run_tool(tool_name, query)

            conversation.append({"role": "assistant", "content": reply})
            conversation.append({
                "role": "user",
                "content": f"Here are the tool results:\n\n{tool_results}\n\nNow provide your full analysis. Focus on market implications for European trading hours."
            })

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=conversation,
                temperature=0.3
            )
            reply = response.choices[0].message.content

        except Exception as e:
            reply = f"Error processing tool call: {e}"

    conversation.append({"role": "assistant", "content": reply})

    print("\nAnalyst:")
    print(reply)
    print("\n" + "-"*50 + "\n")