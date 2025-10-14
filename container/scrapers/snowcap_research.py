import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class SnowcapResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.snowcapresearch.com/shortcampaigns"
        )
        self.name = 'Snowcap Research'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all report sections (each company report)
            report_elements = page.query_selector_all('h2')
            
            for report_element in report_elements:
                try:
                    # Extract title and company info
                    title_text = report_element.text_content().strip()
                    
                    # Extract company name and ticker if present
                    # Pattern matches "Company Name (EXCHANGE:TICKER)" or "Company Name"
                    company_match = re.match(r'^([^(]+)(?:\s*\(([^)]+)\))?', title_text)
                    ticker_info = ''
                    if company_match:
                        company_name = company_match.group(1).strip()
                        ticker_info = company_match.group(2) if company_match.group(2) else ""
                    
                    # Get the list item containing date
                    date_element = report_element.query_selector('+ ul li')
                    if date_element:
                        # Extract date from format "Presentation - DD Month YYYY"
                        date_text = date_element.text_content().strip()
                        date_match = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})', date_text)
                        if date_match:
                            date_str = date_match.group(1)
                            datetime_obj = datetime.datetime.strptime(date_str, '%d %B %Y')
                            
                            report = ResearchReport(
                                source=self.url,
                                publication_date=datetime_obj,
                                report_title=f"Snowcap Research Report: {company_name}",
                                link=self.url,
                                target_company=company_name,
                                short_seller=self.name,
                                ticker=ticker_info
                            )
                            reports.append(report)
                
                except Exception as e:
                    logging.error(f"Error processing report: {e}")
                    
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = SnowcapResearchScraper()
    reports = scraper.scrape()
    print("\nSnowcap Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
