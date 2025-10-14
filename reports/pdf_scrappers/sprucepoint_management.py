import re
from datetime import datetime
from database.db_controller import DatabaseController
from scrapers.base_scraper import BaseScraper

class SprucePointManagementPDFScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(
            url=url
        )
        self.name = 'Spruce Point Management'
        self.db = DatabaseController()

    def extract_reports(self, page):
        try:
            # Find the initial download report button
            download_button = page.locator('a:has-text("Download Report")').first
            if download_button:
                # Wait for the popup window to open when we click the button
                with page.context.expect_page() as popup_info:
                    # Click the button to open the popup
                    download_button.click()
                
                # Get the popup page
                popup_page = popup_info.value
                popup_page.wait_for_load_state('networkidle')
                
                # Find and click the checkbox in the popup to enable the download button
                checkbox = popup_page.locator('input[type="checkbox"]').first
                if checkbox:
                    checkbox.check()
                    
                    # Wait a moment for the download button to become enabled
                    popup_page.wait_for_timeout(1000)
                    
                    # Now find and click the download button in the popup
                    popup_download = popup_page.locator('a:has-text("Download Report")').first
                    if popup_download:
                        # Click the download button which should open a new page or download
                        popup_download.click()
                        
                        # Wait for any navigation or download to complete
                        popup_page.wait_for_load_state('networkidle')
                        
                        # Get the URL from the popup page
                        download_link = popup_page.url
                        
                        # Close the popup
                        popup_page.close()
                        
                        return download_link
            
            return None
        except Exception as e:
            print(f"Error scraping report link: {str(e)}")
            return None

    @classmethod
    def _get_short_report(cls):
        db = DatabaseController()
        links = db.get_link_from_short_sellers('Spruce Point Management')
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
    test_url = "https://www.sprucepointcap.com/research/enfusion-inc"
    scraper = SprucePointManagementPDFScraper(test_url)
    
    # Use the scrape method from BaseScraper
    result = scraper.scrape()
    if result:
        print("\nPDF Scraping Results:")
        print(f"Download Link: {result}")
