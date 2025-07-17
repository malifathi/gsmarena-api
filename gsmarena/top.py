from typing import List, Dict

from .utils import get_data_from_url, soup_from_html

__all__ = ["get_top"]


def get_top() -> List[Dict]:
    """Return device rankings visible in the sidebar of the deals page."""
    html = get_data_from_url("/deals.php3")
    soup = soup_from_html(html)

    categories_data: List[Dict] = []
    for module in soup.select(".sidebar.col.left .module.module-rankings.s3"):
        category_name = module.find("h4").get_text(strip=True)
        positions = module.find_all("tr")

        ranks: List[Dict] = []
        for index, row in enumerate(positions):
            position_txt = row.select_one("td[headers=th3a]").get_text(strip=True)
            if not position_txt:
                continue
            try:
                position_idx = int(position_txt.replace(".", ""))
            except ValueError:
                continue

            name = row.select_one("nobr").get_text(strip=True)
            id_tag = row.find("a", href=True)
            device_id = id_tag["href"].replace(".php", "") if id_tag else None
            count_td = row.select_one("td[headers=th3c]")
            index_val = int(count_td.get_text(strip=True).replace(",", "")) if count_td else 0

            element = {"position": position_idx, "id": device_id, "name": name}
            if index == 0:
                element["dailyHits"] = index_val
            else:
                element["favorites"] = index_val
            ranks.append(element)

        categories_data.append({"category": category_name, "list": ranks})

    return categories_data