import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime
import re

class DirtyBubbleMediaScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.dirtybubblemedia.com/archive"
        )
        self.name = 'Dirty Bubble Media'

    def extract_reports(self, page):
        reports = []
        
        try:

            last_height = page.evaluate('document.documentElement.scrollHeight')
            
            while True:
                # Scroll to bottom
                page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
                page.wait_for_timeout(2000)  # Wait for content to load
                
                # Calculate new scroll height
                new_height = page.evaluate('document.documentElement.scrollHeight')
                
                # Break if no more content is loaded
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
                    
                    # Extract link
                    link_element = post.query_selector('a')
                    link = link_element.get_attribute('href') if link_element else self.url
                    
                    # Extract date (format: "MMM DD, YYYY")
                    date_element = post.query_selector('time')
                    if date_element:
                        date_str = date_element.text_content().strip()
                        # Convert month abbreviation to full name
                        date_str = date_str.replace('Jan', 'January').replace('Feb', 'February')\
                                         .replace('Mar', 'March').replace('Apr', 'April')\
                                         .replace('Aug', 'August').replace('Sep', 'September')\
                                         .replace('Oct', 'October').replace('Nov', 'November')\
                                         .replace('Dec', 'December')
                        datetime_obj = datetime.datetime.strptime(date_str, '%B %d, %Y')
                    else:
                        continue
                    
                    # Extract company name from title if possible
                    company_match = ''
                    company_name = ''
                    
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=link,
                        target_company=company_name,
                        short_seller=self.name
                    )
                    reports.append(report)
                    
                except Exception as e:
                    logging.error(f"Error processing report: {e}")
            
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = DirtyBubbleMediaScraper()
    reports = scraper.scrape()
    print("\nDirty Bubble Media Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")