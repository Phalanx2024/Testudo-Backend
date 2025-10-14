import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime
import re

class SafkhetCapitalScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://safkhetcapital.com/market-advocacy"
        )
        self.name = 'Safkhet Capital'
        self.base_url = "https://safkhetcapital.com"

    def extract_date(self, text):
        """Extract date from text using various patterns"""
        # Try different date patterns
        patterns = [
            (r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', '%d/%m/%Y'),
            (r'(\w+ \d{1,2},? \d{4})', '%B %d, %Y'),
            (r'(\d{1,2}\w{2} \w+ \d{4})', '%d %B %Y'),
        ]
        
        for pattern, date_format in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date_str = match.group(1)
                    return datetime.datetime.strptime(date_str, date_format)
                except ValueError:
                    continue
        
        return None

    def extract_reports(self, page):
        reports = []
        
        try:

            # Get all grid cells
            cells = page.query_selector_all('p[data-ux="Text"]')
            links = page.query_selector_all('a[data-ux-btn="primary"]')
            
            for i, cell in enumerate(cells):
                try:
                    # Get all text content to search for dates
                    title = cell.text_content()
                    
                    # Extract date
                    date = self.extract_date(title)
                    if not date:
                        pass
                    
                    # Extract title and link
                    link_element = links[i]
                    if link_element:
                        link = link_element.get_attribute('href')
                        if not link.startswith('http'):
                            link = f"{self.base_url}{link}"
                    else:
                        link = self.base_url
                    
         
                    report = ResearchReport(
                        source=self.base_url,
                        publication_date=date.date(),
                        report_title=title,
                        link=link,
                        target_company=None,
                        short_seller=self.name
                    )
                    reports.append(report)
                    logging.info(f"Found report: {title} ({date.date()})")
                    
                except Exception as e:
                    logging.error(f"Error processing grid cell: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    reports = SafkhetCapitalScraper().scrape()
    print("\nSafkhet Capital Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
