"""Deals module for GSMArena API - handles device deals and pricing"""

from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .utils import get_data_from_url, get_price


class Deals:
    """Deals service for managing device deals and pricing"""
    
    def get_deals(self) -> List[Dict[str, Any]]:
        """
        Get current device deals from GSMArena
        
        Returns:
            List of deal dictionaries with device info and pricing
        """
        html = get_data_from_url('/deals.php3')
        soup = BeautifulSoup(html, 'html.parser')
        
        deals = []
        body = soup.find('div', id='body')
        
        if body:
            deal_items = body.find_all(class_='pricecut')
            
            for item in deal_items:
                # Extract basic device information
                img_element = item.select_one('.row a img')
                img = img_element.get('src', '') if img_element else ''
                
                url_element = item.select_one('.row a.image')
                url = url_element.get('href', '') if url_element else ''
                
                name_element = item.select_one('.row .phone div h3')
                name = name_element.get_text() if name_element else ''
                
                id_element = item.select_one('.row .phone div a')
                device_id = id_element.get('href', '').replace('.php', '') if id_element else ''
                
                description_element = item.select_one('.row .phone p a')
                description = description_element.get_text() if description_element else ''
                
                # Extract deal information
                price_element = item.select_one('.row .phone .deal a.price')
                price_info = get_price(price_element.get_text()) if price_element else {'currency': '', 'price': 0.0}
                
                memory_element = item.select_one('.row .phone .deal a.memory')
                memory = memory_element.get_text() if memory_element else ''
                
                store_img_element = item.select_one('.row .phone .deal a.store img')
                store_img = store_img_element.get('src', '') if store_img_element else ''
                
                discount_element = item.select_one('.row .phone .deal a.discount')
                discount_text = discount_element.get_text() if discount_element else '0'
                try:
                    discount = float(discount_text)
                except ValueError:
                    discount = 0.0
                
                deal_info = {
                    'memory': memory,
                    'storeImg': store_img,
                    'price': price_info['price'],
                    'currency': price_info['currency'],
                    'discount': discount
                }
                
                # Extract price history
                history = []
                history_element = item.select_one('.history .stats')
                
                if history_element:
                    history_children = list(history_element.children)
                    
                    for i in range(0, len(history_children), 2):
                        if i + 1 < len(history_children):
                            time_element = history_children[i]
                            price_element = history_children[i + 1]
                            
                            if hasattr(time_element, 'get_text') and hasattr(price_element, 'get_text'):
                                time_text = time_element.get_text()
                                price_text = price_element.get_text()
                                history_price = get_price(price_text)
                                
                                history.append({
                                    'time': time_text,
                                    'price': history_price['price'],
                                    'currency': history_price['currency']
                                })
                
                device_deal = {
                    'id': device_id,
                    'img': img,
                    'url': url,
                    'name': name,
                    'description': description,
                    'deal': deal_info,
                    'history': history
                }
                
                deals.append(device_deal)
        
        return deals


# Create instance to export
deals = Deals()