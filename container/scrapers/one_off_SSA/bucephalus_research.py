from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import boto3
import os
import logging

class BucephalusResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://bucephalusresearch.com/"  # You'll need to verify this URL
        )
        self.name = 'Bucephalus Research'
        
    def get_static_reports(self):
        reports_data = [
            # 2020 Reports
            {
                "title": "Lenovo Investigation",
                "date": datetime.datetime(2020, 1, 1),
                "company": "Lenovo",
                "ticker": "992.HK",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Patterson Analysis",
                "date": datetime.datetime(2020, 1, 1),
                "company": "Patterson",
                "ticker": "PDCO",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Rural Funds Group Research",
                "date": datetime.datetime(2020, 1, 1),
                "company": "Rural Funds Group",
                "ticker": "RFF.AU",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Tesla Investigation",
                "date": datetime.datetime(2020, 1, 1),
                "company": "Tesla",
                "ticker": "TSLA",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "WiseTech Analysis",
                "date": datetime.datetime(2020, 1, 1),
                "company": "WiseTech",
                "ticker": "WTC.AU",
                "link": "https://bucephalusresearch.com/"
            },
            # 2019 Reports
            {
                "title": "CIMIC Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "CIMIC",
                "ticker": "CIM.AU",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Hochtief Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Hochtief",
                "ticker": "HOT.GR",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "ACS Research",
                "date": datetime.datetime(2019, 1, 1),
                "company": "ACS",
                "ticker": "ACS.SM",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Patterson Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Patterson",
                "ticker": "PDCO",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Cineworld Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Cineworld",
                "ticker": "CINE",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Rural Funds Group Research",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Rural Funds Group",
                "ticker": "RFF.AU",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Rural Funds Group Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Rural Funds Group",
                "ticker": "RFF.AU",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "BAE Systems Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "BAE Systems",
                "ticker": "BA/",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Li & Fung Research",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Li & Fung",
                "ticker": "494.HK",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "FI Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "FI",
                "ticker": "494.HK",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Prada Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Prada",
                "ticker": "1913.HK",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Hengan Research",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Hengan",
                "ticker": "1099.HK",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Renault Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Renault",
                "ticker": "RNO",
                "link": "https://bucephalusresearch.com/"
            },
            # 2018 Reports
            {
                "title": "Bombardier Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Bombardier",
                "ticker": "BBD",
                "link": "https://bucephalusresearch.com/"
            },
            # General Reports
            {
                "title": "Autodesk Research",
                "date": None,
                "company": "Autodesk",
                "ticker": "ADSK.US",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "BT Group Investigation",
                "date": None,
                "company": "BT Group",
                "ticker": "BT",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Celltrion Analysis",
                "date": None,
                "company": "Celltrion",
                "ticker": "68270.KS",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Man Wah Research",
                "date": None,
                "company": "Man Wah",
                "ticker": "1999.HK",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Ricoh Investigation",
                "date": None,
                "company": "Ricoh",
                "ticker": "7752.JP",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "Thyssenkrupp Analysis",
                "date": None,
                "company": "Thyssenkrupp",
                "ticker": "TKA.GR",
                "link": "https://bucephalusresearch.com/"
            },
            {
                "title": "UPS Research",
                "date": None,
                "company": "UPS",
                "ticker": "UPS.US",
                "link": "https://bucephalusresearch.com/"
            }
        ]

        reports = []
        for report in reports_data:
            re = ResearchReport(
                source=self.url,
                publication_date=report["date"].date() if report["date"] else None,
                report_title=report["title"],
                link=report["link"],
                target_company=report["company"],
                short_seller=self.name,
                ticker=report["ticker"]
            )
            reports.append(re)

        return reports

    def extract_reports(self, page):
        try:
            # Get the page content
            content = page.content()
            
            # Initialize S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
            
            bucket_name = os.getenv('S3_BUCKET_NAME')
            
            # Generate filename using timestamp and company name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.name}_{timestamp}.html"
            
            # Store in S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=f"scraped_content/{filename}",
                Body=content,
                ContentType='text/html'
            )
            
            # Return the static reports
            return self.get_static_reports()
            
        except Exception as e:
            logging.error(f"Error storing content in S3: {str(e)}")
            return self.get_static_reports()

if __name__ == "__main__":
    reports = BucephalusResearchScraper().scrape()
    print("\nBucephalus Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}")
