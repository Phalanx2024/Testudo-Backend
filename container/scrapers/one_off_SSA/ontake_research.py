from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime

class OntakeResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://ontakeresearch.com/"  # You'll need to verify this URL
        )
        self.name = 'Ontake Research'
        
    def get_static_reports(self):
        reports_data = [
            {
                "title": "Kerry Group PLC Investigation",
                "date": datetime.datetime(2021, 11, 2),
                "company": "Kerry Group PLC",
                "ticker": "KYGA",
                "link": "https://ontakeresearch.com/"
            },
            {
                "title": "Aerelius Equity Opportunities SE and Co Analysis",
                "date": datetime.datetime(2020, 2, 14),
                "company": "Aerelius Equity Opportunities SE and Co_2",
                "ticker": "AE4",
                "link": "https://ontakeresearch.com/"
            },
            {
                "title": "Aerelius Equity Opportunities SE and Co Research Report",
                "date": datetime.datetime(2020, 1, 30),
                "company": "Aerelius Equity Opportunities SE and Co_1",
                "ticker": "AE4",
                "link": "https://ontakeresearch.com/"
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
    reports = OntakeResearchScraper().scrape()
    print("\nOntake Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}")
