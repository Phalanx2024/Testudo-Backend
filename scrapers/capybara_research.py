import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime
import re

class CapybaraResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://capybararesearch.com/"
        )
        self.name = 'Capybara Research'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all article sections
            article_elements = page.query_selector_all('div[class="relative w-100 mb4"]')
        
            for article in article_elements:
                try:
                    # Extract title
                    title_element = article.query_selector('a')
                    if not title_element:
                        continue
                    title = article.query_selector('h1').text_content().strip()
                    link = title_element.get_attribute('href') if title_element else self.url
                    
                    # Extract date
                    date_element = article.query_selector('time')
                    
                    date_str = date_element.get_attribute('datetime')
                    datetime_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
             
                    
                    # Extract ticker and company info from the content
                    ticker = article.query_selector('div[class="f5 fw5 mt2 mb3 gray"]').text_content().strip()
                    company_name = ticker
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=self.url+link,
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
    scraper = CapybaraResearchScraper()
    reports = scraper.scrape()
    print("\nCapybara Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
        print(f"Ticker: {report.ticker}")
        print(f"Exchange: {report.exchange}")