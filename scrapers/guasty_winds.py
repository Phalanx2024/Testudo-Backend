import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime
import re

class GuastyWindsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://guastywinds.substack.com/archive"
        )
        self.name = 'Guasty Winds'

    def extract_reports(self, page):
        reports = []
        
        try:
            # The below code is for when the page is not loading all the reports at once -- only to use if want to scrape all reports at once
            # last_height = page.evaluate('document.documentElement.scrollHeight')
            # while True:
            #     page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            #     page.wait_for_timeout(2000)  # Wait for content to load
            #     new_height = page.evaluate('document.documentElement.scrollHeight')
            #     if new_height == last_height:
            #         break
            #     last_height = new_height

            # Find all post elements
            post_elements = page.query_selector_all('div[class="container-Qnseki"]')
            
            for post in post_elements:
                try:
                    # Extract title
                    title_element = post.query_selector('a')
                    if not title_element:
                        continue
                    title = title_element.text_content().strip()
                    
                    # Skip if it's an announcement
                    if 'Announcement:' in title:
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
                    
                    # Extract ticker if present (format: "TICKER-US" or similar)
                    ticker = ""
                    company_name = ""
                    ticker_match = re.search(r'\(([A-Z]+-US)\)', title)
                    if ticker_match:
                        ticker = ticker_match.group(1).split('-')[0]  # Remove the "-US" suffix
                        # Try to extract company name before the ticker
                        company_parts = title.split('(')[0].strip()
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
    scraper = GuastyWindsScraper()
    reports = scraper.scrape()
    print("\nGuasty Winds Reports:")
    for report in reports:
        print(f"\nDate: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
