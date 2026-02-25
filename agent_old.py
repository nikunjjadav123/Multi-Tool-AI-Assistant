import os 
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.weather_tool import get_current_weather
from tools.search_tool import general_search,news_search
from tools.wikipedia_tools import wikipedia_search
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

load_dotenv()


def build_agent(streaming=False):

    llm = ChatGroq(
        model_name=os.getenv("LLM_MODEL"),
        temperature=os.getenv("TEMPERATURE"),
        streaming=streaming,
        callbacks=[StreamingStdOutCallbackHandler()] if streaming else None
    )

    tools = [get_current_weather,general_search,news_search,wikipedia_search] # using hybrid approch of calculator tool means uses the tool directly not via LLM

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools for real-time data like weather."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_agent(
        debug=False,
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
        )

    return agent,llm
