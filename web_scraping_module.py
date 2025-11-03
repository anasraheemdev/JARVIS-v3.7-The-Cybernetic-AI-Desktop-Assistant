"""
Web Scraping Module
Handles web scraping, data extraction, and data collection
"""

import logging
from typing import Dict, Optional, List
import json

logger = logging.getLogger(__name__)

# Web scraping
try:
    from bs4 import BeautifulSoup
    import requests
    WEB_SCRAPING_AVAILABLE = True
except ImportError:
    WEB_SCRAPING_AVAILABLE = False
    logger.warning("BeautifulSoup/requests not installed. Web scraping will be limited.")

# Excel handling
try:
    from openpyxl import Workbook
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    logger.warning("openpyxl not installed. Excel export will be limited.")

class WebScrapingModule:
    """Handles web scraping and data extraction"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
    
    def scrape_website(self, params: Dict) -> str:
        """Scrape a website and extract data"""
        if not WEB_SCRAPING_AVAILABLE:
            return "Web scraping not available. Install: pip install beautifulsoup4 requests"
        
        try:
            url = params.get('url', '')
            selector = params.get('selector', '')  # CSS selector or element type
            extract_text = params.get('extract_text', True)
            
            if not url:
                return "Error: URL required"
            
            # Fetch webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if selector:
                # Find elements by selector
                elements = soup.select(selector)
                results = [elem.get_text(strip=True) if extract_text else str(elem) for elem in elements]
            else:
                # Extract all text
                results = [soup.get_text(strip=True)]
            
            result_text = "\n".join(results[:50])  # Limit to 50 results
            
            return f"Scraped {len(results)} items from {url}:\n\n{result_text}"
        
        except Exception as e:
            logger.error(f"Error scraping website: {e}")
            return f"Error scraping: {e}"
    
    def extract_to_excel(self, params: Dict) -> str:
        """Extract data and save to Excel"""
        if not EXCEL_AVAILABLE:
            return "Excel export not available. Install: pip install openpyxl"
        
        try:
            data = params.get('data', [])  # List of dictionaries or lists
            filename = params.get('filename', 'extracted_data.xlsx')
            headers = params.get('headers', [])
            
            if not data:
                return "Error: No data provided"
            
            from pathlib import Path
            from openpyxl import Workbook
            
            output_path = Path.home() / 'Desktop' / filename
            
            wb = Workbook()
            ws = wb.active
            
            # Add headers if provided
            if headers:
                ws.append(headers)
            
            # Add data rows
            for row in data:
                if isinstance(row, dict):
                    # Convert dict to list based on headers
                    if headers:
                        row_data = [row.get(h, '') for h in headers]
                    else:
                        row_data = list(row.values())
                    ws.append(row_data)
                elif isinstance(row, list):
                    ws.append(row)
                else:
                    ws.append([str(row)])
            
            wb.save(output_path)
            
            return f"Data exported to Excel: {output_path}"
        
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            return f"Error: {e}"
    
    def monitor_price(self, params: Dict) -> str:
        """Monitor price of a product (placeholder - needs specific implementation)"""
        try:
            url = params.get('url', '')
            product_name = params.get('product', '')
            
            if not url:
                return "Error: Product URL required"
            
            # This is a placeholder - actual implementation would need site-specific logic
            return f"Price monitoring for {product_name} at {url} - Feature requires site-specific implementation"
        
        except Exception as e:
            logger.error(f"Error monitoring price: {e}")
            return f"Error: {e}"

