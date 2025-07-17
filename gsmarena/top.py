"""Top module for GSMArena API - handles top devices rankings"""

from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .utils import get_data_from_url


class Top:
    """Top service for managing device rankings and popular devices"""
    
    def get(self) -> List[Dict[str, Any]]:
        """
        Get top devices rankings from GSMArena
        
        Returns:
            List of ranking categories with device lists
        """
        html = get_data_from_url('/deals.php3')
        soup = BeautifulSoup(html, 'html.parser')
        
        rankings = []
        sidebar = soup.select_one('.sidebar.col.left')
        
        if sidebar:
            ranking_modules = sidebar.find_all('div', class_='module module-rankings s3')
            
            for module in ranking_modules:
                # Get category name
                category_element = module.find('h4')
                category = category_element.get_text() if category_element else ''
                
                # Get ranking items
                ranks = []
                table_rows = module.find_all('tr')
                
                for i, row in enumerate(table_rows):
                    position_cell = row.find('td', headers='th3a')
                    link_cell = row.find('a')
                    hits_cell = row.find('td', headers='th3c')
                    
                    if position_cell and link_cell:
                        position_text = position_cell.get_text().replace('.', '')
                        try:
                            position = int(position_text)
                        except ValueError:
                            continue
                        
                        device_name = link_cell.find('nobr')
                        name = device_name.get_text() if device_name else link_cell.get_text()
                        
                        device_id = link_cell.get('href', '').replace('.php', '')
                        
                        # Get hits/favorites count
                        hits_text = hits_cell.get_text().replace(',', '') if hits_cell else '0'
                        try:
                            hits_count = int(hits_text)
                        except ValueError:
                            hits_count = 0
                        
                        rank_entry = {
                            'position': position,
                            'id': device_id,
                            'name': name
                        }
                        
                        # First entry usually has daily hits, others have favorites
                        if i == 0:
                            rank_entry['dailyHits'] = hits_count
                        else:
                            rank_entry['favorites'] = hits_count
                        
                        ranks.append(rank_entry)
                
                if category and ranks:
                    rankings.append({
                        'category': category,
                        'list': ranks
                    })
        
        return rankings


# Create instance to export
top = Top()