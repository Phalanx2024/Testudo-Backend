#!/bin/bash

# Set the working directory to the script's location
cd /Users/albertzhang/Workspace/WASP/TESTUDO/Testudo-Backend

# Activate virtual environment (adjust path if needed)
source venv/bin/activate

# Set up logging
LOG_DIR="/Users/albertzhang/Workspace/WASP/TESTUDO/Testudo-Backend/logs"
mkdir -p "$LOG_DIR"

# Create log file with timestamp
LOG_FILE="$LOG_DIR/scraper_$(date +%Y%m%d_%H%M%S).log"

# Run the scraper and log output
echo "Starting scraper at $(date)" >> "$LOG_FILE"
python run_all_scrapers.py >> "$LOG_FILE" 2>&1
echo "Scraper finished at $(date)" >> "$LOG_FILE"

# Also run the database update if needed
echo "Starting database update at $(date)" >> "$LOG_FILE"
python update_database.py >> "$LOG_FILE" 2>&1
echo "Database update finished at $(date)" >> "$LOG_FILE"

# Deactivate virtual environment
deactivate

echo "Daily scraper job completed at $(date)" >> "$LOG_FILE" 