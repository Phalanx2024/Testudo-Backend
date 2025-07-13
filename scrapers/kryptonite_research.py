import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime
import re

class KryptoniteResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://kryptoniteresearch.com/ideas/"
        )
        self.name = 'Kryptonite Research'
        self.base_url = "https://kryptoniteresearch.com"

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all report entries
            entries = page.query_selector('ol')
            entries = entries.query_selector_all('li')
            
            for entry in entries:
                try:
                    # Extract title and link
                    title_element = entry.query_selector('a')
                    if not title_element:
                        continue
                        
                    title = title_element.text_content().strip()
                    
                    # Extract date (format: "Written by Kryptonite, 6-11-23")
                    date_text = title.split(",")[-1].strip()
                    date_match = re.search(r'(\d{1,2}-\d{1,2}-\d{2})', date_text)
                    if not date_match:
                        continue
                        
                    # Convert date format
                    date_str = date_match.group(1)
                    try:
                        datetime_obj = datetime.datetime.strptime(date_str, '%m-%d-%y')
                    except ValueError:
                        logging.error(f"Could not parse date: {date_str}")
                        continue
                    
                    # Extract ticker and company name if present
                    ticker = ""
                    company_name = ""
                    if ":" in title:
                        company_parts = title.split(":")[0].strip()
                        company_name = company_parts
                    link = entry.query_selector('a').get_attribute('href')
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=link,  # Using base URL since individual report links aren't visible
                        target_company=company_name,
                        short_seller=self.name,
                        ticker=ticker
                    )
                    reports.append(report)
                    logging.info(f"Found report: {title} ({datetime_obj.date()})")
                    
                except Exception as e:
                    logging.error(f"Error processing entry: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = KryptoniteResearchScraper()
    reports = scraper.scrape()
    print("\nKryptonite Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}") 