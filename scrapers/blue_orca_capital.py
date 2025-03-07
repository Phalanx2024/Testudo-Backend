import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class BlueOrcaCapitalScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.blueorcacapital.com/category/reports/"
        )
        self.name = 'Blue Orca Capital'

    def extract_reports(self, page):
        table = page.query_selector('table.cs-archive-table')
        report_elements = table.query_selector_all('tr')
        reports = []
        
        for item in report_elements:
            try:
                link = item.query_selector('a').get_attribute('href')
                title_element = item.query_selector_all('td')
                title = title_element[0].text_content().strip()
                if ':' in title:
                    title = title.split(':')[1].strip()
                company = title_element[1].text_content().strip()
                ticker = title_element[2].text_content().strip()
                date_str = title_element[3].text_content().strip()
                
                # Convert date string to datetime object
                datetime_obj = datetime.datetime.strptime(date_str, '%B %d, %Y')
                
                report = ResearchReport(
                    source=link,
                    publication_date=datetime_obj,
                    report_title=title,
                    link=link,
                    target_company=company + ticker,
                    short_seller=self.name
                )
                reports.append(report)
                
            except Exception as e:
                logging.error(f"Error processing report: {e}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = BlueOrcaCapitalScraper().scrape()
    print("\nBlue Orca Capital Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
