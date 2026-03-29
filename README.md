# AI Release Notes Tracker

A production-ready Python automation tool that tracks AI-related release updates from Databricks, Snowflake, and Google Cloud Platform and sends a daily email digest.

## Features

- Fetches latest release notes from public sources
- Filters only AI/ML-related updates using comprehensive keywords
- Avoids duplicates by tracking previously sent links
- Sends clean, formatted email digests
- Production-ready with error handling and logging
- Configurable via simple config file

## Project Structure

```
project/
│── main.py                 # Main orchestrator
│── config.py              # Configuration settings
│── requirements.txt       # Python dependencies
│── README.md              # This file
│── sent_links.json        # Stores previously sent links (auto-created)
│── ai_release_tracker.log # Log file (auto-created)
│── fetchers/              # Data fetching modules
│     ├── __init__.py
│     ├── databricks.py    # Databricks release notes fetcher
│     ├── snowflake.py     # Snowflake release notes fetcher
│     └── gcp.py           # GCP RSS feed fetcher
│── utils/                 # Utility modules
│     ├── __init__.py
│     ├── filter.py        # AI/ML content filtering
│     ├── storage.py       # Sent links management
│     └── emailer.py       # Email functionality
```

## Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, you need to configure your email settings in `config.py`:

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
3. **Update `config.py`:**
   ```python
   EMAIL_CONFIG = {
       "sender": "your-email@gmail.com",        # Your Gmail
       "password": "your-app-password",          # App password (not regular password)
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "to": ["recipient@example.com"],         # Recipient emails
       "cc": []                                 # Optional CC recipients
   }
   ```

### Other Email Providers

Update `EMAIL_CONFIG` in `config.py` with your provider's SMTP settings.

## Usage

### Basic Usage

Run the tracker to fetch and send updates:
```bash
python main.py
```

### Test Email Configuration

Send a test email to verify your setup:
```bash
python main.py --test
```

### Dry Run

See what updates would be sent without actually sending an email:
```bash
python main.py --dry-run
```

## Scheduling

Set up a cron job to run daily:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * /usr/bin/python3 /path/to/your/project/main.py
```

## Configuration Options

### Sources and Keywords

Edit `config.py` to customize:
- **Sources:** Add or modify data source URLs
- **Keywords:** Add AI/ML related keywords for filtering
- **Limits:** Adjust maximum updates per source and total

### Email Settings

- **Sender:** Your email address
- **Recipients:** TO and CC email lists
- **SMTP:** Server settings for your email provider

### Application Settings

- **MAX_UPDATES_PER_SOURCE:** Maximum updates to include from each source (default: 5)
- **MAX_TOTAL_UPDATES:** Maximum total updates per email (default: 10)
- **REQUEST_TIMEOUT:** HTTP request timeout in seconds (default: 30)
- **RETRY_ATTEMPTS:** Number of retry attempts for failed requests (default: 3)

## How It Works

1. **Fetch Data:** Scrapes Databricks and Snowflake websites, parses GCP RSS feed
2. **Filter Content:** Uses AI/ML keywords to filter relevant updates
3. **Remove Duplicates:** Checks against previously sent links stored in `sent_links.json`
4. **Send Email:** Formats and sends a clean email digest
5. **Update Storage:** Saves newly sent links to avoid duplicates

## Data Sources

- **Databricks:** https://docs.databricks.com/en/release-notes/index.html
- **Snowflake:** https://docs.snowflake.com/en/release-notes  
- **GCP:** https://cloud.google.com/feeds/release-notes.xml

## AI/ML Keywords

The tool filters updates using these keywords:
`ai`, `ml`, `machine learning`, `genai`, `llm`, `artificial intelligence`, `deep learning`, `neural network`, `tensorflow`, `pytorch`, `scikit-learn`, `pandas`, `jupyter`, `notebook`, `model`, `training`, `inference`, `prediction`, `classification`, `regression`, `clustering`, `nlp`, `natural language`, `computer vision`, `cv`, `reinforcement learning`, `gan`, `transformer`, `bert`, `gpt`, `chatbot`, `automation`, `mlops`, `feature store`

## Logging

The application logs to:
- Console output
- `ai_release_tracker.log` file

Log levels include:
- **INFO:** Normal operation
- **WARNING:** Non-critical issues
- **ERROR:** Critical errors

## Error Handling

- **Network Issues:** Automatic retry with exponential backoff
- **Parsing Errors:** Graceful degradation, continues with other sources
- **Email Failures:** Won't update sent links if email fails
- **File I/O:** Handles missing files gracefully

## Troubleshooting

### Common Issues

1. **Email Not Sending:**
   - Check Gmail App Password setup
   - Verify SMTP settings in config
   - Run `python main.py --test` to diagnose

2. **No Updates Found:**
   - Check log file for scraping errors
   - Verify source URLs are accessible
   - Try `--dry-run` to see what's being fetched

3. **Permission Errors:**
   - Ensure write permissions for log and JSON files
   - Check Python path in cron job

### Debug Mode

Enable detailed logging by modifying `setup_logging()` in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Security Notes

- **Never commit real passwords** to version control
- **Use App Passwords** instead of regular passwords for Gmail
- **Consider environment variables** for sensitive config in production
- **Regularly rotate** email passwords

## Contributing

To add new data sources:

1. Create a new fetcher in `fetchers/` directory
2. Follow the existing pattern: return list of `{"title": "...", "link": "..."}` dictionaries
3. Import and call the fetcher in `main.py`
4. Add source URL and name to `config.py`

## License

This project is provided as-is for educational and production use.

## Support

For issues or questions:
1. Check the log file: `ai_release_tracker.log`
2. Run with `--dry-run` to debug
3. Verify configuration in `config.py`
4. Test email with `--test` flag
