import re
from datetime import datetime
from database.db_controller import DatabaseController
from scrapers.base_scraper import BaseScraper

class SnowcapResearchPDFScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(
            url=url
        )
        self.name = 'Snowcap Research'
        self.db = DatabaseController()

    def extract_reports(self, page):
        try:
            # Get all report sections
            reports = []
            
            # Find all company sections
            company_sections = page.locator('h2').all()
            
            for section in company_sections:
                try:
                    # Get company name and ticker
                    company_text = section.text_content().strip()
                    
                    # Get the presentation link for this company
                    presentation_button = section.locator('xpath=following-sibling::ul//a[contains(text(), "Presentation")]').first
                    if presentation_button:
                        presentation_link = presentation_button.get_attribute('href')
                        if presentation_link and not presentation_link.startswith('http'):
                            presentation_link = f"https://www.snowcapresearch.com{presentation_link}"
                            
                        # Get the date from the list item
                        date_element = presentation_button.locator('xpath=..').text_content()
                        date_match = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})', date_element)
                        date = None
                        if date_match:
                            date = datetime.strptime(date_match.group(1), '%d %B %Y')
                        
                        reports.append({
                            'company': company_text,
                            'presentation_link': presentation_link,
                            'date': date
                        })
                except Exception as e:
                    print(f"Error processing company section: {str(e)}")
                    continue
            
            return reports
        except Exception as e:
            print(f"Error scraping presentation links: {str(e)}")
            return None

    @classmethod
    def _get_short_report(cls):
        db = DatabaseController()
        links = db.get_link_from_short_sellers('Snowcap Research')
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
    test_url = "https://www.snowcapresearch.com/shortcampaigns"
    scraper = SnowcapResearchPDFScraper(test_url)
    
    # Use the scrape method from BaseScraper
    results = scraper.scrape()
    if results:
        print("\nPDF Scraping Results:")
        for result in results:
            print(f"\nCompany: {result['company']}")
            print(f"Date: {result['date']}")
            print(f"Presentation Link: {result['presentation_link']}")
