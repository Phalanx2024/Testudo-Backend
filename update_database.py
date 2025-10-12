from database.db_controller import DatabaseController
from run_all_scrapers import run_all_scrapers
from reports.get_short_reports import store_research_content
from dotenv import load_dotenv
import boto3
import os
import logging

def report_exists_by_title(db: DatabaseController, table_name: str, report_title: str) -> bool:
    """
    Return True if a report with the same title already exists in the table.
    """
    existing = db.get_data(table_name, { 'report_title': report_title })
    return bool(existing)

def update_database(table_name, results):
    db = DatabaseController()
    newly_inserted = []
    for name, reports in results.items():
        for report in reports:
            # Detect existing report by title
            if report_exists_by_title(db, table_name, report.report_title):
                continue
            else:
                newly_inserted.append(report)
            # if db.insert_data(table_name, report.to_dict()):
    return newly_inserted


def store_new_reports_content(new_reports):
    """Download and upload new report content to S3."""
    if not new_reports:
        return
    load_dotenv()
    bucket_name = os.getenv('S3_BUCKET_NAME')
    if not bucket_name:
        logging.getLogger(__name__).error("S3_BUCKET_NAME is not set in environment")
        return

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

    for report in new_reports:
        link = getattr(report, 'link', None)
        short_seller = getattr(report, 'short_seller', None)
        report_title = getattr(report, 'report_title', None)
        if not link or not short_seller or not report_title:
            logging.getLogger(__name__).warning("Skipping report with missing fields")
            continue
        try:
            store_research_content(link, bucket_name, s3_client, short_seller, report_title)
        except Exception as e:
            logging.getLogger(__name__).error(f"Failed to store content for '{report_title}': {e}")

def update_short_sellers(results):
    db = DatabaseController()
    for name, reports in results.items():
        for report in reports:
            report.to_dict()
            data = {
                'name': report.short_seller,
                'link': report.link
            }
            logger.info(f"Updating short seller {data}")
            db.insert_data("short_sellers", data)
            
def update_target_companies(results):
    db = DatabaseController()
    for name, reports in results.items():
        for report in reports:
            report.to_dict()
            data = {
                'name': report.target_company,
            }
            logger.info(f"Updating target company {data}")
            db.insert_data("target_companies", data)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting all scrapers")
    results = run_all_scrapers()
    # Your test code here

    logger.info("Updating database with scraped results")
    new_reports = update_database("short_reports", results)
    print("\nNewly inserted short reports:")
    print("-" * 50)
    if not new_reports:
        print("No new short reports inserted.")
    else:
        for r in new_reports:
            print(f"{getattr(r, 'publication_date', '')} | {getattr(r, 'short_seller', '')} | {getattr(r, 'report_title', '')} | {getattr(r, 'link', '')}")
        # Download and store content to S3 for newly discovered reports
        store_new_reports_content(new_reports)
    update_short_sellers(results)
    update_target_companies(results)