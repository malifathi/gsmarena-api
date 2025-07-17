from typing import List, Dict

from bs4 import BeautifulSoup

from .utils import get_data_from_url, soup_from_html, get_price

__all__ = ["get_deals"]


def get_deals() -> List[Dict]:
    """Return current deals list as shown on gsmarena.com/deals.php3."""
    html = get_data_from_url("/deals.php3")
    soup = soup_from_html(html)

    deals: List[Dict] = []

    for div in soup.select("#body .pricecut"):
        img_url = div.select_one(".row a img")
        img = img_url["src"] if img_url else None
        url_tag = div.select_one(".row a.image")
        url = url_tag["href"] if url_tag else None
        name = (div.select_one(".row .phone div h3") or BeautifulSoup("", "lxml")).get_text(strip=True)
        id_tag = div.select_one(".row .phone div a")
        device_id = id_tag["href"].replace(".php", "") if id_tag else None
        description = (div.select_one(".row .phone p a") or BeautifulSoup("", "lxml")).get_text(strip=True)

        # Pricing information
        price_tag = div.select_one(".row .phone .deal a.price")
        price_info = get_price(price_tag.get_text(strip=True) if price_tag else "")

        deal_obj = {
            "memory": (div.select_one(".row .phone .deal a.memory") or BeautifulSoup("", "lxml")).get_text(strip=True),
            "storeImg": (div.select_one(".row .phone .deal a.store img") or BeautifulSoup("", "lxml")).get("src"),
            "price": price_info["price"],
            "currency": price_info["currency"],
            "discount": None,
        }
        discount_tag = div.select_one(".row .phone .deal a.discount")
        if discount_tag:
            try:
                deal_obj["discount"] = float(discount_tag.get_text(strip=True))
            except ValueError:
                deal_obj["discount"] = None

        device_data: Dict = {
            "id": device_id,
            "img": img,
            "url": url,
            "name": name,
            "description": description,
            "deal": deal_obj,
        }

        # Parse price history
        history = []
        stats_children = div.select(".history .stats > *")
        for idx, elem in enumerate(stats_children):
            if idx % 2 == 0:
                history.append({"time": elem.get_text(strip=True)})
            else:
                price_d = get_price(elem.get_text(strip=True))
                history_index = idx // 2
                history[history_index].update(price_d)

        device_data["history"] = history
        deals.append(device_data)

    return deals