import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class UnemonScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.unemon.com/"
        )
        self.name = 'Unemon'
        self.base_url = "https://www.unemon.com"

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all table rows containing reports
            table = page.query_selector('tbody').query_selector('tbody').query_selector('tbody')
            rows = table.query_selector_all('tr')
            
            for row in rows:
                try:
                    # Extract cells from row
                    text_elements = row.text_content().strip().split('\n')
                    date_text = text_elements[0]
                    ticker = text_elements[1]
                    title = text_elements[2]
                    company_name = ticker
                    datetime_obj = datetime.datetime.strptime(date_text, '%Y-%m-%d')
                    # Extract title and link
                    link_element = row.query_selector('a')
                    if not link_element:
                        continue
                        
                    link = link_element.get_attribute('href')
                    if not link.startswith('http'):
                        link = f"{self.base_url}/{link}"

                    
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=link,
                        target_company=company_name,
                        short_seller=self.name,
                        ticker=ticker
                    )
                    reports.append(report)
                    logging.info(f"Found report: {title} ({datetime_obj.date()})")
                    
                except Exception as e:
                    logging.error(f"Error processing row: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = UnemonScraper()
    reports = scraper.scrape()
    print("\nUnemon Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Sentiment: {report.sentiment}")
        print(f"Short Seller: {report.short_seller}") 