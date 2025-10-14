import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class BonitasResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.bonitasresearch.com/research/"
        )
        self.name = 'Bonitas Research'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find the table with research reports
            report_rows = page.query_selector_all('div.company-grid-row')
            
            for row in report_rows:
                try:
                    title = row.query_selector('div.Company-Name').text_content().strip()
                    if '(' in title and ')' in title:
                        company_name = title.split('(')[0].strip()
                    else:
                        company_name = title.split('-')[0].strip()
                    date = row.query_selector('div.Initiation-Date').text_content().strip()
                    date = datetime.datetime.strptime(date, '%m/%d/%Y')
                    link = row.query_selector('div.Company-Name a').get_attribute('href')
                    if '(' in title and ')' in title:
                        ticker = title.split('(')[1].split(')')[0]
                    else:
                        ticker = ''
                    report = ResearchReport(
                            source=self.url,
                            publication_date=date.date(),
                            report_title=title,
                            link=link,
                            target_company=company_name,
                            short_seller=self.name,
                            ticker=ticker
                        )
                    reports.append(report)
                        
                except Exception as e:
                    logging.error(f"Error processing report row: {e}")
                    
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = BonitasResearchScraper()
    reports = scraper.scrape()
    print("\nBonitas Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
        print(f"Ticker: {report.ticker}")