import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class SprucepointManagementScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.sprucepointcap.com/research"
        )
        self.name = 'Spruce Point Management'
        self.base_url = "https://www.sprucepointcap.com"

    def extract_reports(self, page):
        reports = []
                # Navigate to each page
        page.wait_for_selector('div.research-list-wrap')
                
        report_elements = page.query_selector_all('div.research-list-wrap')
        for report in report_elements:
            try:
                        # Extract date
                date_str = report.query_selector('div.research-date').text_content().strip()
                datetime_obj = datetime.datetime.strptime(date_str, '%b %d, %Y')
                        
                    # Extract title and company
                company = report.query_selector('a').text_content().strip()
                industry_positions = report.query_selector_all('div.industry-position')
                industry_position = ' '.join([pos.text_content().strip() for pos in industry_positions])
                title = f"{company}{industry_position}"
                        
                        # Extract link
                link = report.query_selector('a').get_attribute('href')
                if not link.startswith('http'):
                    link = f"{self.base_url}{link}"
                    
                report = ResearchReport(
                    source=self.base_url,
                    publication_date=datetime_obj.date(),
                    report_title=title,
                    link=link,
                    target_company=company,
                    short_seller=self.name
                )
                reports.append(report)
                        
            except Exception as e:
                logging.error(f"Error processing report: {e}")
                continue

        return reports

if __name__ == "__main__":
    reports = SprucepointManagementScraper().scrape()
    print("\nSpruce Point Management Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}") 