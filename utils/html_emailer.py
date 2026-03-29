"""
Premium HTML Email Template - Amazon-Style Design
"""

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Tuple
from datetime import datetime
import logging
from config import EMAIL_CONFIG

logger = logging.getLogger(__name__)


def _build_plain_text(updates_by_source: Dict[str, List[Dict[str, str]]], is_test: bool) -> str:
    total_updates = sum(len(updates) for updates in updates_by_source.values())
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    if is_test:
        return "\n".join(
            [
                "Impact Analytics - AI Tracker (System Verification)",
                f"Generated: {now_str}",
                "",
                "Your email configuration is working.",
                "",
                "Next: run the tracker to receive AI/ML release note digests.",
            ]
        )

    if total_updates == 0:
        return "\n".join(
            [
                "Impact Analytics - AI Intelligence Report",
                f"Generated: {now_str}",
                "",
                "No new AI/ML updates found today.",
            ]
        )

    lines = ["Impact Analytics - AI Intelligence Report", f"Generated: {now_str}", ""]
    for source, updates in updates_by_source.items():
        if not updates:
            continue
        lines.append(f"{source}:")
        for u in updates:
            title = (u.get("title") or "").strip()
            link = (u.get("link") or "").strip()
            lines.append(f"- {title}")
            if link:
                lines.append(f"  {link}")
        lines.append("")
    return "\n".join(lines)


def _brand_header_block() -> str:
    # Forward-safe: table cells with inline styles only.
    return (
        "<tr>"
        "  <td style=\"padding:0; background:#ffffff;\">"
        "    <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" style=\"border-collapse:collapse;\">"
        "      <tr>"
        "        <td style=\"height:4px; background:#ff9900; font-size:0; line-height:0;\">&nbsp;</td>"
        "      </tr>"
        "      <tr>"
        "        <td style=\"padding:18px 24px; background:#ffffff;\">"
        "          <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" style=\"border-collapse:collapse;\">"
        "            <tr>"
        "              <td align=\"left\" style=\"font-family:Arial,Helvetica,sans-serif; font-size:18px; font-weight:700; color:#111111;\">"
        "                <div style=\"font-size:20px; font-weight:700; color:#111111;\">🏢 IMPACT ANALYTICS</div>"
        "              </td>"
        "              <td align=\"right\" style=\"font-family:Arial,Helvetica,sans-serif; font-size:12px; color:#6b7280;\">"
        "                AI Release Notes Digest"
        "              </td>"
        "            </tr>"
        "          </table>"
        "        </td>"
        "      </tr>"
        "      <tr>"
        "        <td style=\"height:1px; background:#e5e7eb; font-size:0; line-height:0;\">&nbsp;</td>"
        "      </tr>"
        "    </table>"
        "  </td>"
        "</tr>"
    )


def _cta_button(href: str, label: str) -> str:
    # Table-based button for Outlook/Gmail forwarding. Border radius may be ignored in some clients, but safe.
    return (
        "<table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" align=\"center\" style=\"border-collapse:separate;\">"
        "  <tr>"
        "    <td bgcolor=\"#ff9900\" style=\"border-radius:10px;\">"
        "      <a href=\"{href}\" "
        "         style=\"display:inline-block; font-family:Arial,Helvetica,sans-serif; font-size:16px; "
        "                font-weight:700; color:#111111; text-decoration:none; padding:12px 22px;\">"
        "        {label}"
        "      </a>"
        "    </td>"
        "  </tr>"
        "</table>"
    ).format(href=href, label=label)


def _section_divider() -> str:
    return "<tr><td style=\"height:1px; background:#e5e7eb; font-size:0; line-height:0;\">&nbsp;</td></tr>"


