import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime
import re

class SunshineResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://sunshineresearch.substack.com/archive"
        )
        self.name = 'Sunshine Research'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Scroll to load all content
            last_height = page.evaluate('document.documentElement.scrollHeight')
            while True:
                page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
                page.wait_for_timeout(2000)  # Wait for content to load
                new_height = page.evaluate('document.documentElement.scrollHeight')
                if new_height == last_height:
                    break
                last_height = new_height

            # Find all post elements
      
            post_elements = page.query_selector_all('div[class="container-Qnseki"]')
            
            for post in post_elements:
                try:
                    # Extract title
                    title_element = post.query_selector('a')
                    if not title_element:
                        continue
                    title = title_element.text_content().strip()
                    
                    # Skip if not a research report
                    if "Learning from the Legends" in title:
                        continue
                    
                    # Extract link
                    link_element = post.query_selector('a')
                    link = link_element.get_attribute('href') if link_element else self.url
                    
                    # Extract date
                    date_element = post.query_selector('time')
                    if not date_element:
                        continue
                    
                    date_text = date_element.text_content().strip()
                    
                    # Convert month names
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
                        current_year = datetime.datetime.now().year
                        date_text += f', {current_year}'
                    
                    datetime_obj = datetime.datetime.strptime(date_text, '%B %d, %Y')
                    
                    # Extract ticker if present
                    ticker = ""
                    company_name = ""
                    
                    # Look for ticker patterns like "DLX US" or in brackets
                    ticker_match = re.search(r'[A-Z]{2,5}\s*US|\[([A-Z]+)\]', title)
                    if ticker_match:
                        ticker = ticker_match.group(0).replace(' US', '').strip('[]')
                        # Try to extract company name before the ticker
                        company_parts = title.split(ticker_match.group(0))[0].strip(' -–')
                        if company_parts:
                            company_name = company_parts.strip()
                    
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
                    
                except Exception as e:
                    logging.error(f"Error processing post: {e}")
            
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = SunshineResearchScraper()
    reports = scraper.scrape()
    print("\nSunshine Research Reports:")
    for report in reports:
        print(f"\nDate: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
