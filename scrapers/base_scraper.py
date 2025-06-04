import logging
from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright

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
                    executable_path="/Users/albertzhang/Library/Caches/ms-playwright/chromium_headless_shell-1155/chrome-mac/headless_shell",
                    headless=True,
                )
                context = browser.new_context(
                    ignore_https_errors=True,
                    viewport=None,
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                )
                page = context.new_page()
                
                page.set_default_timeout(60000)
                
                logging.info(f"Fetching URL: {self.url}")
                try:
                    page.goto(self.url, wait_until='networkidle', timeout=60000)
                    
                    page.wait_for_load_state('domcontentloaded')
                    page.wait_for_load_state('networkidle')
                    
                    # page.wait_for_timeout(5000)
                    
                    reports = self.extract_reports(page)
                    return reports
                    
                finally:
                    browser.close()
            
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
            return None