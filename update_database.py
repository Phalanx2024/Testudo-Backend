from database.db_controller import DatabaseController
from run_all_scrapers import run_all_scrapers
import logging

def update_database(table_name, results):
    db = DatabaseController()
    for name, reports in results.items():
        for report in reports:
            db.insert_data(table_name, report.to_dict())

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

    logger.info(f"Updating database with {results}")
    update_database("short_reports", results)
    # update_short_sellers( results)
    # update_target_companies(results)