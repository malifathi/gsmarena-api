import re
from typing import Dict

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.gsmarena.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    )
}


def get_data_from_url(path: str) -> str:
    """Return raw HTML from a gsmarena.com relative *path*.

    Parameters
    ----------
    path: str
        Path beginning with a leading slash (e.g. "/makers.php3").

    Returns
    -------
    str
        Raw HTML page text.
    """
    if not path.startswith("/"):
        path = "/" + path

    url = BASE_URL + path
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def get_price(text: str) -> Dict[str, float]:
    """Convert gsmarena price string into a structured dict.

    The price string is usually formatted like::

        "$ 499.00" or "€ 299"

    where the currency symbol precedes a *thin space* (\u2009) followed by
    a number that may contain commas.
    """
    # Remove any commas used as thousands separator and split on thin space
    cleaned = text.replace(",", "")
    parts = re.split(r"\u2009|\s+", cleaned.strip())
    if len(parts) < 2:
        return {"currency": "", "price": None}

    currency, price_str = parts[0], parts[1]
    try:
        price_val = float(price_str)
    except ValueError:
        price_val = None
    return {"currency": currency, "price": price_val}


def soup_from_html(html: str) -> BeautifulSoup:
    """Helper that returns a BeautifulSoup instance with the *lxml* parser."""
    return BeautifulSoup(html, "lxml")