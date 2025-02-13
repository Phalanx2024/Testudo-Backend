import logging
from patchright.sync_api import sync_playwright
import csv
from datetime import datetime
import time
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.output_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'scraped_data')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def fetch_page(self, url):
        """Fetch the webpage content with error handling and retries."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=False
                    )
                    context = browser.new_context(
                        ignore_https_errors=True,
                        viewport=None
                    )
                    page = context.new_page()
                    page.goto(url)
                    content = page.content()
                    browser.close()
                    return content
            except Exception as e:
                logging.error(f"Error fetching {url}: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)
        return None

    def parse_content(self, page):
        """Parse the page content using Patchright."""
        items = []
        elements = page.query_selector_all('div[data-aid="DOWNLOAD_DOCUMENTS_RENDERED"]')
        
        for element in elements:
            try:
                link_element = element.query_selector('a[data-aid="DOWNLOAD_DOCUMENT_LINK_WRAPPER_RENDERED"]')
                title = link_element.get_attribute('aria-label').replace('Download ', '')
                link = link_element.get_attribute('href')
                date = title.split(' - ')[0]
                
                items.append({
                    'date': date,
                    'title': title,
                    'link': link
                })
            except Exception as e:
                logging.error(f"Error parsing element: {str(e)}")
                continue
                
        return items

    def save_to_csv(self, data, filename):
        """Save the scraped data to a CSV file."""
        if not data:
            logging.warning("No data to save")
            return

        try:
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Data successfully saved to {filepath}")
        except IOError as e:
            logging.error(f"Error saving to CSV: {str(e)}")

    def scrape(self):
        """Main scraping method."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=False
                )
                context = browser.new_context(
                    ignore_https_errors=True,
                    viewport=None
                )
                page = context.new_page()
                
                logging.info(f"Accessing URL: {self.base_url}")
                page.goto(self.base_url)
                
                page.wait_for_load_state('networkidle')
                
                items = self.parse_content(page)
                self.save_to_csv(items, 'culper_reports.csv')
                
                browser.close()
                return items
                
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
            return None

def main():
    base_url = "https://culperresearch.com/latest-research"
    scraper = WebScraper(base_url)
    
    try:
        reports = scraper.scrape()
        if reports:
            print("\nExtracted Reports:")
            for report in reports:
                print(f"\nDate: {report['date']}")
                print(f"Title: {report['title']}")
                print(f"Link: {report['link']}")
    except Exception as e:
        logging.error(f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    main() 