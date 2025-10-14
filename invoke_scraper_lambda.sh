#!/bin/bash

# Variables
FUNCTION_NAME="lambda_playwright_scrapers"

echo "Invoking Scraper Lambda function..."

# Create the payload for scraper testing
PAYLOAD=$(cat << EOF
{
    "upload_to_s3": false
}
EOF
)

# Invoke Lambda and save response
aws lambda invoke \
    --function-name $FUNCTION_NAME \
    --payload "$PAYLOAD" \
    --cli-binary-format raw-in-base64-out \
    response.json

# Check if invocation was successful
if [ $? -eq 0 ]; then
    echo "Lambda invoked successfully!"
    echo "Response saved to response.json"
    cat response.json
else
    echo "Error invoking Lambda function"
    exit 1
fi