def _escape_html(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _build_updates_html(updates_by_source: Dict[str, List[Dict[str, str]]]) -> str:
    blocks: List[str] = []
    for source, updates in updates_by_source.items():
        if not updates:
            continue

        blocks.append(
            "<tr>"
            "  <td style=\"padding:18px 24px 8px 24px; font-family:Arial,Helvetica,sans-serif;\">"
            f"    <div style=\"font-size:14px; font-weight:800; color:#111111; letter-spacing:0.2px;\">{_escape_html(source)}</div>"
            "    <div style=\"font-size:12px; color:#6b7280; margin-top:2px;\">AI/ML related release notes</div>"
            "  </td>"
            "</tr>"
        )

        for u in updates:
            title = _escape_html((u.get("title") or "").strip())
            link = _escape_html((u.get("link") or "").strip())

            blocks.append(
                "<tr>"
                "  <td style=\"padding:0 24px 12px 24px;\">"
                "    <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" "
                "           style=\"border-collapse:separate; border:1px solid #e5e7eb; border-radius:10px;\">"
                "      <tr>"
                "        <td style=\"padding:14px 14px 12px 14px; font-family:Arial,Helvetica,sans-serif;\">"
                f"          <div style=\"font-size:14px; font-weight:700; color:#111111; line-height:1.35;\">{title}</div>"
                "          <div style=\"height:8px; font-size:0; line-height:0;\">&nbsp;</div>"
                "          <div style=\"font-size:12px; color:#374151;\">"
                f"            <a href=\"{link}\" style=\"color:#0b57d0; text-decoration:none; word-break:break-word;\">{link}</a>"
                "          </div>"
                "        </td>"
                "      </tr>"
                "    </table>"
                "  </td>"
                "</tr>"
            )

    return "".join(blocks)

def create_html_email(updates_by_source: Dict[str, List[Dict[str, str]]], is_test: bool = False) -> str:
    """
    Create a premium HTML email template inspired by Amazon-style emails
    
    Args:
        updates_by_source: Dictionary of updates grouped by source
        is_test: Whether this is a test email
        
    Returns:
        Complete HTML email content
    """
    
    total_updates = sum(len(updates) for updates in updates_by_source.values())
    
    # Dynamic content based on email type
    if is_test:
        subject = "🤖 Impact Analytics - System Verification"
        main_title = "System Verification Complete"
        main_subtitle = "Your AI Intelligence Tracker is operational"
        main_content = """
        <div style="text-align: center; margin: 30px 0;">
            <div style="display: inline-block; background: #00a86b; color: white; padding: 15px 30px; border-radius: 8px; font-weight: 600;">
                ✓ SYSTEM ACTIVE
            </div>
        </div>
        <p style="font-size: 16px; line-height: 1.6; margin: 20px 0;">
            Your <strong>AI Release Notes Tracker</strong> has been successfully configured and is now monitoring 
            Databricks, Snowflake, and Google Cloud Platform for the latest AI/ML updates.
        </p>
        <p style="font-size: 16px; line-height: 1.6; margin: 20px 0;">
            You'll receive daily intelligence reports with actionable insights, executive summaries, and direct links 
            to the latest technology developments.
        </p>
        """
        cta_text = "View Documentation"
        cta_link = "https://www.impactanalytics.co"
    else:
        if total_updates == 0:
            subject = "🤖 AI Intelligence Report - No New Updates"
            main_title = "No New Updates Today"
            main_subtitle = "All systems monitoring normally"
            main_content = """
            <p style="font-size: 16px; line-height: 1.6; margin: 20px 0;">
                Our AI monitoring system has scanned all sources today and found no new AI/ML related updates. 
                This is normal - updates will appear as they become available.
            </p>
            <p style="font-size: 16px; line-height: 1.6; margin: 20px 0;">
                The system continues to monitor:
            </p>
            <ul style="font-size: 16px; line-height: 1.6; margin: 20px 0; padding-left: 20px;">
                <li style="margin: 10px 0;"><strong>Databricks Platform</strong> - AI/ML features</li>
                <li style="margin: 10px 0;"><strong>Snowflake Cloud</strong> - Analytics enhancements</li>
                <li style="margin: 10px 0;"><strong>Google Cloud</strong> - AI infrastructure</li>
            </ul>
            """
            cta_text = "View Dashboard"
            cta_link = "https://www.impactanalytics.co"
        else:
            subject = f"📊 AI Intelligence Report - {total_updates} New Updates"
            main_title = f"{total_updates} New Updates Found"
            main_subtitle = "Latest AI/ML Technology Intelligence"
            
            # Build updates content
            main_content = "<div style='margin: 20px 0;'>"
            for source, updates in updates_by_source.items():
                if not updates:
                    continue
                    
                icon = "🔷" if source == "Databricks" else "🔶" if source == "Snowflake" else "🔸"
                source_desc = {
                    "Databricks": "Unified Analytics & Machine Learning",
                    "Snowflake": "Cloud Data Platform", 
                    "GCP": "Cloud Infrastructure & AI"
                }.get(source, "Platform")
                
                main_content += f"""
                <div style="margin: 25px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #e9ecef;">
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <span style="font-size: 24px; margin-right: 10px;">{icon}</span>
                        <div>
                            <h3 style="margin: 0; font-size: 18px; color: #2c3e50;">{source}</h3>
                            <p style="margin: 5px 0 0 0; font-size: 14px; color: #6c757d;">{source_desc}</p>
                        </div>
                    </div>
                    <div style="margin-left: 34px;">
                """
                
                for i, update in enumerate(updates, 1):
                    title = update.get('title', 'No title')
                    link = update.get('link', '')
                    
                    if len(title) > 80:
                        title = title[:77] + "..."
                        
                    main_content += f"""
                        <div style="margin: 15px 0; padding: 15px; background: white; border-radius: 6px; border: 1px solid #e9ecef;">
                            <div style="display: flex; align-items: flex-start; margin-bottom: 8px;">
                                <span style="background: #007bff; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; min-width: 20px; text-align: center; margin-right: 10px;">
                                    {i}
                                </span>
                                <div style="flex: 1;">
                                    <h4 style="margin: 0; font-size: 16px; color: #2c3e50; line-height: 1.4;">{title}</h4>
                                </div>
                            </div>
                            <div style="text-align: center; margin-top: 12px;">
                                <a href="{link}" style="display: inline-block; background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: 500; font-size: 14px;">
                                    View Details →
                                </a>
                            </div>
                        </div>
                    """
                
                main_content += "</div></div>"
            main_content += "</div>"
            
            cta_text = "View All Updates"
            cta_link = "#"
    
    # Forward-safe HTML: table-based layout + inline styles only.
    # Avoids reliance on <style> which forwarding often strips.
    preheader = _escape_html(
        "Your daily AI/ML release note digest from Databricks, Snowflake, and Google Cloud."
        if not is_test
        else "System verification: your email setup is working."
    )

    if (not is_test) and total_updates > 0:
        updates_html = _build_updates_html(updates_by_source)
    else:
        updates_html = ""

    cta_html = _cta_button(cta_link, cta_text)

    html_template = f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\" />
    <title>{_escape_html(subject)}</title>
  </head>
  <body style=\"margin:0; padding:0; background:#f3f4f6;\">
    <div style=\"display:none; font-size:1px; color:#f3f4f6; line-height:1px; max-height:0px; max-width:0px; opacity:0; overflow:hidden;\">{preheader}</div>

    <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" style=\"border-collapse:collapse; background:#f3f4f6;\">
      <tr>
        <td align=\"center\" style=\"padding:24px 12px;\">
          <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" width=\"600\" style=\"width:100%; max-width:600px; border-collapse:collapse; background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; overflow:hidden;\">
            {_brand_header_block()}

            <tr>
              <td style="padding:22px 24px 6px 24px; font-family:Arial,Helvetica,sans-serif;">
                <div style="font-size:16px; color:#111111;">Hi,</div>
                <div style="height:10px; font-size:0; line-height:0;">&nbsp;</div>
                <div style="font-size:14px; color:#374151;">Here's your latest AI/ML release notes digest.</div>
              </td>
            </tr>

            <tr>
              <td style=\"padding:16px 24px 6px 24px; font-family:Arial,Helvetica,sans-serif;\">
                <div style=\"font-size:22px; font-weight:800; color:#111111; line-height:1.25;\">{_escape_html(main_title)}</div>
                <div style=\"height:6px; font-size:0; line-height:0;\">&nbsp;</div>
                <div style=\"font-size:14px; color:#6b7280;\">{_escape_html(main_subtitle)}</div>
              </td>
            </tr>

            <tr>
              <td style=\"padding:4px 24px 10px 24px; font-family:Arial,Helvetica,sans-serif; font-size:12px; color:#6b7280;\">
                Generated on <strong style=\"color:#111111;\">{datetime.now().strftime('%B %d, %Y')}</strong>
              </td>
            </tr>

            {_section_divider()}

            <tr>
              <td style=\"padding:18px 24px 10px 24px; font-family:Arial,Helvetica,sans-serif;\">
                <div style=\"font-size:14px; color:#111111;\">{main_content}</div>
              </td>
            </tr>

            {updates_html}

            <tr>
              <td style=\"padding:18px 24px 22px 24px;\">{cta_html}</td>
            </tr>

            {_section_divider()}

            <tr>
              <td style=\"padding:18px 24px 22px 24px; font-family:Arial,Helvetica,sans-serif;\">
                <div style=\"font-size:12px; color:#6b7280; line-height:1.6;\">
                  <strong style=\"color:#111111;\">Impact Analytics</strong><br/>
                  Contact: analytics@impactanalytics.co<br/>
                  Website: www.impactanalytics.co
                </div>
                <div style=\"height:10px; font-size:0; line-height:0;\">&nbsp;</div>
                <div style=\"font-size:11px; color:#9ca3af; line-height:1.6;\">
                  You’re receiving this email because you opted in to technology intelligence updates. If this was forwarded to you, you can ignore this message.
                </div>
              </td>
            </tr>
          </table>

          <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" width=\"600\" style=\"width:100%; max-width:600px; border-collapse:collapse;\">
            <tr>
              <td align=\"center\" style=\"padding:14px 6px 0 6px; font-family:Arial,Helvetica,sans-serif; font-size:11px; color:#9ca3af;\">
                © {datetime.now().strftime('%Y')} Impact Analytics. All rights reserved.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""
    
    return html_template

def send_html_email(updates_by_source: Dict[str, List[Dict[str, str]]], is_test: bool = False) -> bool:
    """
    Send premium HTML email
    
    Args:
        updates_by_source: Dictionary of updates grouped by source
        is_test: Whether this is a test email
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = ', '.join(EMAIL_CONFIG['to'])
        
        if EMAIL_CONFIG['cc']:
            msg['Cc'] = ', '.join(EMAIL_CONFIG['cc'])
        
        # Create HTML content
        html_content = create_html_email(updates_by_source, is_test)
        
        # Determine subject
        total_updates = sum(len(updates) for updates in updates_by_source.values())
        if is_test:
            subject = "🤖 Impact Analytics - System Verification"
        elif total_updates == 0:
            subject = "🤖 AI Intelligence Report - No New Updates"
        else:
            subject = f"📊 AI Intelligence Report - {total_updates} New Updates"
        
        msg['Subject'] = subject
        
        # Attach plain-text + HTML (alternative). Forwarding clients often prefer one.
        text_content = _build_plain_text(updates_by_source, is_test=is_test)
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # Send email
        import smtplib
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            
            all_recipients = EMAIL_CONFIG['to'] + EMAIL_CONFIG['cc']
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG['sender'], all_recipients, text)
        
        logger.info(f"Premium HTML email sent successfully to {len(all_recipients)} recipients")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send HTML email: {e}")
        return False
