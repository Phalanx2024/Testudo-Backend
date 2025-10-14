import re
from datetime import datetime
from database.db_controller import DatabaseController
from scrapers.base_scraper import BaseScraper

class PresciencePointPDFScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(
            url=url
        )
        self.name = 'Prescience Point'
        self.db = DatabaseController()

    def extract_reports(self, page):
        try:
            # Find the download report link
            download_link = None
            download_button = page.locator('a:has-text("Download Report")').first
            if download_button:
                download_link = download_button.get_attribute('href', timeout=3000)
                
                # If it's a relative URL, make it absolute
                if download_link and not download_link.startswith('http'):
                    download_link = f"https://www.presciencepoint.com{download_link}"
            
            return download_link
        except Exception as e:
            print(f"Error scraping report link: {str(e)}")
            return None

    @classmethod
    def _get_short_report(cls):
        db = DatabaseController()
        links = db.get_link_from_short_sellers('Prescience Point')
        short_reports_list = []
        for link in links:
            report_details = {
                'report_name': link[2],
                'report_link': link[4]
            }
            short_reports_list.append(report_details)
        return short_reports_list

if __name__ == "__main__":
    # Test the scraper
    test_url = "https://www.presciencepoint.com/research/research-archives/aersale-update2/"
    scraper = PresciencePointPDFScraper(test_url)
    
    # Use the scrape method from BaseScraper
    result = scraper.scrape()
    if result:
        print("\nPDF Scraping Results:")
        print(f"Download Link: {result}")
    else:
        print("\nNo download link found") 