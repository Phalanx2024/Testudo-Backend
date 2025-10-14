import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
from datetime import datetime
import re

class BirdDogResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.birddogresearch.com/"
        )
        self.name = 'Bird Dog Research'
    
    def extract_reports(self, page):
        report_elements = page.query_selector_all('div[jscontroller="sGwD4d"]')
        
        reports = []
        for element in report_elements:
            try:
                title_span = element.query_selector('span.C9DxTc.aw5Odc')
                title = title_span.inner_text().strip() if title_span else None

                target_company = title.split(":")[0].strip()

                all_spans = element.query_selector_all('span.C9DxTc')
                date_str = None
                for span in all_spans:
                    if 'aw5Odc' not in span.get_attribute('class'):
                        date_str = span.inner_text().strip()
                
                cleaned = date_str.replace("Published ", "").strip()
                cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', cleaned)
                date = datetime.strptime(cleaned, '%B %d, %Y')


                reports.append(ResearchReport(
                    source=self.url,
                    publication_date=date,
                    report_title=title,
                    link=None,
                    target_company=target_company,
                    short_seller='Bird Dog Research'
                ))
                
            except Exception as e:
                logging.error(f"Error processing report: {str(e)}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = BirdDogResearchScraper().scrape()

    print("\n Bird Dog Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")