import boto3
import os
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv



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