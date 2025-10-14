import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class WolfpackResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.wolfpackresearch.com/items"
        )
        self.name = 'Wolfpack Research'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all research report sections
            # Based on the website structure, reports appear to be in sections with titles
            report_sections = page.query_selector_all('div[role="listitem"]')
            
            for section in report_sections:
                try:
                    # Get the title text
                    title = section.query_selector('h2').text_content().strip()
    
                    # Find the "Read More" link associated with this section
                    # The link should be near this section
                 
                    read_more_link = section.query_selector('a:has-text("Read More")')
                    if read_more_link:
                        link = read_more_link.get_attribute('href')
                    else:
                        # If no "Read More" link, try to find any link in the section
                        link_element = section.query_selector('a')
                        link = link_element.get_attribute('href') if link_element else None
    
                    
                    # Extract company name and ticker from title
                    sub_title = section.query_selector('p').text_content().strip()
                    company_name = sub_title
                    ticker = ''
                    
                    # Look for ticker in parentheses or after colon
                    if '(' in sub_title and ')' in sub_title:
                        # Extract ticker from parentheses
                        ticker_match = re.search(r'\(([^)]+)\)', sub_title)
                        if ticker_match:
                            ticker = ticker_match.group(1)
                            company_name = title.split('(')[0].strip()
                    elif ':' in title:
                        # Extract ticker after colon
                        parts = title.split(':')
                        if len(parts) > 1:
                            company_name = parts[0].strip()
                            ticker = parts[1].strip()
                    
                    # Try to extract date from the section or nearby elements
                    # Since the website doesn't show dates prominently, we'll use current date
                    # You might need to adjust this based on actual date availability
                    date = datetime.datetime.now().date()
                    
                    # Create the report object
                    report = ResearchReport(
                        source=self.url,
                        publication_date=date,
                        report_title=title,
                        link=link,
                        target_company=ticker,
                        short_seller=self.name,
                        ticker=ticker
                    )
                    reports.append(report)
                        
                except Exception as e:
                    logging.error(f"Error processing report section: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = WolfpackResearchScraper()
    reports = scraper.scrape()
    print("\nWolfpack Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
        print(f"Ticker: {report.ticker}") 