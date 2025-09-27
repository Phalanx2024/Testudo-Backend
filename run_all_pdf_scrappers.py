import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import time
import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from reports.get_short_reports import store_research_content, store_using_beautifulsoup
from reports.report_handlers import ShortReportController
from reports.pdf_scrappers.ningi_research import NingiResearchPDFScraper
from reports.pdf_scrappers.snowcap_research import SnowcapResearchPDFScraper
from reports.pdf_scrappers.viceroy_research import ViceroyResearchPDFScraper
from reports.pdf_scrappers.sprucepoint_management import SprucePointManagementPDFScraper
from reports.pdf_scrappers.bonitas_research import BonitasResearchPDFScraper
from reports.pdf_scrappers.prescience_point import PresciencePointPDFScraper
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define scraper configurations
SCRAPER_CONFIGS = [
    # {
    #     'name': 'Ningi Research',
    #     'class': NingiResearchPDFScraper
    # },
    # {
    #     'name': 'Snowcap Research',
    #     'class': SnowcapResearchPDFScraper
    # },
    # {
    #     'name': 'Viceroy Research',
    #     'class': ViceroyResearchPDFScraper
    # },
    # {
    #     'name': 'Spruce Point Management',
    #     'class': SprucePointManagementPDFScraper
    # },
    # {
    #     'name': 'Bonitas Research',
    #     'class': BonitasResearchPDFScraper
    # },
    # {
    #     'name': 'Prescience Point',
    #     'class': PresciencePointPDFScraper
    # }
]

def run_scraper(config: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Run a single scraper and return its results
    """
    logger.info(f"Starting scraper for {config['name']}")
    try:
        # Get list of URLs to scrape
        urls_to_scrape = config['class']._get_short_report()
        if not urls_to_scrape:
            logger.warning(f"No URLs found for {config['name']}")
            return []

        all_results = []
        # Add retry logic
        max_retries = 3
        for report in urls_to_scrape:
            url = report['report_link']
            scraper = config['class'](url)
            
            for attempt in range(max_retries):
                try:
                    result = scraper.scrape()
                    if result:
                        all_results.append({
                            'report_name': report['report_name'],
                            'report_link': result,
                        })
                        break
                    else:
                        logger.warning(f"Attempt {attempt + 1}/{max_retries}: No results found for {url}, retrying...")
                        if attempt < max_retries - 1:  # Don't sleep on last attempt
                            time.sleep(5)  # Wait 5 seconds between retries
                except Exception as e:
                    logger.error(f"Error scraping {url}: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

        logger.info(f"Successfully scraped {len(all_results)} reports from {config['name']}")
        return all_results
    except Exception as e:
        logger.error(f"Error running {config['name']} scraper: {str(e)}")
        return []

def run_all_scrapers(max_workers: int = 2) -> Dict[str, List[Dict[str, str]]]:
    """
    Run all scrapers in parallel using ThreadPoolExecutor
    
    Args:
        max_workers (int): Maximum number of parallel scraping tasks
        
    Returns:
        Dict[str, List[Dict[str, str]]]: Dictionary mapping scraper names to their results
    """
    # Reduce max_workers to avoid overwhelming resources
    all_results = {}
    
    # Group scrapers into batches to avoid overwhelming the system
    for i in range(0, len(SCRAPER_CONFIGS), max_workers):
        batch = SCRAPER_CONFIGS[i:i + max_workers]
        logger.info(f"Processing batch of {len(batch)} scrapers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_config = {
                executor.submit(run_scraper, config): config
                for config in batch
            }
            
            for future in future_to_config:
                config = future_to_config[future]
                try:
                    results = future.result()
                    all_results[config['name']] = results
                except Exception as e:
                    logger.error(f"Scraper {config['name']} failed with error: {str(e)}")
                    all_results[config['name']] = []
        
        # Add a small delay between batches
        if i + max_workers < len(SCRAPER_CONFIGS):
            time.sleep(2)
    
    return all_results

def main():
    """
    Main function to run all scrapers and display results
    """
    logger.info("Starting all scrapers")
    report_to_store = run_all_scrapers()
    try:
        load_dotenv()
        # Initialize the S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        
        bucket_name = os.getenv('S3_BUCKET_NAME')

        for short_seller, reports in report_to_store.items():
            for report in reports:
                report_name = report['report_name']
                report_link = report['report_link']
                if short_seller == "Prescience Point":
                    store_using_beautifulsoup(report_link, bucket_name, s3_client, short_seller, report_name)
                else:
                    store_research_content(report_link, bucket_name, s3_client, short_seller, report_name)

        print("Testing S3 Connection...")
        
        # Test 1: List buckets
        print("\nTest 1: Listing buckets")
        response = s3_client.list_buckets()
        print(f"Found {len(response['Buckets'])} buckets:")
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
            
        # Test 2: Check specific bucket
        print(f"\nTest 2: Checking access to bucket: {bucket_name}")
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Successfully accessed bucket: {bucket_name}")
        
        # Test 3: Upload a test file
        print("\nTest 3: Uploading test file")
        test_content = b"This is a test file"
        test_key = "test/test_file.txt"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=test_content
        )
        print(f"Successfully uploaded test file to: {test_key}")
        
        # Test 4: Download the test file
        print("\nTest 4: Downloading test file")
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=test_key
        )
        downloaded_content = response['Body'].read()
        print(f"Successfully downloaded test file. Content matches: {downloaded_content == test_content}")
        
        # Test 5: Delete the test file
        print("\nTest 5: Deleting test file")
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=test_key
        )
        print("Successfully deleted test file")
        
        print("\nAll tests completed successfully! ✅")

        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"\n❌ Error: {error_code}")
        print(f"Message: {error_message}")
        
        if error_code == 'InvalidAccessKeyId':
            print("\nTroubleshooting tip: Check if your AWS_ACCESS_KEY_ID is correct")
        elif error_code == 'SignatureDoesNotMatch':
            print("\nTroubleshooting tip: Check if your AWS_SECRET_ACCESS_KEY is correct")
        elif error_code == 'NoSuchBucket':
            print("\nTroubleshooting tip: Check if your S3_BUCKET_NAME is correct")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
 
    # Print current configuration (without secret key)
    print("Current Configuration:")
    print(f"AWS_REGION: {os.environ.get('AWS_REGION', 'Not set')}")
    print(f"S3_BUCKET_NAME: {os.environ.get('S3_BUCKET_NAME', 'Not set')}")
    print(f"AWS_ACCESS_KEY_ID: {'Set' if os.environ.get('AWS_ACCESS_KEY_ID') else 'Not set'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'Set' if os.environ.get('AWS_SECRET_ACCESS_KEY') else 'Not set'}\n")
    
    main()
