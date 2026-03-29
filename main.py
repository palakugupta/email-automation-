"""
AI Release Notes Tracker - Main Application

This script fetches AI/ML related release notes from Databricks, Snowflake, and GCP,
filters them for AI content, removes duplicates, and sends a daily email digest.
"""

import logging
import sys
import argparse
from typing import Dict, List
from datetime import datetime

# Import project modules
from config import SOURCES, MAX_UPDATES_PER_SOURCE, MAX_TOTAL_UPDATES, LOG_FILE
from fetchers import fetch_databricks_updates, fetch_snowflake_updates, fetch_gcp_updates
from utils import filter_ai_updates, load_sent_links, save_sent_links, filter_new_updates, add_to_sent_links, send_email, create_test_email

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def fetch_all_updates() -> Dict[str, List[Dict[str, str]]]:
    """
    Fetch updates from all sources
    
    Returns:
        Dictionary of updates grouped by source
    """
    logger.info("Starting to fetch updates from all sources")
    
    all_updates = {}
    
    # Fetch from Databricks
    try:
        databricks_updates = fetch_databricks_updates(SOURCES["Databricks"])
        all_updates["Databricks"] = databricks_updates
        logger.info(f"Fetched {len(databricks_updates)} updates from Databricks")
    except Exception as e:
        logger.error(f"Error fetching Databricks updates: {e}")
        all_updates["Databricks"] = []
    
    # Fetch from Snowflake
    try:
        snowflake_updates = fetch_snowflake_updates(SOURCES["Snowflake"])
        all_updates["Snowflake"] = snowflake_updates
        logger.info(f"Fetched {len(snowflake_updates)} updates from Snowflake")
    except Exception as e:
        logger.error(f"Error fetching Snowflake updates: {e}")
        all_updates["Snowflake"] = []
    
    # Fetch from GCP
    try:
        gcp_updates = fetch_gcp_updates(SOURCES["GCP"])
        all_updates["GCP"] = gcp_updates
        logger.info(f"Fetched {len(gcp_updates)} updates from GCP")
    except Exception as e:
        logger.error(f"Error fetching GCP updates: {e}")
        all_updates["GCP"] = []
    
    return all_updates

def process_updates(all_updates: Dict[str, List[Dict[str, str]]], sent_links: set) -> Dict[str, List[Dict[str, str]]]:
    """
    Process updates: filter AI content and remove duplicates
    
    Args:
        all_updates: Raw updates from all sources
        sent_links: Set of previously sent links
        
    Returns:
        Processed updates ready for email
    """
    logger.info("Processing updates: filtering AI content and removing duplicates")
    
    processed_updates = {}
    total_new_updates = 0
    
    for source, updates in all_updates.items():
        logger.info(f"Processing {len(updates)} updates from {source}")
        
        # Filter for AI/ML related content
        ai_updates = filter_ai_updates(updates, source)
        
        # Remove already sent updates
        new_updates = filter_new_updates(ai_updates, sent_links)
        
        # Limit updates per source
        limited_updates = new_updates[:MAX_UPDATES_PER_SOURCE]
        
        processed_updates[source] = limited_updates
        total_new_updates += len(limited_updates)
        
        logger.info(f"{source}: {len(limited_updates)} new AI updates (from {len(updates)} total)")
    
    # Apply total limit if needed
    if total_new_updates > MAX_TOTAL_UPDATES:
        logger.info(f"Limiting total updates to {MAX_TOTAL_UPDATES}")
        
        # Sort sources by number of updates and distribute fairly
        sorted_sources = sorted(processed_updates.items(), key=lambda x: len(x[1]), reverse=True)
        
        limited_updates = {}
        remaining_slots = MAX_TOTAL_UPDATES
        
        for source, updates in sorted_sources:
            if remaining_slots <= 0:
                break
            
            take = min(len(updates), remaining_slots)
            limited_updates[source] = updates[:take]
            remaining_slots -= take
        
        processed_updates = limited_updates
    
    return processed_updates

def main():
    """Main application function"""
    parser = argparse.ArgumentParser(description='AI Release Notes Tracker')
    parser.add_argument('--test', action='store_true', help='Send a test email')
    parser.add_argument('--dry-run', action='store_true', help='Run without sending email')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    global logger
    logger = logging.getLogger(__name__)
    logger.info("AI Release Notes Tracker started")
    
    # Handle test email
    if args.test:
        logger.info("Sending test email...")
        if create_test_email():
            logger.info("Test email sent successfully!")
            return 0
        else:
            logger.error("Failed to send test email")
            return 1
    
    try:
        # Load previously sent links
        sent_links = load_sent_links()
        
        # Fetch all updates
        all_updates = fetch_all_updates()
        
        # Process updates
        processed_updates = process_updates(all_updates, sent_links)
        
        # Count total updates
        total_updates = sum(len(updates) for updates in processed_updates.values())
        
        if total_updates == 0:
            logger.info("No new AI/ML updates found")
            if not args.dry_run:
                # Send email even if no updates (to show system is working)
                send_email(processed_updates)
            else:
                logger.info("Dry run: Would send 'no updates' email")
        else:
            logger.info(f"Found {total_updates} new AI/ML updates to send")
            
            if not args.dry_run:
                # Send email with updates
                if send_email(processed_updates):
                    # Update sent links after successful email
                    for source, updates in processed_updates.items():
                        sent_links = add_to_sent_links(updates, sent_links)
                    
                    save_sent_links(sent_links)
                    logger.info("Email sent successfully and sent links updated")
                else:
                    logger.error("Failed to send email, not updating sent links")
                    return 1
            else:
                logger.info("Dry run: Would send email with updates")
                # Show what would be sent
                for source, updates in processed_updates.items():
                    logger.info(f"{source}: {len(updates)} updates")
                    for update in updates[:2]:  # Show first 2 as example
                        logger.info(f"  - {update.get('title', 'No title')}")
        
        logger.info("AI Release Notes Tracker completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
