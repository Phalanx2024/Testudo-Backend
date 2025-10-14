from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime

class TriamResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://triamresearch.com/"  # You'll need to verify this URL
        )
        self.name = 'Triam Research'
        
    def get_static_reports(self):
        reports_data = [
            {
                "title": "China All Access Holdings Limited Research Report",
                "date": datetime.datetime(2017, 1, 1),
                "company": "China All Access Holdings Limited",
                "ticker": "633.HK",
                "link": "https://triamresearch.com/"
            },
            {
                "title": "CAA and Skycomm Investigation",
                "date": datetime.datetime(2016, 1, 1),
                "company": "CAA and Skycomm",
                "ticker": "",
                "link": "https://triamresearch.com/"
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
    reports = TriamResearchScraper().scrape()
    print("\nTriam Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}")
