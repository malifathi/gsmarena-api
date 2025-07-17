"""Search module for GSMArena API - handles device searching"""

from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .utils import get_data_from_url


class Search:
    """Search service for finding devices"""
    
    def search(self, search_value: str) -> List[Dict[str, Any]]:
        """
        Search for devices by keyword
        
        Args:
            search_value: Search term (e.g., 'casio', 'iphone')
            
        Returns:
            List of device dictionaries matching the search term
        """
        html = get_data_from_url(f'/results.php3?sQuickSearch=yes&sName={search_value}')
        soup = BeautifulSoup(html, 'html.parser')
        
        devices = []
        makers_div = soup.find('div', class_='makers')
        
        if makers_div:
            device_items = makers_div.find_all('li')
            
            for item in device_items:
                link = item.find('a')
                span = item.find('span')
                img = item.find('img')
                
                if link and span:
                    device_id = link.get('href', '').replace('.php', '')
                    
                    # Handle device name with potential HTML breaks
                    span_html = str(span)
                    device_name = span.get_text().replace('\n', ' ').strip()
                    # Remove extra whitespace
                    device_name = ' '.join(device_name.split())
                    
                    device_img = img.get('src', '') if img else ''
                    device_description = img.get('title', '') if img else ''
                    
                    devices.append({
                        'id': device_id,
                        'name': device_name,
                        'img': device_img,
                        'description': device_description
                    })
        
        return devices


# Create instance to export
search = Search()