import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class ViceroyResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://viceroyresearch.org/publications/page/1"
        )
        self.name = 'Viceroy Research'
        self.base_url = "https://viceroyresearch.org/publications/page/"

    def extract_reports(self, page):
        reports = []
        
        try:
            articles = page.query_selector_all('div.col-md-12')
            for article in articles:
                try:
                    link_element = article.query_selector('a')
                    if not link_element:
                        continue
                        
                    title = link_element.text_content().strip()
                    link = link_element.get_attribute('href')
                    date_str = article.query_selector('time').get_attribute('datetime')
                    datetime_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    company = article.query_selector('li a').text_content().strip()
                    
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=link,
                        target_company=company,
                        short_seller=self.name
                    )
                    reports.append(report)
                    
                except Exception as e:
                    logging.error(f"Error processing article: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    reports = ViceroyResearchScraper().scrape()
    print("\nViceroy Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
