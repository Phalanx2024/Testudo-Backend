import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from reports.get_short_reports import store_research_content
from reports.report_handlers import ShortReportController
from reports.pdf_scrappers.ningi_research import NingiResearchPDFScraper
def test_s3_connection():
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

        short_report_controller = ShortReportController()
        report_to_store = short_report_controller.get_short_reports()
        for short_seller, reports in report_to_store.items():
            for report in reports:
                report_name = report['report_name']
                report_link = report['report_link']
                store_research_content(report_link, bucket_name, s3_client, short_seller, report_name)
        
        # # Test storing PDF content
        # pdf_url = "https://muddywatersresearch.com/wp-content/uploads/2011/04/DGW_MW_040411.pdf"
        # store_research_content(pdf_url, bucket_name, s3_client)
        
        # # Test storing HTML content
        # html_url = "https://muddywatersresearch.com/research/dgw/initiating-coverage-dgw/"
        # store_research_content(html_url, bucket_name, s3_client)
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
    
    test_s3_connection()


# if __name__ == "__main__":
#     test_url = "https://ningiresearch.com/2025/03/26/vita-coco-nasdaq-coco-structural-issues-amid-stalling-sales-and-costco-contract-loss/"
#     scraper = NingiResearchPDFScraper(test_url)
#     result = scraper.get_pdf_link(scraper.page)
#     print(result)

