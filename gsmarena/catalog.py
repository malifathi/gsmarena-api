import re
from typing import List, Dict

from bs4 import Tag

from .utils import get_data_from_url, soup_from_html

__all__ = [
    "get_brands",
    "get_brand",
    "get_device",
]


def _extract_devices(list_items) -> List[Dict]:
    """Return a list with basic info for each device present in *list_items*."""
    devices = []
    for li in list_items:
        if not isinstance(li, Tag):
            continue
        a_tag = li.find("a", href=True)
        if not a_tag:
            continue
        device_id = a_tag["href"].replace(".php", "")
        img_tag = li.find("img")
        devices.append(
            {
                "id": device_id,
                "name": li.find("span").get_text(strip=True),
                "img": img_tag["src"] if img_tag else None,
                "description": img_tag.get("title") if img_tag else None,
            }
        )
    return devices


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def get_brands() -> List[Dict]:
    """Return a list with all phone brands listed on GSM Arena."""
    html = get_data_from_url("/makers.php3")
    soup = soup_from_html(html)

    brands: List[Dict] = []
    for td in soup.select("table td"):
        a_tag = td.find("a", href=True)
        if not a_tag:
            continue
        brand_id = a_tag["href"].replace(".php", "")
        brand_name = re.sub(r"\d", "", a_tag.get_text()).replace(" devices", "").strip()
        devices_span = td.find("span")
        devices_count = (
            int(devices_span.get_text().replace(" devices", "").strip()) if devices_span else 0
        )
        brands.append({"id": brand_id, "name": brand_name, "devices": devices_count})
    return brands


def get_brand(brand: str) -> List[Dict]:
    """Return all devices for a given *brand* slug (e.g. "samsung")."""
    next_path = f"/{brand}.php"
    devices: List[Dict] = []

    while next_path:
        html = get_data_from_url(next_path)
        soup = soup_from_html(html)
        devices.extend(_extract_devices(soup.select(".makers li")))

        next_link = soup.select_one('a.prevnextbutton[title="Next page"]')
        next_path = f"/{next_link['href']}" if next_link else None
    return devices


def get_device(device_slug: str) -> Dict:
    """Return detailed specification dictionary for a single *device_slug*."""
    html = get_data_from_url(f"/{device_slug}.php")
    soup = soup_from_html(html)

    def _safe_text(selector: str):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else ""

    quick_spec = [
        {"name": "Display size", "value": _safe_text("span[data-spec=displaysize-hl]")},
        {"name": "Display resolution", "value": _safe_text("div[data-spec=displayres-hl]")},
        {"name": "Camera pixels", "value": _safe_text(".accent-camera")},
        {"name": "Video pixels", "value": _safe_text("div[data-spec=videopixels-hl]")},
        {"name": "RAM size", "value": _safe_text(".accent-expansion")},
        {"name": "Chipset", "value": _safe_text("div[data-spec=chipset-hl]")},
        {"name": "Battery size", "value": _safe_text(".accent-battery")},
        {"name": "Battery type", "value": _safe_text("div[data-spec=battype-hl]")},
    ]

    name = _safe_text(".specs-phone-name-title")
    img_tag = soup.select_one(".specs-photo-main a img")
    img_url = img_tag["src"] if img_tag else None

    detail_spec = []
    for table in soup.find_all("table"):
        category = table.find("th")
        if not category:
            continue
        spec_list = []
        for tr in table.find_all("tr"):
            name_td = tr.select_one("td.ttl")
            value_td = tr.select_one("td.nfo")
            if not name_td or not value_td:
                continue
            spec_list.append({"name": name_td.get_text(strip=True), "value": value_td.get_text(" ", strip=True)})
        if spec_list:
            detail_spec.append({"category": category.get_text(strip=True), "specifications": spec_list})

    return {
        "name": name,
        "img": img_url,
        "detailSpec": detail_spec,
        "quickSpec": quick_spec,
    }