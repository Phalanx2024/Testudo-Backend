import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
from datetime import datetime

class PigFarmerCapitalScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.pigfarmercapital.com/report"
        )
        self.name = 'Pig Farmer Capital'
    
    def extract_reports(self, page):
        report_elements = page.query_selector_all("div.sqs-html-content")
        
        reports = []
        for report in report_elements:
            try:
                anchor = report.query_selector("a")
                if anchor:
                    href = anchor.get_attribute("href")
                    if href and href.endswith(".pdf"):
                        full_link = "https://www.pigfarmercapital.com" + href

                        short_seller = self.name
                        target_company = 'Enovix'
                        reports.append(ResearchReport(
                            source=self.url,
                            publication_date="No Date",
                            report_title="Enovix: TJ Rodgers Can’t Save this Overhyped Battery Technology",
                            link=full_link,
                            target_company=target_company,
                            short_seller=short_seller
                        ))
                    
            except Exception as e:
                logging.error(f"Error processing report: {str(e)}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = PigFarmerCapitalScraper().scrape()

    print("\n Big Farmer Capital Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")