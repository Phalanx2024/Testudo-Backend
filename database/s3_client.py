import boto3
import logging
from botocore.exceptions import ClientError
import os

class S3Client:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.environ.get('S3_BUCKET_NAME')

    def upload_file(self, file_data, key):
        """
        Upload a file to S3
        """
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_data,
            )
            return f"s3://{self.bucket_name}/{key}"
        except ClientError as e:
            logging.error(f"Error uploading to S3: {e}")
            raise

    def get_file(self, key):
        """
        Get a file from S3
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return response['Body'].read()
        except ClientError as e:
            logging.error(f"Error getting file from S3: {e}")
            raise

    def delete_file(self, key):
        """
        Delete a file from S3
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
        except ClientError as e:
            logging.error(f"Error deleting file from S3: {e}")
            raise

    def list_files(self, prefix=''):
        """
        List files in S3 bucket with optional prefix
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            return [obj['Key'] for obj in response.get('Contents', [])]
        except ClientError as e:
            logging.error(f"Error listing files in S3: {e}")
            raise

    def generate_presigned_url(self, key, expiration=3600):
        """
        Generate a presigned URL for file download
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logging.error(f"Error generating presigned URL: {e}")
            raise