"""Utility functions for GSMArena API"""

import requests
import re
from typing import Dict, Any


def get_data_from_url(url: str) -> str:
    """
    Fetch HTML data from GSMArena URL
    
    Args:
        url: The relative URL path (e.g., '/makers.php3')
        
    Returns:
        HTML content as string
        
    Raises:
        requests.RequestException: If the request fails
    """
    response = requests.get(f"https://www.gsmarena.com{url}")
    response.raise_for_status()
    return response.text


def get_price(text: str) -> Dict[str, Any]:
    """
    Parse price text and extract currency and numeric value
    
    Args:
        text: Price text like "£ 449.00" or "$ 1,299.99"
        
    Returns:
        Dictionary with 'currency' and 'price' keys
    """
    # Remove commas and split by space
    clean_text = text.replace(',', '')
    parts = clean_text.split(' ')
    
    if len(parts) >= 2:
        currency = parts[0]
        try:
            price = float(parts[1])
        except (ValueError, IndexError):
            price = 0.0
    else:
        currency = ""
        price = 0.0
    
    return {
        'currency': currency,
        'price': price
    }