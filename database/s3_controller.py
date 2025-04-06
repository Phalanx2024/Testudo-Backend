from boto3.s3 import S3Client

s3 = S3Client()

# Upload a file
def upload_handler(file_data, filename):
    try:
        s3_key = f"uploads/{filename}"
        s3_url = s3.upload_file(file_data, s3_key)
        return {"success": True, "url": s3_url}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Download a file
def download_handler(key):
    try:
        file_data = s3.get_file(key)
        return file_data
    except Exception as e:
        return {"error": str(e)}

# List files
def list_files_handler():
    try:
        files = s3.list_files()
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

# Generate temporary download URL
def get_download_url(key):
    try:
        url = s3.generate_presigned_url(key)
        return {"url": url}
    except Exception as e:
        return {"error": str(e)}