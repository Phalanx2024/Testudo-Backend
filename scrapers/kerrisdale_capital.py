import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class KerrisdaleScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.kerrisdalecap.com/blog"
        )
        self.name = 'Kerrisdale Capital'
        self.base_url = "https://www.kerrisdalecap.com"

    def extract_reports(self, page):
        reports = []
        
        try:
            page.wait_for_selector('div.each-post')
            report_elements = page.query_selector_all('div.each-post')
            
            for report in report_elements:
                try:
                    # Extract title and subtitle
                    title = report.query_selector('h2').text_content().strip()
                    subtitle = report.query_selector('p.post-desc').text_content().strip()
                    full_title = f"{title}, {subtitle}"
                    
                    # Extract date
                    date_parts = report.query_selector('div.post-date').text_content().strip().split('\n')
                    date_parts = [ele.strip() for ele in date_parts]
                    date_str = '/'.join(date_parts)
                    datetime_obj = datetime.datetime.strptime(date_str, '%b/%d/%Y')
                    
                    # Extract link from onclick attribute
                    link_element = report.query_selector('a')
                    onclick = link_element.get_attribute('onclick')
                    link = onclick.split(',')[3].strip("' ")
                    
                    report = ResearchReport(
                        source=self.base_url,
                        publication_date=datetime_obj.date(),
                        report_title=full_title,
                        link=link,
                        target_company=title,
                        short_seller=self.name
                    )
                    reports.append(report)
                    
                except Exception as e:
                    logging.error(f"Error processing report: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    reports = KerrisdaleScraper().scrape()
    print("\nKerrisdale Capital Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
