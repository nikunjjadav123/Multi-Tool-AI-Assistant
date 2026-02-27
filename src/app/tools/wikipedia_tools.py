import wikipedia
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class WikipediaSearchInput(BaseModel):
    query: str = Field(description="Topic to search on Wikipedia")


@tool(args_schema=WikipediaSearchInput)
def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return a short summary."""

    print("\n📚 WIKIPEDIA TOOL EXECUTED\n")

    try:
        # Step 1: Search for relevant titles
        search_results = wikipedia.search(query)

        if not search_results:
            return "No relevant Wikipedia pages found."

        # Step 2: Try top 3 matches safely
        for title in search_results[:3]:
            try:
                page = wikipedia.page(title, auto_suggest=True)
                return wikipedia.summary(page.title, sentences=3)
            except:
                continue

        return "Could not retrieve a valid Wikipedia page."

    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        return "AMBIGUOUS:\n" + "\n".join(options)

    except Exception as e:
        return f"Error retrieving information: {e}"
