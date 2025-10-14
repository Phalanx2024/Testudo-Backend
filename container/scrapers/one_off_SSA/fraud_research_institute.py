from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime

class FraudResearchInstituteScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://fraudresearchinstitute.com/"  # You'll need to verify this URL
        )
        self.name = 'Fraud Research Institute'
        
    def get_static_reports(self):
        reports_data = [
            {
                "title": "Perkins Oil and Gas Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Perkins Oil and Gas",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Cloudweb Research Report",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Cloudweb",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Luminar Media Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Luminar Media",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Onelife Technologies Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Onelife Technologies",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Zoompass Holdings Research",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Zoompass Holdings",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Vapor Group Analysis",
                "date": datetime.datetime(2014, 1, 1),
                "company": "Vapor Group",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Vapor Group Investigation",
                "date": datetime.datetime(2014, 1, 1),
                "company": "Vapor Group",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Well Power Research Report",
                "date": datetime.datetime(2014, 1, 1),
                "company": "Well Power",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Gray Fox Petroleum Analysis",
                "date": datetime.datetime(2014, 1, 1),
                "company": "Gray Fox Petroleum",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Nuvilex Investigation",
                "date": datetime.datetime(2014, 1, 1),
                "company": "Nuvilex",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Generation Next Franchise Brands Research",
                "date": datetime.datetime(2014, 1, 1),
                "company": "Generation Next Franchise Brands",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Swingplane Ventures Analysis",
                "date": datetime.datetime(2013, 1, 1),
                "company": "Swingplane Ventures",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Echo Automotive Investigation",
                "date": datetime.datetime(2013, 1, 1),
                "company": "Echo Automotive",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "Medical Marijuana Inc Research Report",
                "date": datetime.datetime(2013, 1, 1),
                "company": "Medical Marijuana Inc",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
            },
            {
                "title": "USA Graphite Analysis",
                "date": datetime.datetime(2013, 1, 1),
                "company": "USA Graphite",
                "ticker": "",
                "link": "https://fraudresearchinstitute.com/"
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
    reports = FraudResearchInstituteScraper().scrape()
    print("\nFraud Research Institute Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}")
