import re
from datetime import datetime
from database.db_controller import DatabaseController
from scrapers.base_scraper import BaseScraper

class ViceroyResearchPDFScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(
            url=url
        )
        self.name = 'Viceroy Research'
        self.db = DatabaseController()

    def extract_reports(self, page):
        try:
            # Find the report download link
            download_link = None
            download_button = page.locator('a:has-text("DOWNLOAD")').first
            if download_button:
                download_link = download_button.get_attribute('href', timeout=3000)
                # Get the next link after the text
            return download_link
        except Exception as e:
            print(f"Error scraping report link: {str(e)}")
            return None

    @classmethod
    def _get_short_report(cls):
        db = DatabaseController()
        links = db.get_link_from_short_sellers('Viceroy Research')
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
    test_url = "https://viceroyresearch.org/2025/05/21/arbor-may-2025-clo-update/"
    scraper = ViceroyResearchPDFScraper(test_url)
    
    # Use the scrape method from BaseScraper
    result = scraper.scrape()
    if result:
        print("\nPDF Scraping Results:")
        print(f"Download Link: {result}")
