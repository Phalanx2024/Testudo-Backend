import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime

class HindenburgResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://hindenburgresearch.com"
        )
        self.name = 'Hindenburg Research'

    def extract_reports(self, page):
        reports = []
        
        try:
            # First get the headline article
            # page.goto(self.url, wait_until='networkidle', timeout=60000)
            # headline = page.query_selector('div.post-heading')
            # if headline:
            #     title = headline.query_selector('h1').text_content()
            #     link = headline.query_selector('a').get_attribute('href')
            #     date_str = headline.query_selector('time').get_attribute('datetime')
            #     datetime_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                
            #     report = ResearchReport(
            #         source=self.url,
            #         publication_date=datetime_obj.date(),
            #         report_title=title,
            #         link=link,
            #         target_company=title.split(':')[0] if ':' in title else title,
            #         short_seller=self.name
            #     )
            #     reports.append(report)
            
            # Then get reports from paginated pages
            try:
                articles = page.query_selector_all('div.post-preview')
                for article in articles:
                    try:
                        title = article.query_selector('h2').text_content().strip()
                        link = article.query_selector('a').get_attribute('href')
                        date_str = article.query_selector('time').get_attribute('datetime')
                        datetime_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        
                        report = ResearchReport(
                            source=self.url,
                            publication_date=datetime_obj.date(),
                            report_title=title,
                            link=link,
                            target_company=title.split(':')[0] if ':' in title else title,
                            short_seller=self.name
                        )
                        reports.append(report)
                            
                    except Exception as e:
                        logging.error(f"Error processing article: {e}")
                            
            except Exception as e:
                logging.error(f"Error processing page {1}: {e}")
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    reports = HindenburgResearchScraper().scrape()
    print("\nHindenburg Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
