"""Catalog module for GSMArena API - handles brands and device listings"""

from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import re
from .utils import get_data_from_url


class Catalog:
    """Catalog service for managing brands and devices"""
    
    def get_brands(self) -> List[Dict[str, Any]]:
        """
        Get list of all brands from GSMArena
        
        Returns:
            List of brand dictionaries with id, name, and device count
        """
        html = get_data_from_url('/makers.php3')
        soup = BeautifulSoup(html, 'html.parser')
        
        brands = []
        table = soup.find('table')
        if table:
            cells = table.find_all('td')
            
            for cell in cells:
                link = cell.find('a')
                span = cell.find('span')
                
                if link and span:
                    href = link.get('href', '')
                    brand_id = href.replace('.php', '')
                    
                    # Extract brand name (remove device count numbers)
                    brand_name = re.sub(r'\d+', '', link.get_text()).replace(' devices', '').strip()
                    
                    # Extract device count
                    span_text = span.get_text().replace(' devices', '')
                    try:
                        device_count = int(span_text)
                    except ValueError:
                        device_count = 0
                    
                    brands.append({
                        'id': brand_id,
                        'name': brand_name,
                        'devices': device_count
                    })
        
        return brands
    
    def _get_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        """Get the next page URL if it exists"""
        next_link = soup.find('a', class_='prevnextbutton', title='Next page')
        if next_link:
            href = next_link.get('href', '')
            return href.replace('.php', '')
        return None
    
    def _get_devices_from_soup(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract device information from soup"""
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
                    device_name = span.get_text()
                    device_img = img.get('src', '') if img else ''
                    device_description = img.get('title', '') if img else ''
                    
                    devices.append({
                        'id': device_id,
                        'name': device_name,
                        'img': device_img,
                        'description': device_description
                    })
        
        return devices
    
    def get_brand(self, brand: str) -> List[Dict[str, Any]]:
        """
        Get devices for a specific brand with pagination support
        
        Args:
            brand: Brand ID (e.g., 'apple-phones-48')
            
        Returns:
            List of device dictionaries
        """
        html = get_data_from_url(f'/{brand}.php')
        soup = BeautifulSoup(html, 'html.parser')
        
        all_devices = []
        
        # Get devices from first page
        devices = self._get_devices_from_soup(soup)
        all_devices.extend(devices)
        
        # Handle pagination
        while True:
            next_page = self._get_next_page(soup)
            if not next_page:
                break
                
            html = get_data_from_url(f'/{next_page}.php')
            soup = BeautifulSoup(html, 'html.parser')
            devices = self._get_devices_from_soup(soup)
            all_devices.extend(devices)
        
        return all_devices
    
    def get_device(self, device: str) -> Dict[str, Any]:
        """
        Get detailed specifications for a specific device
        
        Args:
            device: Device ID (e.g., 'apple_iphone_13_pro_max-11089')
            
        Returns:
            Dictionary with device specifications
        """
        html = get_data_from_url(f'/{device}.php')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract basic information
        name_element = soup.find(class_='specs-phone-name-title')
        name = name_element.get_text() if name_element else ''
        
        img_element = soup.select_one('.specs-photo-main a img')
        img = img_element.get('src', '') if img_element else ''
        
        # Extract quick specifications
        quick_spec = []
        
        # Helper function to add spec if element exists
        def add_spec(name: str, selector: str, attr: str = None):
            element = soup.select_one(selector)
            if element:
                value = element.get(attr) if attr else element.get_text()
                quick_spec.append({'name': name, 'value': value})
        
        add_spec('Display size', 'span[data-spec=displaysize-hl]')
        add_spec('Display resolution', 'div[data-spec=displayres-hl]')
        add_spec('Camera pixels', '.accent-camera')
        add_spec('Video pixels', 'div[data-spec=videopixels-hl]')
        add_spec('RAM size', '.accent-expansion')
        add_spec('Chipset', 'div[data-spec=chipset-hl]')
        add_spec('Battery size', '.accent-battery')
        add_spec('Battery type', 'div[data-spec=battype-hl]')
        
        # Extract detailed specifications
        detail_spec = []
        spec_tables = soup.find_all('table')
        
        for table in spec_tables:
            category_element = table.find('th')
            if not category_element:
                continue
                
            category = category_element.get_text()
            specifications = []
            
            rows = table.find_all('tr')
            for row in rows:
                ttl_cell = row.find('td', class_='ttl')
                nfo_cell = row.find('td', class_='nfo')
                
                if ttl_cell and nfo_cell:
                    specifications.append({
                        'name': ttl_cell.get_text(),
                        'value': nfo_cell.get_text()
                    })
            
            if category and specifications:
                detail_spec.append({
                    'category': category,
                    'specifications': specifications
                })
        
        return {
            'name': name,
            'img': img,
            'detailSpec': detail_spec,
            'quickSpec': quick_spec
        }


# Create instance to export
catalog = Catalog()