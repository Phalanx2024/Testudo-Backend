import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class GMTResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.gmtresearch.com/en/library/companies"
        )
        self.name = 'GMT Research'

    def extract_reports(self, page):
        reports = []
       
        table = page.query_selector('table')
        rows = table.query_selector_all('tr')        
        for row in rows:
            try:
                cells = row.query_selector_all('td')
                if not cells:  # Skip header row
                    continue
                            
                # Extract data from cells
                date_str = cells[0].get_attribute('data-title') == 'Year' and cells[0].text_content()
                title = cells[1].get_attribute('data-title') == 'Name' and cells[1].text_content()
                link = cells[1].query_selector('a').get_attribute('href')
                ticker = cells[2].get_attribute('data-title') == 'Ticker' and cells[2].text_content()
                # sector = cells[3].get_attribute('data-title') == 'Sector' and cells[3].text_content()
                last_update_str = cells[4].get_attribute('data-title') == 'Last Updated' and cells[4].text_content()
                        
                # Convert date strings to datetime objects
                pub_date = datetime.datetime.strptime(date_str.strip(), '%b %Y')
                last_update = datetime.datetime.strptime(last_update_str.strip(), '%d %b %Y')
                        
                report = ResearchReport(
                    source=self.url,
                    publication_date=pub_date,
                    report_title=title.strip(),
                    link=link,
                    target_company=ticker.strip(),
                    short_seller=self.name
                    )
                reports.append(report)
                        
            except Exception as e:
                logging.error(f"Error processing row: {e}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = GMTResearchScraper().scrape()
    print("\nGMT Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Sector: {report.sector}")
        print(f"Last Update: {report.last_update}")
        print(f"Short Seller: {report.short_seller}")
