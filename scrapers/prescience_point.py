import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime
import re

class PresciencePointScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.presciencepoint.com/research/research-archive/page/1/"
        )
        self.name = 'Prescience Point'
        self.base_url = "https://www.presciencepoint.com/research/research-archive/page/"

    def extract_reports(self, page):
        reports = []
        
        try:
            # Scrape all pages (1 through 5)
            for page_num in range(1, 6):
                current_url = f"{self.base_url}{page_num}/"
                logging.info(f"Scraping page {page_num}: {current_url}")
                
                # Navigate to the page
    
                
                # Find all report elements on current page
                report_elements = page.query_selector_all('div.box')
                
                for report in report_elements:
                    try:
                        # Extract title and ticker
                        title_element = report.query_selector('h3')
                        if not title_element:
                            continue
                            
                        title_text = title_element.text_content().strip()
                        
                        # Extract ticker (format: "Company Name | TICKER")
                        ticker_match = re.search(r'\|\s*([A-Z]+)', title_text)
                        ticker = ticker_match.group(1) if ticker_match else ""
                        
                        # Extract company name
                        company_name = ""
                        if ticker:
                            company_parts = title_text.split('|')[0].strip()
                            company_name = company_parts
                        
                        # Extract link
                        link_element = report.query_selector('a')
                        link = link_element.get_attribute('href') if link_element else self.url
                        
                        # Extract date
                        date_element = report.query_selector('h6')
                        if not date_element:
                            continue
                            
                        date_text = date_element.text_content().strip()
                        datetime_obj = datetime.datetime.strptime(date_text, '%B %d, %Y')
                        
                        # Extract description
                        # desc_element = report.query_selector('p')
                        # description = desc_element.text_content().strip() if desc_element else ""
                        
                        # Combine title with description if available
                        # full_title = f"{title_text} - {description}" if description else title_text
                        
                        report = ResearchReport(
                            source=self.url,
                            publication_date=datetime_obj.date(),
                            report_title=title_text,
                            link=link,
                            target_company=company_name,
                            short_seller=self.name,
                            ticker=ticker
                        )
                        reports.append(report)
                        
                    except Exception as e:
                        logging.error(f"Error processing report: {e}")
                
                # Add a small delay between pages
                page.wait_for_timeout(2000)
            
        except Exception as e:
            logging.error(f"Error processing pages: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = PresciencePointScraper()
    reports = scraper.scrape()
    print("\nPrescience Point Reports:")
    for report in reports:
        print(f"\nDate: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}") 