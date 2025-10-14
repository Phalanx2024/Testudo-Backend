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
            logging.info("Starting Playwright...")
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-gpu",
                        "--no-sandbox",
                        "--single-process",
                        "--disable-dev-shm-usage",
                        "--no-zygote",
                        "--disable-setuid-sandbox",
                        "--disable-accelerated-2d-canvas",
                        "--no-first-run",
                        "--no-default-browser-check",
                        "--disable-background-networking",
                        "--disable-background-timer-throttling",
                        "--disable-client-side-phishing-detection",
                        "--disable-component-update",
                        "--disable-default-apps",
                        "--disable-domain-reliability",
                        "--disable-features=AudioServiceOutOfProcess",
                        "--disable-hang-monitor",
                        "--disable-ipc-flooding-protection",
                        "--disable-popup-blocking",
                        "--disable-prompt-on-repost",
                        "--disable-renderer-backgrounding",
                        "--disable-sync",
                        "--force-color-profile=srgb",
                        "--metrics-recording-only",
                        "--mute-audio",
                        "--no-pings",
                        "--use-gl=swiftshader",
                        "--window-size=1280,1696",
                        "--disable-extensions",
                        "--disable-plugins",
                        "--disable-images",
                        "--disable-web-security",
                        "--disable-features=VizDisplayCompositor"
                    ]
                )
                context = browser.new_context(
                    ignore_https_errors=True,
                    viewport=None,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                )
                page = context.new_page()
                
                # Set headers
                page.set_extra_http_headers({
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Cache-Control": "max-age=0",
                })
                
                page.set_default_timeout(60000)
                
                logging.info(f"Fetching URL: {self.url}")
                try:
                    page.goto(self.url, wait_until='networkidle', timeout=60000)
                    
                    page.wait_for_load_state('domcontentloaded')
                    page.wait_for_load_state('networkidle')
                    
                    reports = self.extract_reports(page)
                    return reports
                    
                finally:
                    try:
                        page.close()
                    except:
                        pass
                    try:
                        context.close()
                    except:
                        pass
                    try:
                        browser.close()
                    except:
                        pass
            
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
            return None