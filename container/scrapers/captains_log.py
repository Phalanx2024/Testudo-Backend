import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class CaptainsLogScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.thecaptainslog.io"
        )
        self.name = 'The Captains Log'
        self.base_url = "https://www.thecaptainslog.io"
        self.total_pages = 3  # Adjust based on actual number of pages

    def extract_reports(self, page):
        reports = []
        
        try:
            for page_num in range(1, self.total_pages + 1):
                # Navigate to each page
                if page_num > 1:
                    page.goto(f"{self.base_url}/page/{page_num}/")
                    page.wait_for_load_state('networkidle')
                
                # Find all article elements
                articles = page.query_selector_all('article')
                
                for article in articles:
                    try:
                        # Extract title and link
                        title_element = article.query_selector('h3')
                        if not title_element:
                            continue
                            
                        title = title_element.text_content().strip()
                        link_element = article.query_selector('a')
                        link = link_element.get_attribute('href')
                        if not link.startswith('http'):
                            link = f"{self.base_url}{link}"
                        
                        # Extract date from title or content
                        date_match =article.query_selector('time')
                        date_text = date_match.text_content().strip()
                        # Convert abbreviated month names to full names
                        month_mappings = {
                            'Jan': 'January',
                            'Feb': 'February',
                            'Mar': 'March',
                            'Apr': 'April',
                            'May': 'May',
                            'Jun': 'June',
                            'Jul': 'July',
                            'Aug': 'August',
                            'Sep': 'September',
                            'Oct': 'October',
                            'Nov': 'November',
                            'Dec': 'December'
                        }
                    
                        for abbr, full in month_mappings.items():
                            date_text = date_text.replace(abbr, full)
                        datetime_obj = datetime.datetime.strptime(date_text, '%d %B %Y')
                  
                        # Extract ticker and company name
                        company_name = ""
                        ticker = ""
                        
                        # Look for ticker in parentheses or after colon
                        ticker_match = re.search(r'\((NYSE|NASDAQ):\s*([A-Z]+)\)', title)
                        if ticker_match:
                            ticker = ticker_match.group(2)
                            # Get company name from before the ticker
                            company_parts = title.split('(')[0].strip()
                            company_name = company_parts
                        
                        # If no ticker found in standard format, try other patterns
                        if not ticker:
                            # Try to find standalone ticker
                            ticker_match = re.search(r'([A-Z]{2,5}):', title)
                            if ticker_match:
                                ticker = ticker_match.group(1)
                                company_name = title.split(':')[1].strip().split('(')[0].strip()
                        
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
                        logging.error(f"Error processing article: {e}")
                        continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = CaptainsLogScraper()
    reports = scraper.scrape()
    print("\nThe Captain's Log Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}") 