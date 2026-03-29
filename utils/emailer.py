"""
Email functionality for sending AI release notes digest
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime
import requests
import urllib3
from utils.html_emailer import send_html_email
from config import EMAIL_CONFIG

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

def get_link_preview(url: str, max_length: int = 100) -> str:
    """
    Get a brief preview of the link content
    
    Args:
        url: URL to fetch preview from
        max_length: Maximum length of preview
        
    Returns:
        Preview text or error message
    """
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc.get('content').strip()
            return desc[:max_length] + "..." if len(desc) > max_length else desc
        
        # Try og:description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            desc = og_desc.get('content').strip()
            return desc[:max_length] + "..." if len(desc) > max_length else desc
        
        # Fallback to first paragraph
        first_p = soup.find('p')
        if first_p:
            text = first_p.get_text(strip=True)
            return text[:max_length] + "..." if len(text) > max_length else text
        
        return "No preview available"
        
    except Exception:
        return "Preview unavailable"

def format_email_content(updates_by_source: Dict[str, List[Dict[str, str]]]) -> str:
    """
    Format updates into a professional, aesthetically pleasing email body
    
    Args:
        updates_by_source: Dictionary of updates grouped by source
        
    Returns:
        Formatted email content as string
    """
    content = []
    
    # Professional header with company branding
    content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
    content.append("│                     AI RELEASE NOTES DIGEST                               │")
    content.append("│                Impact Analytics - Technology Intelligence                  │")
    content.append("└─────────────────────────────────────────────────────────────────────────────┘")
    content.append("")
    
    content.append(f"📅 Date: {datetime.now().strftime('%B %d, %Y')}")
    content.append(f"🕐 Generated: {datetime.now().strftime('%I:%M %p')}")
    content.append("")
    
    total_updates = sum(len(updates) for updates in updates_by_source.values())
    
    if total_updates == 0:
        content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
        content.append("│                             NO NEW UPDATES                                │")
        content.append("└─────────────────────────────────────────────────────────────────────────────┘")
        content.append("")
        content.append("🤖 No new AI/ML related updates found today.")
        content.append("")
        content.append("📊 The system continuously monitors:")
        content.append("   • Databricks Platform Updates")
        content.append("   • Snowflake Cloud Data Platform")
        content.append("   • Google Cloud Platform Releases")
        content.append("")
        content.append("🔔 Check back tomorrow for the latest AI technology updates!")
        content.append("")
        content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
        content.append("│                     AUTOMATED INTELLIGENCE REPORT                         │")
        content.append("│               Powered by Impact Analytics AI Tracker                       │")
        content.append("└─────────────────────────────────────────────────────────────────────────────┘")
        
        return "\n".join(content)
    
    # Summary section
    content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
    content.append(f"│                    📊 EXECUTIVE SUMMARY: {total_updates} UPDATES FOUND               │")
    content.append("└─────────────────────────────────────────────────────────────────────────────┘")
    content.append("")
    
    # Create summary table
    content.append("📈 UPDATE BREAKDOWN:")
    content.append("─" * 60)
    for source, updates in updates_by_source.items():
        if updates:
            icon = "🔷" if source == "Databricks" else "🔶" if source == "Snowflake" else "🔸"
            content.append(f"   {icon} {source:12} : {len(updates):2d} updates")
    content.append("─" * 60)
    content.append("")
    
    # Detailed updates by source
    for source, updates in updates_by_source.items():
        if not updates:
            continue
            
        # Source header with professional styling
        if source == "Databricks":
            content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
            content.append("│                           🔷 DATABRICKS                                   │")
            content.append("│                    Unified Analytics & Machine Learning                   │")
            content.append("└─────────────────────────────────────────────────────────────────────────────┘")
        elif source == "Snowflake":
            content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
            content.append("│                           🔶 SNOWFLAKE                                    │")
            content.append("│                      Cloud Data Platform                                │")
            content.append("└─────────────────────────────────────────────────────────────────────────────┘")
        else:
            content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
            content.append("│                           🔸 GOOGLE CLOUD                                │")
            content.append("│                      Cloud Infrastructure & AI                           │")
            content.append("└─────────────────────────────────────────────────────────────────────────────┘")
        
        content.append("")
        
        for i, update in enumerate(updates, 1):
            title = update.get('title', 'No title')
            link = update.get('link', '')
            
            # Format title with numbering
            if len(title) > 85:
                title = title[:82] + "..."
            
            content.append(f"   {i}. 📌 {title}")
            
            # Add preview if available
            preview = get_link_preview(link)
            if preview and preview != "No preview available" and preview != "Preview unavailable":
                if len(preview) > 75:
                    preview = preview[:72] + "..."
                content.append(f"      💡 {preview}")
            
            # Format link
            content.append(f"      🔗 {link}")
            content.append("")
        
        content.append("")
    
    # Professional footer
    content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
    content.append("│                        📊 METHODOLOGY                                      │")
    content.append("│   • AI/ML content filtered using advanced keyword analysis                 │")
    content.append("│   • Real-time web scraping from official release channels                  │")
    content.append("│   • Duplicate prevention with intelligent link tracking                   │")
    content.append("│   • Automated summary generation with content preview                      │")
    content.append("└─────────────────────────────────────────────────────────────────────────────┘")
    content.append("")
    
    content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
    content.append("│                    🏢 IMPACT ANALYTICS                                      │")
    content.append("│              Data-Driven Intelligence Solutions                            │")
    content.append("│                                                                             │")
    content.append(f"│              📧 Questions: analytics@impactanalytics.co                     │")
    content.append(f"│              🌐 Website: www.impactanalytics.co                           │")
    content.append("│                                                                             │")
    content.append("│              ⚡ Powered by Advanced AI Technology                         │")
    content.append("│              🔄 Automated Daily Intelligence Reports                      │")
    content.append("└─────────────────────────────────────────────────────────────────────────────┘")
    content.append("")
    
    content.append("┌─────────────────────────────────────────────────────────────────────────────┐")
    content.append("│                     📱 CONNECT WITH US                                     │")
    content.append("│  LinkedIn | Twitter | GitHub | Medium                                     │")
    content.append("│                                                                             │")
    content.append("│              🎯 Transforming Data into Intelligence                        │")
    content.append("└─────────────────────────────────────────────────────────────────────────────┘")
    
    return "\n".join(content)

def send_email(updates_by_source: Dict[str, List[Dict[str, str]]]) -> bool:
    """
    Send premium HTML email with AI/ML updates
    
    Args:
        updates_by_source: Dictionary of updates grouped by source
        
    Returns:
        True if email sent successfully, False otherwise
    """
    return send_html_email(updates_by_source, is_test=False)

def create_test_email() -> bool:
    """
    Send a professional test email to verify configuration
    
    Returns:
        True if test email sent successfully, False otherwise
    """
    return send_html_email({}, is_test=True)
