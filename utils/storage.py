"""
Storage utilities for managing sent links
"""

import json
import logging
import os
from typing import List, Dict, Set
from config import SENT_LINKS_FILE

logger = logging.getLogger(__name__)

def load_sent_links() -> Set[str]:
    """
    Load previously sent links from JSON file
    
    Returns:
        Set of sent links
    """
    try:
        if os.path.exists(SENT_LINKS_FILE):
            with open(SENT_LINKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                sent_links = set(data.get('links', []))
                logger.info(f"Loaded {len(sent_links)} previously sent links")
                return sent_links
        else:
            logger.info("No existing sent links file found, starting fresh")
            return set()
    except Exception as e:
        logger.error(f"Error loading sent links: {e}")
        return set()

def save_sent_links(sent_links: Set[str]) -> None:
    """
    Save sent links to JSON file
    
    Args:
        sent_links: Set of sent links to save
    """
    try:
        data = {
            'links': list(sent_links),
            'last_updated': str(os.path.getmtime(SENT_LINKS_FILE) if os.path.exists(SENT_LINKS_FILE) else 'new')
        }
        
        with open(SENT_LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(sent_links)} links to {SENT_LINKS_FILE}")
        
    except Exception as e:
        logger.error(f"Error saving sent links: {e}")

def filter_new_updates(updates: List[Dict[str, str]], sent_links: Set[str]) -> List[Dict[str, str]]:
    """
    Filter out updates that have already been sent
    
    Args:
        updates: List of update dictionaries
        sent_links: Set of previously sent links
        
    Returns:
        List of new updates
    """
    new_updates = []
    
    for update in updates:
        link = update.get('link', '')
        if link and link not in sent_links:
            new_updates.append(update)
    
    logger.info(f"Filtered {len(updates)} updates, {len(new_updates)} are new")
    return new_updates

def add_to_sent_links(updates: List[Dict[str, str]], sent_links: Set[str]) -> Set[str]:
    """
    Add new updates to sent links set
    
    Args:
        updates: List of update dictionaries to add
        sent_links: Existing set of sent links
        
    Returns:
        Updated set of sent links
    """
    for update in updates:
        link = update.get('link', '')
        if link:
            sent_links.add(link)
    
    return sent_links
