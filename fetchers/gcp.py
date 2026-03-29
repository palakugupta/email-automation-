"""
Google Cloud Platform release notes fetcher using RSS
"""

import feedparser
import logging
from typing import List, Dict
import time
from config import REQUEST_TIMEOUT, RETRY_ATTEMPTS, RETRY_DELAY

logger = logging.getLogger(__name__)

def fetch_gcp_updates(url: str) -> List[Dict[str, str]]:
    """
    Fetch AI-related release notes from GCP RSS feed
    
    Args:
        url: GCP release notes RSS feed URL
        
    Returns:
        List of dictionaries containing title and link
    """
    updates = []
    
    for attempt in range(RETRY_ATTEMPTS):
        try:
            logger.info(f"Fetching GCP updates (attempt {attempt + 1})")
            
            # Parse RSS feed
            feed = feedparser.parse(url)
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing warning: {feed.bozo_exception}")
            
            entries = feed.entries
            
            for entry in entries[:20]:  # Limit to first 20 entries
                try:
                    title = entry.get('title', '').strip()
                    link = entry.get('link', '').strip()
                    
                    if title and link:
                        updates.append({
                            "title": title,
                            "link": link
                        })
                        
                except Exception as e:
                    logger.warning(f"Error processing GCP entry: {e}")
                    continue
            
            logger.info(f"Found {len(updates)} GCP updates")
            return updates
            
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed for GCP: {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to fetch GCP updates after {RETRY_ATTEMPTS} attempts")
                return []
    
    return updates
