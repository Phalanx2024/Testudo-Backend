import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class OutliersResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://outliers.substack.com/archive"
        )
        self.name = 'Outliers Research'
        self.base_url = "https://outliers.substack.com"

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all post elements (using Substack's container class)
            post_elements = page.query_selector_all('div.container-Qnseki')
            
            for post in post_elements:
                try:
                    # Extract title and link
                    title_element =  post.query_selector('a[data-testid=post-preview-title]')
                    if not title_element:
                        continue
                        
                    title = title_element.text_content().strip()
                    link_element = post.query_selector('a')
                    link = link_element.get_attribute('href') if link_element else None
                    
                    if not link:
                        continue
                    
                    if not link.startswith('http'):
                        link = f"{self.base_url}{link}"
                    
                    # Extract date
                    date_element = post.query_selector('time')
                    if not date_element:
                        continue
                        
                    date_text = date_element.text_content().strip()
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
                    
                    # Add year if not present
                    if not re.search(r'\d{4}', date_text):
                        date_text += f', {datetime.datetime.now().year}'
                        
                    datetime_obj = datetime.datetime.strptime(date_text, '%B %d, %Y')
                    
                    # Extract company name if present in title (e.g., "Company Name (TICKER)")
                    company_name = ""
                    ticker = ""
                    if '(' in title and ')' in title:
                        company_parts = title.split('(')[0].strip()
                        ticker_match = title.split('(')[1].split(')')[0].strip()
                        company_name = company_parts
                        ticker = ticker_match
                    
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
                    logging.error(f"Error processing report: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = OutliersResearchScraper()
    reports = scraper.scrape()
    print("\nOutliers Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
        print(f"Ticker: {report.ticker}") 