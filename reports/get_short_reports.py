import boto3
import os
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv
from datetime import datetime
import mimetypes
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
def store_research_content(url, bucket_name, s3_client, short_seller_name, report_name):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path="/Users/albertzhang/Library/Caches/ms-playwright/chromium_headless_shell-1155/chrome-mac/headless_shell",
                headless=True,
            )
            context = browser.new_context(
                ignore_https_errors=True,
                viewport=None,
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            page.set_default_timeout(60000)
           
             # Navigate to the URL
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_load_state('networkidle')
                
            # Determine content type
            is_pdf = url.lower().endswith('.pdf')
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = '.pdf' if is_pdf else '.html'
            filename = f"{report_name}{file_extension}"
            
            # Prepare content and metadata
            if is_pdf:
                # For PDFs, get the content directly
                content = page.content()
                content_type = 'application/pdf'
            else:
                # For HTML pages, get the rendered content
                content = page.content()
                content_type = 'text/html'
            
            # Upload to S3 with metadata
            s3_client.put_object(
                Bucket=bucket_name,
                Key=f"research_reports/{short_seller_name}/{filename}",
                Body=content,
                ContentType=content_type,
                Metadata={
                    'source': f'{short_seller_name}',
                    'date': timestamp,
                    'url': url,
                    'content_type': 'pdf' if is_pdf else 'html'
                }
            )
            
            browser.close()
            print(f"Successfully stored content in S3: {filename}")
            return True
        
    except Exception as e:
        print(f"Error fetching content: {str(e)}")
        return False
    except ClientError as e:
        print(f"Error uploading to S3: {str(e)}")
        return False


def store_using_beautifulsoup(url, bucket_name, s3_client, short_seller_name, report_name):
    try:
            # Fetch content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Determine content type
        content_type = response.headers.get('content-type', '').lower()
        is_pdf = 'pdf' in content_type or url.lower().endswith('.pdf')
        
        # # Extract company name from URL
        # company = "DGW"  # You might want to make this more dynamic
        # if "DGW" in url:
        #     company = "DGW"
        # # Add more company mappings as needed
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = '.pdf' if is_pdf else '.html'
        filename = f"{report_name}{file_extension}"
        
        # Prepare content and metadata
        if is_pdf:
            content = response.content
            content_type = 'application/pdf'
        else:
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            main_content = soup.find('div', class_='entry-content')
            content = str(main_content) if main_content else response.content
            content_type = 'text/html'
        
        # Upload to S3 with metadata
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"research_reports/{short_seller_name}/{filename}",
            Body=content,
            ContentType=content_type,
            Metadata={
                'source': f'{short_seller_name}',
                'date': timestamp,
                'url': url,
                'content_type': 'pdf' if is_pdf else 'html'
            }
        )
        
        print(f"Successfully stored content in S3: {filename}")
        return True
        
    except Exception as e:
        print(f"Error fetching content: {str(e)}")
        return False
    except ClientError as e:
        print(f"Error uploading to S3: {str(e)}")
        return False