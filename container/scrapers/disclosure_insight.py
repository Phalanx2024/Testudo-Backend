import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class DisclosureInsightScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.disclosureinsight.com/archive"
        )
        self.name = 'Disclosure Insight'
        self.base_url = "https://www.disclosureinsight.com"

    def parse_relative_date(self, date_text):
        """Convert relative dates like '1 hr ago' to datetime objects"""
        now = datetime.datetime.now()
        
        if 'hr ago' in date_text or 'hrs ago' in date_text:
            hours = int(date_text.split()[0])
            return now - datetime.timedelta(hours=hours)

    def extract_reports(self, page):
        reports = []
        
        try:
            # The below code is for when the page is not loading all the reports at once -- only to use if want to scrape all reports at once
            # last_height = page.evaluate('document.documentElement.scrollHeight')
            # while True:
            #     page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
            #     page.wait_for_timeout(2000)
            #     new_height = page.evaluate('document.documentElement.scrollHeight')
            #     if new_height == last_height:
            #         break
            #     last_height = new_height
            
            post_elements = page.query_selector_all('div.container-Qnseki')
            
            for post in post_elements:
                try:
                    title_element = post.query_selector('a[data-testid=post-preview-title]')
                    if not title_element:
                        continue
                        
                    title = title_element.text_content().strip()
                    link_element = post.query_selector('a')
                    link = link_element.get_attribute('href') if link_element else None
                    
                    if not link:
                        continue
                    
                    if not link.startswith('http'):
                        link = f"{self.base_url}{link}"
                    
                    # Extract date with relative time handling
                    date_element = post.query_selector('time')
                    if not date_element:
                        continue
                        
                    date_text = date_element.text_content().strip()
                    
                    # Try parsing relative date first
                    datetime_obj = self.parse_relative_date(date_text)
                    
                    # If not a relative date, try standard date format
                    if not datetime_obj:
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
                        
                        if not re.search(r'\d{4}', date_text):
                            date_text += f', {datetime.datetime.now().year}'
                            
                        datetime_obj = datetime.datetime.strptime(date_text, '%B %d, %Y')
                    
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=link,
                        target_company="",
                        short_seller=self.name,
                        ticker=""
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
    scraper = DisclosureInsightScraper()
    reports = scraper.scrape()
    print("\nDisclosure Insight Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}") 