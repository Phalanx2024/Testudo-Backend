import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class FiatLuxPartnersScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://fiatluxpartners.com/reports"
        )
        self.name = 'Fiat Lux Partners'
        self.base_url = "https://fiatluxpartners.com"

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all report sections
            titles = page.query_selector_all('div.text-box')
            for i, section in enumerate(titles):
                try:
                    # Get date
                    date_element = section.query_selector('h3')
                    if not date_element:
                        continue
                        
                    date_text = date_element.text_content().strip()
                    try:
                        datetime_obj = datetime.datetime.strptime(date_text, '%B %d, %Y')
                    except ValueError:
                        logging.error(f"Could not parse date: {date_text}")
                        continue
                    title_element = section.query_selector('h1')
                    title = title_element.text_content().strip()
                    
                    # Extract ticker if present
                    ticker = ""
                    company_name = ""
                    ticker_match = re.search(r'\(((?:NYSE|TSX):\s*([A-Z]+))\)', title)
                    if ticker_match:
                        ticker = ticker_match.group(2)
                        company_name = title.split('(')[0].strip()
                    
                    # Get link
                    link =  self.url
                    
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
                    logging.error(f"Error processing section: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = FiatLuxPartnersScraper()
    reports = scraper.scrape()
    print("\nFiat Lux Partners Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}") 