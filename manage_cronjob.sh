#!/bin/bash

# Script to manage the daily scraper cronjob

case "$1" in
    "install")
        echo "Installing daily scraper cronjob (runs at 12:00 PM daily)..."
        echo "0 12 * * * /Users/albertzhang/Workspace/WASP/TESTUDO/Testudo-Backend/run_scrapers_daily.sh" | crontab -
        echo "Cronjob installed successfully!"
        echo "Current crontab:"
        crontab -l
        ;;
    "remove")
        echo "Removing daily scraper cronjob..."
        crontab -r
        echo "Cronjob removed successfully!"
        ;;
    "status")
        echo "Current crontab:"
        crontab -l
        ;;
    "test")
        echo "Testing the scraper script..."
        ./run_scrapers_daily.sh
        echo "Test completed. Check logs/ directory for output."
        ;;
    *)
        echo "Usage: $0 {install|remove|status|test}"
        echo "  install - Install the daily cronjob"
        echo "  remove  - Remove all cronjobs"
        echo "  status  - Show current crontab"
        echo "  test    - Test the scraper script"
        exit 1
        ;;
esac 