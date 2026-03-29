"""
Snowflake release notes fetcher
"""

import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
import time
import urllib3
from config import REQUEST_TIMEOUT, RETRY_ATTEMPTS, RETRY_DELAY

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

def fetch_snowflake_updates(url: str) -> List[Dict[str, str]]:
    """
    Fetch AI-related release notes from Snowflake
    
    Args:
        url: Snowflake release notes URL
        
    Returns:
        List of dictionaries containing title and link
    """
    updates = []
    
    for attempt in range(RETRY_ATTEMPTS):
        try:
            logger.info(f"Fetching Snowflake updates (attempt {attempt + 1})")
            response = requests.get(url, timeout=REQUEST_TIMEOUT, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for release notes sections
            # Snowflake typically has release items in various formats
            release_items = []
            
            # Try different selectors that Snowflake might use
            selectors = [
                'a[href*="release"]',
                'a[href*="version"]',
                '.release-item a',
                '.version-item a',
                'li a',
                'td a'
            ]
            
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    release_items.extend(items)
                    break
            
            # If no specific items found, look for any links with release/version in text
            if not release_items:
                all_links = soup.find_all('a')
                release_items = [link for link in all_links if any(keyword in link.get_text().lower() 
                              for keyword in ['release', 'version', 'update'])]
            
            for item in release_items[:15]:  # Limit to first 15 items
                try:
                    title = item.get_text(strip=True)
                    link = item.get('href')
                    
                    if title and link:
                        # Ensure link is absolute
                        if link.startswith('/'):
                            link = f"https://docs.snowflake.com{link}"
                        elif not link.startswith('http'):
                            continue
                        
                        # Skip empty or very short titles
                        if len(title) < 10:
                            continue
                        
                        updates.append({
                            "title": title,
                            "link": link
                        })
                        
                except Exception as e:
                    logger.warning(f"Error processing Snowflake item: {e}")
                    continue
            
            logger.info(f"Found {len(updates)} Snowflake updates")
            return updates
            
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for Snowflake: {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to fetch Snowflake updates after {RETRY_ATTEMPTS} attempts")
                return []
    
    return updates
