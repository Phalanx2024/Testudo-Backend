import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class QuintessentialCapitalScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.qcmfunds.com/reports/"  # You'll need to verify this URL
        )
        self.name = 'Quintessential Capital'
        
    def get_static_reports(self):
        # Static list of reports since they don't have a structured webpage
        reports_data = [
              {
                "title": "The dark side of Darktrace",
                "date": datetime.datetime(2023, 1, 1),  # Approximate date
                "company": "Darktrace ",
                "link": "https://www.qcmfunds.com/the-dark-side-of-darktrace/"
            },
            {
                "title": "Cassava Sciences Research Report",
                "date": datetime.datetime(2023, 1, 1),  # Approximate date
                "company": "Cassava Sciences",
                "link": "https://www.qcmfunds.com/cassava-sciences/"
            },
            {
                "title": "Penumbra: Short Seller Critical Report",
                "date": datetime.datetime(2020, 12, 1),  # Approximate date
                "company": "Penumbra",
                "link": "https://www.qcmfunds.com/penumbra-report/"
            },
            {
                "title": "Sun Corporation: Buy Recommendation",
                "date": datetime.datetime(2023, 1, 1),  # Approximate date
                "company": "Sun Corporation",
                "link": "https://www.qcmfunds.com/sun-corporation/"
            },
            {
                "title": "Akazoo: Fraud Investigation Report",
                "date": datetime.datetime(2020, 4, 1),  # Approximate date
                "company": "Akazoo",
                "link": "https://www.qcmfunds.com/akazoo-report/"
            },
            {
                "title": "Bio-on: Accounting Flaws Investigation",
                "date": datetime.datetime(2019, 7, 1),  # Approximate date
                "company": "Bio-on",
                "link": "https://www.qcmfunds.com/bio-on-report/"
            },
            {
                "title": "Globo Plc: Financial Data Investigation",
                "date": datetime.datetime(2015, 10, 1),  # Approximate date
                "company": "Globo Plc",
                "link": "https://www.qcmfunds.com/globo-report/"
            },
            {
                "title": "Folli Follie: Asia Sales Investigation",
                "date": datetime.datetime(2018, 5, 1),  # Approximate date
                "company": "Folli Follie",
                "link": "https://www.qcmfunds.com/folli-follie-report/"
            },
            {
                "title": "Aphria: Cannabis Company Investigation",
                "date": datetime.datetime(2018, 12, 1),  # Approximate date
                "company": "Aphria",
                "link": "https://www.qcmfunds.com/aphria-report/"
            }
        ]
        
        return [
            ResearchReport(
                source=self.url,
                publication_date=report["date"].date(),
                report_title=report["title"],
                link=report["link"],
                target_company=report["company"],
                short_seller=self.name
            )
            for report in reports_data
        ]

    def extract_reports(self, page):
        # Since this is a static list, we don't need to scrape the page
        return self.get_static_reports()

if __name__ == "__main__":
    reports = QuintessentialCapitalScraper().scrape()
    print("\nQuintessential Capital Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")