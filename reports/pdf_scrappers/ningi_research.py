import re
from datetime import datetime
from scrapers.base_scraper import BaseScraper

class NingiResearchPDFScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(
            url=url
        )
    
    def get_pdf_link(self, page):
        try:
            # Get the page content
            content = page.content()
            
            # Find the download link using page.locator
            download_link = None
            download_button = page.locator('a:has-text("Download")').first
            if download_button:
                download_link = download_button.get_attribute('href')
                if download_link and not download_link.startswith('http'):
                    download_link = f"https://ningiresearch.com{download_link}"
            return download_link
        except Exception as e:
            print(f"Error scraping PDF link: {str(e)}")
            return None

if __name__ == "__main__":
    # Test the scraper
    test_url = "https://ningiresearch.com/2025/03/26/vita-coco-nasdaq-coco-structural-issues-amid-stalling-sales-and-costco-contract-loss/"
    scraper = NingiResearchPDFScraper(test_url)
    
    # Use the scrape method from BaseScraper
    result = scraper.get_pdf_link(scraper.page)
    if result:
        print("\nPDF Scraping Results:")
        print(f"Title: {result['title']}")
        print(f"Date: {result['date']}")
        print(f"Company: {result['company']}")
        print(f"Ticker: {result['ticker']}")
        print(f"PDF URL: {result['pdf_url']}")