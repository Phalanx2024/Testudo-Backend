from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class EmersonAnalyticsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://emersonanalytics.com/"  # You'll need to verify this URL
        )
        self.name = 'Emerson Analytics'
        
    def get_static_reports(self):
        reports_data = [
            {
                "title": "Realord Group Holdings Limited Research Report",
                "date": datetime.datetime(2019, 7, 28),
                "company": "Realord Group Holdings Limited",
                "ticker": "1196.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Realord Group Holdings Limited Analysis",
                "date": datetime.datetime(2019, 7, 21),
                "company": "Realord Group Holdings Limited",
                "ticker": "1196.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Southern Energy Holdings Group Limited Investigation",
                "date": datetime.datetime(2019, 6, 29),
                "company": "Southern Energy Holdings Group Limited",
                "ticker": "1573.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Zhou Hei International Holdings Company Limited Research",
                "date": datetime.datetime(2019, 3, 13),
                "company": "Zhou Hei International Holdings Company Limited",
                "ticker": "1458.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Zhou Hei International Holdings Company Limited Analysis",
                "date": datetime.datetime(2019, 1, 3),
                "company": "Zhou Hei International Holdings Company Limited",
                "ticker": "1458.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Tian Ge Interactive Holdings Limited Investigation",
                "date": datetime.datetime(2017, 8, 28),
                "company": "Tian Ge Interactive Holdings Limited",
                "ticker": "1980.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Tian Ge Interactive Holdings Limited Research",
                "date": datetime.datetime(2017, 8, 16),
                "company": "Tian Ge Interactive Holdings Limited",
                "ticker": "1980.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Hua Han Health Industry Holdings Limited Analysis",
                "date": datetime.datetime(2016, 7, 9),
                "company": "Hua Han Health Industry Holdings Limited",
                "ticker": "00587.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Hua Han Health Industry Holdings Limited Investigation",
                "date": datetime.datetime(2016, 8, 26),
                "company": "Hua Han Health Industry Holdings Limited",
                "ticker": "00587.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Hua Han Health Industry Holdings Limited Research",
                "date": datetime.datetime(2016, 10, 8),
                "company": "Hua Han Health Industry Holdings Limited",
                "ticker": "00587.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "China Diber Optic Network System Group Ltd Analysis",
                "date": datetime.datetime(2015, 10, 29),
                "company": "China Diber Optic Network System Group Ltd",
                "ticker": "0377.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "China Diber Optic Network System Group Ltd Investigation",
                "date": datetime.datetime(2016, 10, 8),
                "company": "China Diber Optic Network System Group Ltd",
                "ticker": "0377.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Sound Global Ltd Research",
                "date": datetime.datetime(2015, 2, 23),
                "company": "Sound Global Ltd",
                "ticker": "00967.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Sound Global Ltd Analysis",
                "date": datetime.datetime(2015, 2, 15),
                "company": "Sound Global Ltd",
                "ticker": "00967.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Sound Global Ltd Investigation",
                "date": datetime.datetime(2015, 2, 2),
                "company": "Sound Global Ltd",
                "ticker": "00967.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Shenguan Holdings Group Limited Research",
                "date": datetime.datetime(2014, 9, 29),
                "company": "Shenguan Holdings Group Limited",
                "ticker": "00829.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "Shenguan Holdings Group Limited Analysis",
                "date": datetime.datetime(2014, 2, 9),
                "company": "Shenguan Holdings Group Limited",
                "ticker": "00829.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "China Lumena New Materials Corp Investigation",
                "date": datetime.datetime(2014, 6, 5),
                "company": "China Lumena New Materials Corp",
                "ticker": "00067.HK",
                "link": "https://emersonanalytics.com/"
            },
            {
                "title": "China Lumena New Materials Corp Research",
                "date": datetime.datetime(2014, 1, 4),
                "company": "China Lumena New Materials Corp",
                "ticker": "00067.HK",
                "link": "https://emersonanalytics.com/"
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
    reports = EmersonAnalyticsScraper().scrape()
    print("\nEmerson Analytics Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}")
