import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class QCMFundsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.qcmfunds.com/past-qcm-campaigns/"
        )
        self.name = 'Quintessential Capital Management'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Get all elements
            elements = page.query_selector_all('p')
            current_company = ""
            current_ticker = ""
            
            for element in elements:
                try:
                    # Check if this paragraph contains a company name (strong tag)
                    strong = element.query_selector('strong')
                    if strong:
                        company_text = strong.text_content().strip()
                        if company_text and 'Past QCM Campaigns' not in company_text:
                            # Extract ticker if present
                            ticker_match = re.search(r'\(([A-Z]+)\)', company_text)
                            if ticker_match:
                                current_ticker = ticker_match.group(1)
                                current_company = company_text.split('(')[0].strip()
                            else:
                                current_company = company_text
                                current_ticker = ""
                        continue

                    # If we have a current company, look for report links
                    if current_company:
                        links = element.query_selector_all('a')
                        for link in links:
                            try:
                                url = link.get_attribute('href')
                                if not url:
                                    continue
                                
                                link_text = link.text_content().strip()
                                
                                # Try to extract date from the link text
                                date_obj = None
                                date_match = re.search(r'\b\d{4}\b', link_text)
                                if date_match:
                                    year = int(date_match.group(0))
                                    # Use January 1st as default date when only year is available
                                    date_obj = datetime.date(year, 1, 1)
                                else:
                                    # Use current date if no date found
                                    date_obj = datetime.datetime.now().date()
                                
                                report = ResearchReport(
                                    source=self.url,
                                    publication_date=date_obj,
                                    report_title=link_text,
                                    link=url,
                                    target_company=current_company,
                                    short_seller=self.name,
                                    ticker=current_ticker
                                )
                                reports.append(report)
                                
                            except Exception as e:
                                logging.error(f"Error processing link: {e}")
                    
                except Exception as e:
                    logging.error(f"Error processing element: {e}")
            
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = QCMFundsScraper()
    reports = scraper.scrape()
    print("\nQCM Funds Reports:")
    for report in reports:
        print(f"\nDate: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
