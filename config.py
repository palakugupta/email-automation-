"""
Configuration settings for AI Release Notes Tracker
"""

# Data sources configuration
SOURCES = {
    "Databricks": "https://docs.databricks.com/en/release-notes/index.html",
    "Snowflake": "https://docs.snowflake.com/en/release-notes",
    "GCP": "https://cloud.google.com/feeds/release-notes.xml"
}

# AI/ML related keywords for filtering
KEYWORDS = [
    "ai", "ml", "machine learning", "genai", "llm", 
    "artificial intelligence", "deep learning", "neural network",
    "tensorflow", "pytorch", "scikit-learn", "pandas",
    "jupyter", "notebook", "model", "training", "inference",
    "prediction", "classification", "regression", "clustering",
    "nlp", "natural language", "computer vision", "cv",
    "reinforcement learning", "gan", "transformer", "bert",
    "gpt", "chatbot", "automation", "mlops", "feature store"
]

# Email configuration
EMAIL_CONFIG = {
    "sender": "palak.gupta@impactanalytics.co",  # Replace with your Gmail
    "password": "boywjoujvydvqccr",    # Replace with your Gmail App Password
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "to": ["palakugupta@gmail.com", "sreeharsha.naik@impactanalytics.co"],   # Replace with recipient emails
    "cc": ["deepa.s@impactanalytics.co"]                           # Optional CC recipients
}

# Application settings
MAX_UPDATES_PER_SOURCE = 5
MAX_TOTAL_UPDATES = 10
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

# File paths
SENT_LINKS_FILE = "sent_links.json"
LOG_FILE = "ai_release_tracker.log"
