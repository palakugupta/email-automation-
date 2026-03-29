"""
Content filtering utilities for AI/ML related updates
"""

import re
import logging
from typing import List, Dict
import requests
import urllib3
from config import KEYWORDS, REQUEST_TIMEOUT

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

def is_ai_ml_related(title: str, link: str, content: str = None) -> bool:
    """
    Check if content is related to AI/ML based on keywords
    
    Args:
        title: Title of the update
        link: URL of the update
        content: Optional page content
        
    Returns:
        True if AI/ML related, False otherwise
    """
    # Combine all text to search
    search_text = f"{title} {link}".lower()
    if content:
        search_text += f" {content.lower()}"
    
    # Check for keywords
    for keyword in KEYWORDS:
        if keyword.lower() in search_text:
            return True
    
    return False

def fetch_page_content(url: str) -> str:
    """
    Fetch page content for additional filtering
    
    Args:
        url: URL to fetch
        
    Returns:
        Page text content or empty string if failed
    """
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT, verify=False)
        response.raise_for_status()
        
        # Extract text from HTML (simple approach)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:2000]  # Limit to first 2000 characters
        
    except Exception as e:
        logger.warning(f"Failed to fetch content from {url}: {e}")
        return ""

def filter_ai_updates(updates: List[Dict[str, str]], source: str) -> List[Dict[str, str]]:
    """
    Filter updates to only include AI/ML related content
    
    Args:
        updates: List of update dictionaries
        source: Source name for logging
        
    Returns:
        Filtered list of AI/ML related updates
    """
    ai_updates = []
    
    logger.info(f"Filtering {len(updates)} updates from {source}")
    
    for update in updates:
        try:
            title = update.get('title', '')
            link = update.get('link', '')
            
            # First check title and link
            if is_ai_ml_related(title, link):
                ai_updates.append(update)
                continue
            
            # If not found in title/link, try fetching content (optional)
            # Only do this for a few items to avoid too many requests
            if len(ai_updates) < 5:  # Limit content fetching
                content = fetch_page_content(link)
                if is_ai_ml_related(title, link, content):
                    ai_updates.append(update)
                    
        except Exception as e:
            logger.warning(f"Error filtering update from {source}: {e}")
            continue
    
    logger.info(f"Found {len(ai_updates)} AI/ML related updates from {source}")
    return ai_updates
