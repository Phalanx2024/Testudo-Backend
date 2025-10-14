import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class FriendlyBearScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://friendlybearresearch.com/"
        )
        self.name = 'Friendly Bear'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all article elements
            article_elements = page.query_selector_all('article')
            
            for article in article_elements:
                try:
                    # Extract title and link
                    title_element = article.query_selector('h2 a')
                    if not title_element:
                        continue
                    
                    title = title_element.text_content().strip()
                    link = title_element.get_attribute('href')
                    
                    # Extract date from URL or title (format usually includes date)
                    date_match = article.query_selector('a.post-meta-date-link').text_content()
                    
                    datetime_obj = datetime.datetime.strptime(date_match, '%B %d, %Y')
                    
                    # Extract ticker (usually in caps at the start of the post)
                    ticker = date_match = article.query_selector('p').text_content().strip()
                    ticker_element = article.query_selector('.entry-title')

                    # Create report object
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=link,
                        target_company="",  # Company name usually needs to be extracted from the full article
                        short_seller=self.name,
                        ticker=ticker
                    )
                    reports.append(report)
                    
                except Exception as e:
                    logging.error(f"Error processing article: {e}")
            
        except Exception as e:
            logging.error(f"Error processing page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = FriendlyBearScraper()
    reports = scraper.scrape()
    print("\nFriendly Bear Reports:")
    for report in reports:
        print(f"\nDate: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Ticker: {report.ticker}")