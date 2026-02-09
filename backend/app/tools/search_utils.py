from typing import List, Dict, Any
from app.tools.web_search import web_search_tool


def run_searches(
    queries: List[str],
    *,
    max_results_per_query: int = 4,
    max_total: int = 12,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    seen = set()

    for query in queries:
        try:
            batch = web_search_tool.invoke(
                {"query": query, "max_results": max_results_per_query}
            )
        except Exception:
            batch = []

        for r in batch:
            url = (r.get("url") or "").strip()
            title = (r.get("title") or "").strip()
            key = url or title
            if not key or key in seen:
                continue
            seen.add(key)
            results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": (r.get("snippet") or "").strip(),
                }
            )
            if len(results) >= max_total:
                return results

    return results


def build_search_context(
    results: List[Dict[str, Any]], *, max_items: int = 12
) -> str:
    if not results:
        return "No search results found."

    lines = []
    for idx, r in enumerate(results[:max_items], start=1):
        title = r.get("title") or "Untitled"
        snippet = r.get("snippet") or ""
        url = r.get("url") or ""
        lines.append(f"[{idx}] {title}\n{snippet}\nURL: {url}")

    return "\n\n".join(lines)
