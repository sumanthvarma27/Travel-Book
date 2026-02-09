"""
Search utility functions for web search across agents.
Provides unified interface for DuckDuckGo search with error handling and rate limiting.
"""

from typing import List, Dict, Any
import logging
import time
import random

logger = logging.getLogger(__name__)

# Rate limiting: track last search time
_last_search_time = 0.0
_MIN_DELAY = 2.0  # Minimum seconds between searches


def web_search(query: str, max_results: int = 4) -> List[Dict[str, Any]]:
    """
    Search the web using DuckDuckGo with rate limiting.
    """
    global _last_search_time

    # Rate limiting - wait between searches
    elapsed = time.time() - _last_search_time
    if elapsed < _MIN_DELAY:
        wait_time = _MIN_DELAY - elapsed + random.uniform(0.5, 1.5)
        time.sleep(wait_time)

    try:
        try:
            from ddgs import DDGS  # type: ignore
        except ImportError:
            from duckduckgo_search import DDGS

        _last_search_time = time.time()

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r.get("title", ""),
                "url": r.get("href") or r.get("link", ""),
                "snippet": r.get("body") or r.get("snippet", "")
            })

        logger.info(f"✅ Search successful: '{query}' returned {len(formatted_results)} results")
        return formatted_results

    except Exception as e:
        error_str = str(e)
        if "Ratelimit" in error_str or "429" in error_str or "202" in error_str:
            logger.warning(f"⚠️ Rate limited for '{query}', waiting and retrying...")
            time.sleep(5 + random.uniform(1, 3))
            _last_search_time = time.time()
            try:
                from duckduckgo_search import DDGS
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=max_results))
                formatted = [
                    {
                        "title": r.get("title", ""),
                        "url": r.get("href") or r.get("link", ""),
                        "snippet": r.get("body") or r.get("snippet", "")
                    }
                    for r in results
                ]
                logger.info(f"✅ Retry successful: '{query}' returned {len(formatted)} results")
                return formatted
            except Exception:
                pass

        logger.warning(f"⚠️ Search failed for '{query}': {error_str[:80]}")
        return []


def run_searches(queries: List[str], max_results_per_query: int = 3, max_total: int = 12) -> List[Dict[str, Any]]:
    """
    Run multiple search queries with rate limiting.
    """
    all_results = []

    for i, query in enumerate(queries):
        # Reduce number of searches to avoid rate limits
        if len(all_results) >= max_total:
            break

        results = web_search(query, max_results=max_results_per_query)
        all_results.extend(results)

    # Deduplicate by URL
    seen_urls = set()
    unique_results = []
    for result in all_results:
        url = result.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

    return unique_results[:max_total]


def build_search_context(results: List[Dict[str, Any]], max_items: int = 10) -> str:
    """
    Format search results into a context string for LLM consumption.
    """
    if not results:
        return "No web search results available. Use your general knowledge to provide recommendations."

    context = ""
    for i, result in enumerate(results[:max_items], 1):
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        snippet = result.get("snippet", "")

        context += f"\n{i}. {title}\n"
        if url:
            context += f"   Source: {url}\n"
        if snippet:
            context += f"   {snippet}\n"

    return context