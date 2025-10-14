from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class MithraForensicResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://mithraforensic.com/"  # You'll need to verify this URL
        )
        self.name = 'Mithra Forensic Research'
        
    def get_static_reports(self):
        reports_data = [
            {
                "title": "JD.com Investigation",
                "date": datetime.datetime(2019, 3, 19),
                "company": "JD.com",
                "ticker": "9618",
                "link": "https://mithraforensic.com/"
            },
            {
                "title": "JD.com Analysis",
                "date": datetime.datetime(2018, 1, 5),
                "company": "JD.com",
                "ticker": "9618",
                "link": "https://mithraforensic.com/"
            },
            {
                "title": "Bitcoin Group SE Research Report",
                "date": datetime.datetime(2017, 3, 5),
                "company": "Bitcoin Group SE",
                "ticker": "BTG",
                "link": "https://mithraforensic.com/"
            },
            {
                "title": "Vishop Investigation",
                "date": datetime.datetime(2015, 1, 12),
                "company": "Vishop",
                "ticker": "VIPS",
                "link": "https://mithraforensic.com/"
            },
            {
                "title": "Vishop Analysis",
                "date": datetime.datetime(2015, 7, 31),
                "company": "Vishop",
                "ticker": "VIPS",
                "link": "https://mithraforensic.com/"
            },
            {
                "title": "Vishop Research Report",
                "date": datetime.datetime(2015, 5, 29),
                "company": "Vishop",
                "ticker": "VIPS",
                "link": "https://mithraforensic.com/"
            }
        ]

        reports = []
        for report in reports_data:
            re = ResearchReport(
                source=self.url,
                publication_date=report["date"].date(),
                report_title=report["title"],
                link=report["link"],
                target_company=report["company"],
                short_seller=self.name,
                ticker=report["ticker"]
            )
            reports.append(re)

        return reports

    def extract_reports(self, page):
        # Since this is a static list, we don't need to scrape the page
        return self.get_static_reports()

if __name__ == "__main__":
    reports = MithraForensicResearchScraper().scrape()
    print("\nMithra Forensic Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}")
