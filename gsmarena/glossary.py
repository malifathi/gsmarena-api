from typing import List, Dict

from .utils import get_data_from_url, soup_from_html

__all__ = ["get_glossary", "get_term"]


def get_glossary() -> List[Dict]:
    """Return alphabetical glossary of terms."""
    html = get_data_from_url("/glossary.php3")
    soup = soup_from_html(html)

    glossary: List[Dict] = []
    parent_terms = soup.select("#body .st-text")
    for idx, el in enumerate(parent_terms[0].children if parent_terms else []):
        if getattr(el, "name", None) is None:
            # Skip NavigableString etc.
            continue
        if idx % 2 == 0:
            glossary.append({"letter": el.get_text(strip=True), "list": []})
        else:
            for a in el.select("a"):
                term_id = a["href"].replace("glossary.php3?term=", "")
                name = a.get_text(strip=True)
                glossary[-1]["list"].append({"id": term_id, "name": name})
    return glossary


def get_term(term: str) -> Dict:
    """Return a single glossary term details."""
    html = get_data_from_url(f"/glossary.php3?term={term}")
    soup = soup_from_html(html)

    body = soup.select_one("#body")
    title = body.select_one(".review-header .article-hgroup h1").get_text(strip=True) if body else ""
    text_node = body.select_one(".st-text") if body else None
    text_html = text_node.decode_contents() if text_node else ""

    return {"title": title, "html": text_html}