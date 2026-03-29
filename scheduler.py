"""
Email Automation Scheduler

This script provides multiple ways to automate the email sending:
1. Windows Task Scheduler integration
2. Python scheduler (runs continuously)
3. Cron-like scheduling
"""

import os
import sys
import time
import logging
import subprocess
from datetime import datetime, timedelta
from schedule import every, run_pending
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_email_script():
    """Run the main email script"""
    try:
        logger.info("Running email automation script...")
        result = subprocess.run([sys.executable, 'main.py'], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            logger.info("Email script executed successfully")
            logger.info(f"Output: {result.stdout}")
        else:
            logger.error(f"Email script failed with return code {result.returncode}")
            logger.error(f"Error: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        logger.error(f"Error running email script: {e}")
        return False

def continuous_scheduler(interval_hours=24):
    """Run the scheduler continuously"""
    logger.info(f"Starting continuous scheduler - running every {interval_hours} hours")
    
    # Schedule the job
    every(interval_hours).hours.do(run_email_script)
    
    # Run once immediately
    logger.info("Running initial email check...")
    run_email_script()
    
    # Keep running
    while True:
        run_pending()
        time.sleep(60)  # Check every minute

def create_task_scheduler_script():
    """Create a batch script for Windows Task Scheduler"""
    batch_content = f"""@echo off
cd /d "{os.path.dirname(os.path.abspath(__file__))}"
python scheduler.py --run-once
"""
    
    with open('run_email.bat', 'w') as f:
        f.write(batch_content)
    
    logger.info("Created run_email.bat for Windows Task Scheduler")
    logger.info("To set up Windows Task Scheduler:")
    logger.info("1. Open Task Scheduler")
    logger.info("2. Create Basic Task")
    logger.info("3. Set trigger to Daily (or your preferred schedule)")
    logger.info("4. Action: Start a program")
    logger.info(f"5. Program: {os.path.abspath('run_email.bat')}")

def main():
    parser = argparse.ArgumentParser(description='Email Automation Scheduler')
    parser.add_argument('--run-once', action='store_true', help='Run email script once and exit')
    parser.add_argument('--continuous', action='store_true', help='Run continuously (default: every 24 hours)')
    parser.add_argument('--interval', type=int, default=24, help='Interval in hours for continuous mode')
    parser.add_argument('--create-task', action='store_true', help='Create batch file for Windows Task Scheduler')
    
    args = parser.parse_args()
    
    if args.create_task:
        create_task_scheduler_script()
        return
    
    if args.run_once:
        logger.info("Running email script once...")
        success = run_email_script()
        sys.exit(0 if success else 1)
    
    if args.continuous:
        continuous_scheduler(args.interval)
    else:
        # Default: show options
        print("Email Automation Scheduler")
        print("Options:")
        print("1. Run once: python scheduler.py --run-once")
        print("2. Continuous mode: python scheduler.py --continuous")
        print("3. Create Windows Task Scheduler: python scheduler.py --create-task")
        print("4. Custom interval: python scheduler.py --continuous --interval 12")

if __name__ == "__main__":
    main()
