import logging
from abc import ABC, abstractmethod
import os
from patchright.sync_api import sync_playwright

class BaseScraper(ABC):
    def __init__(self, url):
        self.url = url
        
    @abstractmethod
    def extract_reports(self, page):
        """
        Extract reports from the page. Must be implemented by child classes.
        Should return a list of dictionaries with 'date', 'title', and 'link' keys.
        """
        pass

    def scrape(self):
        try:
            logging.info("Starting Patchright...")
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                )
                context = browser.new_context(
                    ignore_https_errors=True,
                    viewport=None,
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                )
                page = context.new_page()
                
                # Set longer timeout and add additional wait options
                page.set_default_timeout(60000)  # 60 seconds timeout
                
                logging.info(f"Fetching URL: {self.url}")
                try:
                    # Navigate with custom timeout and wait until network is idle
                    page.goto(self.url, wait_until='networkidle', timeout=60000)
                    
                    # Additional wait for content to be visible
                    page.wait_for_load_state('domcontentloaded')
                    page.wait_for_load_state('networkidle')
                    
                    # Wait a bit more for any dynamic content
                    page.wait_for_timeout(5000)  # 5 second additional wait
                    
                    reports = self.extract_reports(page)
                    return reports
                    
                finally:
                    browser.close()
            
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
            return None