from langchain_tavily import TavilySearch
from langchain.tools import tool    

# @tool
# def general_search(query:str):
#     """Search for general information"""
#     print("General Search tool loaded")

#     return TavilySearch(
#         max_results=5,
#         topic="general"
#     ).run(query)

@tool
def news_search(query:str):
    """Search for news"""
    print("News Search tool loaded")
    return TavilySearch(
        max_results=5,
        topic="news"
    ).run(query)