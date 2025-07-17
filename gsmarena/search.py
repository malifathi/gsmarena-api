from typing import List, Dict

from .utils import get_data_from_url, soup_from_html

__all__ = ["search"]


def search(query: str) -> List[Dict]:
    """Search devices by *query* string."""
    html = get_data_from_url(f"/results.php3?sQuickSearch=yes&sName={query}")
    soup = soup_from_html(html)

    results: List[Dict] = []
    for li in soup.select(".makers li"):
        a_tag = li.find("a", href=True)
        if not a_tag:
            continue
        device_id = a_tag["href"].replace(".php", "")
        img_tag = li.find("img")
        name_parts = li.find("span").decode_contents().split("<br>")
        name = " ".join(part.strip() for part in name_parts if part.strip())
        results.append(
            {
                "id": device_id,
                "name": name,
                "img": img_tag["src"] if img_tag else None,
                "description": img_tag.get("title") if img_tag else None,
            }
        )
    return results