import re
from datetime import datetime
from database.db_controller import DatabaseController
from scrapers.base_scraper import BaseScraper

class BonitasResearchPDFScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(
            url=url
        )
        self.name = 'Bonitas Research'
        self.db = DatabaseController()

    def extract_reports(self, page):
        try:
            # Find the download link using the class selector
            download_link = None
            download_button = page.locator('a.download-link').first
            if download_button:
                # First get the download link
                download_link = download_button.get_attribute('href', timeout=3000)
                
                if download_link:
                    # Navigate to the download page (this will redirect to the PDF)
                    page.goto(download_link)
                    
                    # Wait for the redirect to complete
                    page.wait_for_load_state('networkidle')
                    
                    # Get the final URL after redirect (this will be the PDF URL)
                    final_url = page.url
                    
                    # Check if we got redirected to a PDF
                    download_url = final_url.replace('tos-check/?pdf_id=', '')
                    download_link = f"{download_url}.pdf"
            
            return download_link
        except Exception as e:
            print(f"Error scraping report link: {str(e)}")
            return None

    @classmethod
    def _get_short_report(cls):
        db = DatabaseController()
        links = db.get_link_from_short_sellers('Bonitas Research')
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
    test_url = "https://www.bonitasresearch.com/research/"
    scraper = BonitasResearchPDFScraper(test_url)
    
    # Use the scrape method from BaseScraper
    result = scraper.scrape()
    if result:
        print("\nPDF Scraping Results:")
        print(f"Download Link: {result}")
