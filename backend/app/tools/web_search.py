from langchain_core.tools import tool
from typing import List, Dict, Any

@tool
def web_search_tool(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
    """
    Search the web using DuckDuckGo for travel information.

    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 6)

    Returns:
        List of search results with title, url, and snippet
    """
    try:
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r.get("title", ""),
                "url": r.get("href", r.get("link", "")),
                "snippet": r.get("body", r.get("snippet", ""))
            })

        return formatted_results

    except Exception as e:
        return [{
            "title": "Search Error",
            "url": "",
            "snippet": f"Unable to fetch search results: {str(e)}"
        }]
