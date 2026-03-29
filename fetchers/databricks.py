"""
Databricks release notes fetcher
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

def fetch_databricks_updates(url: str) -> List[Dict[str, str]]:
    """
    Fetch AI-related release notes from Databricks
    
    Args:
        url: Databricks release notes URL
        
    Returns:
        List of dictionaries containing title and link
    """
    updates = []
    
    for attempt in range(RETRY_ATTEMPTS):
        try:
            logger.info(f"Fetching Databricks updates (attempt {attempt + 1})")
            response = requests.get(url, timeout=REQUEST_TIMEOUT, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for release notes sections
            # Databricks typically has release items in lists or cards
            release_items = soup.find_all(['li', 'div'], class_=lambda x: x and ('release' in x.lower() or 'note' in x.lower()))
            
            if not release_items:
                # Try alternative selectors
                release_items = soup.find_all('a', href=lambda x: x and 'release' in x.lower())
            
            if not release_items:
                # Look for any links that might be release-related
                release_items = soup.find_all('a', href=lambda x: x and ('release' in x.lower() or 'version' in x.lower()))
            
            for item in release_items[:10]:  # Limit to first 10 items
                try:
                    # Extract title and link
                    if item.name == 'a':
                        title = item.get_text(strip=True)
                        link = item.get('href')
                    else:
                        # Look for link inside the item
                        link_elem = item.find('a')
                        if link_elem:
                            title = link_elem.get_text(strip=True) or item.get_text(strip=True)
                            link = link_elem.get('href')
                        else:
                            title = item.get_text(strip=True)
                            link = None
                    
                    if title and link:
                        # Ensure link is absolute
                        if link.startswith('/'):
                            link = f"https://docs.databricks.com{link}"
                        elif not link.startswith('http'):
                            continue
                        
                        updates.append({
                            "title": title,
                            "link": link
                        })
                        
                except Exception as e:
                    logger.warning(f"Error processing Databricks item: {e}")
                    continue
            
            logger.info(f"Found {len(updates)} Databricks updates")
            return updates
            
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for Databricks: {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to fetch Databricks updates after {RETRY_ATTEMPTS} attempts")
                return []
    
    return updates
