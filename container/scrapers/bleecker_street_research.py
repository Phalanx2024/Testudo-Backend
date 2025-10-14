import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime

class BleeckerStreetResearchScraper(BaseScraper):
    def __init__(self):
        self.url = 'https://www.bleeckerstreetresearch.com/research'
        self.base_url = 'https://www.bleeckerstreetresearch.com'
        self.name = 'Bleecker Street Research'
        
    def extract_reports(self, page):    
        report_elements = page.query_selector_all('div.blog-item-text')
        reports = []
        for report in report_elements:
            try:
                title = report.query_selector('a').text_content().strip()
                datetime_author = report.query_selector('span').text_content().split('\n')[-2].strip()
                datetime_obj = datetime.datetime.strptime(datetime_author, '%m/%d/%y')
                link = self.base_url + report.query_selector('a').get_attribute('href')
                company = title.split('(')[0] if '(' in title and ')' in title else ''
                content_obj = ResearchReport(
                    source=self.base_url + link,
                    publication_date=datetime_obj,
                    report_title=title,
                    link=link,
                    target_company=company,
                    short_seller=self.name
                )
                reports.append(content_obj)
            except Exception as e:
                print(f"Error processing report: {e}")
                continue                    
        return reports

if __name__ == "__main__":
    reports = BleeckerStreetResearchScraper().scrape()
    print("\Bleecker Street Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
