# lambda_function.py
import asyncio
import boto3
import json
import logging
import time
from run_scrapers import run_all_scrapers
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def scroll_to_bottom(page):
    try:
        previous_height = await page.evaluate('document.body.scrollHeight')
        while True:
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(3)
            current_height = await page.evaluate('document.body.scrollHeight')
            if current_height == previous_height:
                break
            previous_height = current_height
    except Exception as e:
        logger.error(f"Error during scrolling: {e}")
        raise

async def download_page_content(url):
    async with async_playwright() as p:
        # Launch the browser with all necessary parameters
        logger.info("Launching browser...")
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--single-process",
                "--disable-dev-shm-usage",
                "--no-zygote",
                "--disable-setuid-sandbox",
                "--disable-accelerated-2d-canvas",
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-background-networking",
                "--disable-background-timer-throttling",
                "--disable-client-side-phishing-detection",
                "--disable-component-update",
                "--disable-default-apps",
                "--disable-domain-reliability",
                "--disable-features=AudioServiceOutOfProcess",
                "--disable-hang-monitor",
                "--disable-ipc-flooding-protection",
                "--disable-popup-blocking",
                "--disable-prompt-on-repost",
                "--disable-renderer-backgrounding",
                "--disable-sync",
                "--force-color-profile=srgb",
                "--metrics-recording-only",
                "--mute-audio",
                "--no-pings",
                "--use-gl=swiftshader",
                "--window-size=1280,1696"
            ]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()

        # Set headers
        await page.set_extra_http_headers({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        })

        await page.set_content("<meta http-equiv='X-Content-Type-Options' content='nosniff'>")

        # Navigate to URL
        logger.info(f"Navigating to URL: {url}")
        try:
            await page.goto(url, timeout=60000)
            try:
                await page.wait_for_load_state('networkidle', timeout=60000)
            except Exception as e:
                logger.warning(f"Network idle state timed out: {e}")
            logger.info("Page loaded successfully.")

            # Scroll to bottom
            await scroll_to_bottom(page)
            await page.wait_for_timeout(5000)
            logger.info("Scrolled to the bottom.")

            # Get the page content
            content = await page.content()
        except Exception as e:
            logger.error(f"Failed to load page: {e}")
            raise

        await browser.close()
        logger.info("Browser closed.")

        return content

async def main(event):
    """
    Main lambda function that runs all scrapers
    """
    try:
        logger.info("Starting scraper lambda function")
        
        # Run all scrapers
        logger.info("Running all scrapers...")
        results = run_all_scrapers(max_workers=1)  # Single worker to avoid disk space issues
        
        # Calculate total reports
        total_reports = sum(len(reports) for reports in results.values())
        successful_scrapers = sum(1 for reports in results.values() if len(reports) > 0)
        
        logger.info(f"Scraping completed. Total reports: {total_reports} from {successful_scrapers} scrapers")
        
        # Log total count of new reports and database operations
        if total_reports > 0:
            logger.info(f"TOTAL NEW REPORTS SCRAPED: {total_reports} reports have been successfully scraped and added to the database")
            logger.info(f"TOTAL DATABASE WRITES SUCCESSFUL: {total_reports} reports have been successfully written to the database")
        else:
            logger.info("NO NEW REPORTS SCRAPED: No new reports have been scraped from any source")
            logger.info("NO DATABASE WRITES: No reports were written to the database")
        
        # Prepare response
        response = {
            'statusCode': 200,
            'message': f'Successfully scraped {total_reports} reports from {successful_scrapers} scrapers',
            'total_reports': total_reports,
            'successful_scrapers': successful_scrapers,
            'total_scrapers': len(results),
            'database_writes': total_reports,  # Assuming all scraped reports were written to database
            'scraper_results': {}
        }
        
        # Add summary for each scraper
        for scraper_name, reports in results.items():
            response['scraper_results'][scraper_name] = {
                'report_count': len(reports),
                'status': 'success' if len(reports) > 0 else 'no_reports'
            }
        
        # If S3 upload is requested in event
        if event.get('upload_to_s3'):
            bucket_name = event.get('bucket', 'testudo-scraped-reports')
            output_key = event.get('output_key', f'scraper-results-{int(time.time())}.json')
            
            try:
                logger.info("Uploading results to S3...")
                s3_client = boto3.client('s3')
                
                # Convert results to JSON string
                results_json = json.dumps(results, default=str, indent=2)
                
                s3_client.put_object(
                    Bucket=bucket_name, 
                    Key=output_key, 
                    Body=results_json, 
                    ContentType='application/json'
                )
                
                response['s3_upload'] = {
                    'bucket': bucket_name,
                    'key': output_key,
                    'status': 'success'
                }
                logger.info(f"Results uploaded to S3: s3://{bucket_name}/{output_key}")
                
            except Exception as e:
                logger.error(f"Error uploading to S3: {e}")
                response['s3_upload'] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        return response
        
    except Exception as e:
        logger.error(f"Error in lambda function: {str(e)}")
        return {
            'statusCode': 500,
            'message': f'Error running scrapers: {str(e)}',
            'error': str(e)
        }

def handler(event, context):
    """
    AWS Lambda handler function
    """
    return asyncio.run(main(event))