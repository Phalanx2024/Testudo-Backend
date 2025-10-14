import os
from datetime import datetime
import logging
import psycopg2
from scrapers.sunshine_research import SunshineResearchScraper
from scrapers.prescience_point import PresciencePointScraper
from scrapers.guasty_winds import GuastyWindsScraper
from scrapers.friendly_bear import FriendlyBearScraper

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host=os.environ['NEON_HOST'],
            database=os.environ['NEON_DATABASE'],
            user=os.environ['NEON_USER'],
            password=os.environ['NEON_PASSWORD']
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def save_report_to_db(conn, report):
    """Save a single report to database"""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO reports (
                    source, publication_date, report_title, 
                    link, target_company, short_seller, 
                    ticker, s3_path
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (link) DO UPDATE SET
                    s3_path = EXCLUDED.s3_path
                RETURNING id;
            """, (
                report.source,
                report.publication_date,
                report.report_title,
                report.link,
                report.target_company,
                report.short_seller,
                report.ticker,
                report.s3_path
            ))
            conn.commit()
            return cur.fetchone()[0]
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")
        conn.rollback()
        raise

def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        logger.info("Starting scraper run")
        
        # Initialize scrapers
        scrapers = [
            SunshineResearchScraper(),
            PresciencePointScraper(),
            GuastyWindsScraper(),
            FriendlyBearScraper()
        ]
        
        # Connect to database
        conn = get_db_connection()
        
        total_reports = 0
        new_reports = 0
        
        # Run each scraper
        for scraper in scrapers:
            try:
                logger.info(f"Running scraper: {scraper.name}")
                reports = scraper.scrape()
                
                if reports:
                    for report in reports:
                        try:
                            save_report_to_db(conn, report)
                            new_reports += 1
                        except Exception as e:
                            logger.error(f"Error saving report: {str(e)}")
                            continue
                            
                    total_reports += len(reports)
                    logger.info(f"Found {len(reports)} reports from {scraper.name}")
                
            except Exception as e:
                logger.error(f"Error with scraper {scraper.name}: {str(e)}")
                continue
        
        conn.close()
        
        return {
            'statusCode': 200,
            'body': f'Successfully scraped {total_reports} reports, {new_reports} new entries'
        }
        
    except Exception as e:
        logger.error(f"Lambda execution error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }