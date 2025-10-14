import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class BearCaveScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://thebearcave.substack.com/archive"
        )
        self.name = 'The Bear Cave'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Scroll down multiple times to load more content
            # last_height = page.evaluate('document.documentElement.scrollHeight')
            
            # while True:
            #     # Scroll to bottom
            #     page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            #     page.wait_for_timeout(2000)  # Wait for content to load
                
            #     # Calculate new scroll height
            #     new_height = page.evaluate('document.documentElement.scrollHeight')
                
            #     # Break if no more content is loaded
            #     if new_height == last_height:
            #         break
                    
            #     last_height = new_height
            
            # Find all post elements after scrolling
            post_elements = page.query_selector_all('div[class="container-Qnseki"]')
            
            for post in post_elements:
                try:
                    # Extract title
                    title_element = post.query_selector('a')
                    if not title_element:
                        continue
                    title = title_element.text_content().strip()
                    
                    # Skip weekly roundup posts
                    if 'The Bear Cave #' in title:
                        continue
                        
                    # Extract link
                    link_element = post.query_selector('a')
                    link = link_element.get_attribute('href') if link_element else self.url
                    
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
                    current_year = datetime.datetime.now().year
                    if not re.search(r'\d{4}', date_text):  # Check if any 4-digit year is present
                        date_text += f', {current_year}'  # Default to current year
                        
                    datetime_obj = datetime.datetime.strptime(date_text, '%B %d, %Y')
                    
                    # Extract ticker and company name if present (format: "Problems at Company Name (TICKER)")
                    company_name = ""
                    ticker = ""
                    if '(' in title and ')' in title:
                        if "Problems at" in title:
                            company_parts = title.split('Problems at ')[1].split('(')[0].strip()
                            ticker_match = title.split('Problems at ')[1].split('(')[1].split(')')[0].strip()
                            company_name = company_parts
                            ticker = ticker_match
                        else:
                            ticker_match = title.split('(')[1].split(')')[0].strip()
                            company_name = ticker_match
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
                    
                except Exception as e:
                    logging.error(f"Error processing report: {e}")
            
        
                    
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = BearCaveScraper()
    reports = scraper.scrape()
    print("\nThe Bear Cave Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
        print(f"Ticker: {report.ticker}")