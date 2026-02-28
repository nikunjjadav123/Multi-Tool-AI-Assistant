import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from app.tools.weather_tool import get_current_weather
from app.tools.wikipedia_tools import wikipedia_search
from app.tools.search_tool import news_search
from app.tools.calculator_tool import calculator
from app.tools.date_time_tool import get_current_datetime
from app.utils.extract_expression import is_math, extract_expression
from app.utils.date_time_expression import is_datetime_query
from app.prompts import CALCULATOR_PROMPT
from langchain_groq import ChatGroq
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from app.memory.mongo_memory import get_mongo_checkpointer
from langchain_core.messages import BaseMessage
from app.utils.date_time_expression import extract_location

from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model_name=os.getenv("LLM_MODEL"),
    temperature=os.getenv("TEMPERATURE"),
    streaming=False,
    callbacks=[StreamingStdOutCallbackHandler()],
)


# -------------------------
# State
# -------------------------


class AgentState(TypedDict):
    history: List[BaseMessage]
    user_input: str
    result: str


# -------------------------
# Router Node
# -------------------------


def router(state: AgentState):
    query = state["user_input"].lower()
    # Personal / conversational questions

    if any(word in query for word in ["my name", "who am i", "what is my name"]):
        return "chat_node"
    if "weather" in query:
        return "weather_node"
    if any(word in query for word in ["news", "latest", "recent", "headline"]):
        return "news_node"
    if is_datetime_query(query):
        return "datetime_node"
    if is_math(query):
        return "math_node"

    return "wiki_node"


def chat_node(state: AgentState):
    history = state.get("history", [])

    history.append({"role": "user", "content": state["user_input"]})

    response = llm.invoke(history)

    history.append({"role": "assistant", "content": response.content})

    return {"history": history, "result": response.content}


# -------------------------
# Tool Nodes
# -------------------------


def weather_node(state: AgentState):
    print("Weather Node Executing...")

    extract = llm.invoke(
        f"Extract only the city name from this sentence: {state['user_input']}. "
    )

    city = extract.content.strip()
    raw_weather = get_current_weather.invoke({"city": city})

    formatted = llm.invoke(
        f"""
    Convert the following weather data into ONE short single-line weather report.

    Return ONLY the sentence.
    Do NOT add quotes.
    Do NOT add extra commentary

    Weather Data:
    {raw_weather}
    """
    )

    return {"result": formatted.content}


def datetime_node(state: AgentState):
    location = extract_location(state["user_input"])
    result = get_current_datetime.invoke({"location": location})

    formatted = llm.invoke(
        f"""
        Convert the following datetime data into ONE short single-line date-time report.

        Return ONLY the sentence.
        Do NOT add quotes.
        Do NOT add extra commentary

        User Input: {state["user_input"]}
        Result: {result}
    """
    )
    return {"result": formatted.content}


def wiki_node(state: AgentState):
    result = wikipedia_search.invoke({"query": state["user_input"]})
    return {"result": result}


def news_node(state: AgentState):
    result = news_search.invoke({"query": state["user_input"], "topic": "news"})

    articles = result.get("results", [])

    if not articles:
        return {"result": "No recent news found."}

    formatted = []

    for article in articles[:3]:
        formatted.append(
            f"📰 {article.get('title','No title')}\n" f"🔗 {article.get('url','')}"
        )

    return {"result": "\n\n".join(formatted)}


def math_node(state: AgentState):
    expr = extract_expression(state["user_input"])
    if not expr:
        return {"result": "Sorry, I could not understand the math expression."}
    raw_result = calculator.invoke({"expression": expr})

    prompt_text = CALCULATOR_PROMPT.format(expr=expr, result=str(raw_result))

    formatted = llm.invoke(prompt_text)
    return {"result": formatted.content}


# -------------------------
# Build Graph
# -------------------------

builder = StateGraph(AgentState)

builder.add_node("weather_node", weather_node)
builder.add_node("wiki_node", wiki_node)
builder.add_node("news_node", news_node)
builder.add_node("math_node", math_node)
builder.add_node("chat_node", chat_node)
builder.add_node("datetime_node", datetime_node)

builder.set_conditional_entry_point(router)

builder.add_edge("weather_node", END)
builder.add_edge("wiki_node", END)
builder.add_edge("news_node", END)
builder.add_edge("math_node", END)
builder.add_edge("chat_node", END)
builder.add_edge("datetime_node", END)

checkpointer = get_mongo_checkpointer()

graph = builder.compile(checkpointer=checkpointer)

# -------------------------
# Run Function
# -------------------------


def run_agent(user_input: str):
    result = graph.invoke(
        {"user_input": user_input}, config={"configurable": {"thread_id": "user_1"}}
    )
    return result["result"]
