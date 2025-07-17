"""Glossary module for GSMArena API - handles glossary terms and definitions"""

from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .utils import get_data_from_url


class Glossary:
    """Glossary service for managing technology terms and definitions"""
    
    def get(self) -> List[Dict[str, Any]]:
        """
        Get glossary terms organized by letter
        
        Returns:
            List of dictionaries with letters and their associated terms
        """
        html = get_data_from_url('/glossary.php3')
        soup = BeautifulSoup(html, 'html.parser')
        
        glossary = []
        body = soup.find('div', id='body')
        
        if body:
            st_text = body.find(class_='st-text')
            if st_text:
                children = list(st_text.children)
                
                for i in range(0, len(children), 2):
                    if i + 1 < len(children):
                        letter_element = children[i]
                        terms_element = children[i + 1]
                        
                        # Check if this is a letter header
                        if hasattr(letter_element, 'get_text'):
                            letter = letter_element.get_text().strip()
                            
                            # Extract terms for this letter
                            terms = []
                            if hasattr(terms_element, 'find_all'):
                                term_links = terms_element.find_all('a')
                                
                                for link in term_links:
                                    href = link.get('href', '')
                                    term_id = href.replace('glossary.php3?term=', '')
                                    term_name = link.get_text()
                                    
                                    if term_id and term_name:
                                        terms.append({
                                            'id': term_id,
                                            'name': term_name
                                        })
                            
                            if letter and terms:
                                glossary.append({
                                    'letter': letter,
                                    'list': terms
                                })
        
        return glossary
    
    def get_term(self, term: str) -> Dict[str, Any]:
        """
        Get detailed definition for a specific glossary term
        
        Args:
            term: Term ID (e.g., 'xenon-flash')
            
        Returns:
            Dictionary with term title and HTML content
        """
        html = get_data_from_url(f'/glossary.php3?term={term}')
        soup = BeautifulSoup(html, 'html.parser')
        
        body = soup.find('div', id='body')
        title = ''
        content = ''
        
        if body:
            # Extract title
            title_element = body.select_one('.review-header .article-hgroup h1')
            title = title_element.get_text() if title_element else ''
            
            # Extract content
            content_element = body.select_one('.st-text')
            if content_element:
                # Get the HTML content of the first st-text element
                content = str(content_element)
            else:
                content = ''
        
        return {
            'title': title,
            'html': content
        }


# Create instance to export
glossary = Glossary()