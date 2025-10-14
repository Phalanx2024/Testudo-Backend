# Testudo-Backend - Serverless Web Scraping with Playwright and AWS Lambda

## Introduction
This project demonstrates a comprehensive serverless approach to web scraping using [Playwright](https://playwright.dev/) and [AWS Lambda](https://aws.amazon.com/lambda/). The system scrapes research reports from 50+ financial research firms including Hindenburg Research, Viceroy Research, Citron Research, J Capital, and many others.

Serverless web scraping is an efficient solution that allows you to scrape data without maintaining servers and only pay for compute time used during the scraping task.

## Features
- **50+ Research Firm Scrapers**: Comprehensive coverage of major short-seller research firms
- **Comprehensive Logging**: Detailed logging for each scraped report and database operations
- **Database Integration**: Automatic insertion of scraped reports into database
- **AWS Lambda Deployment**: Serverless deployment with optimized resource usage
- **Error Handling**: Robust retry logic and error handling for reliable scraping

## Prerequisites
Before starting, ensure you have the following:

- An AWS account with appropriate permissions
- [AWS CLI](https://aws.amazon.com/cli/) installed and configured
- [Docker](https://www.docker.com/) installed on your local machine
- Basic knowledge of Python and AWS services

**Note for Windows Users:**  
This project uses shell scripts (`.sh` files). Windows users may need [WSL2](https://docs.microsoft.com/en-us/windows/wsl/) or can directly run the AWS CLI commands in the command prompt. Remember to make each script executable by running:
```bash
chmod +x script_name.sh
```

## Project Structure

```bash
├── create_iam_role.sh          # Sets up AWS IAM roles for Lambda permissions
├── deploy.sh                   # Builds Docker image and deploys to Lambda
├── invoke_lambda.sh            # Invokes the Lambda function
├── container/
│   ├── Dockerfile              # Configures the Lambda container
│   ├── lambda_function.py      # Core scraping logic with comprehensive logging
│   ├── run_scrapers.py         # Orchestrates all 50+ scrapers
│   ├── database/               # Database integration modules
│   ├── model/                  # Data models for research reports
│   ├── scrapers/               # Individual scraper implementations
│   └── requirements.txt        # Python dependencies
```

## Supported Research Firms
- Hindenburg Research
- Viceroy Research
- Citron Research
- J Capital
- Kerrisdale Capital
- Wolfpack Research
- Blue Orca Capital
- Spruce Point Management
- And 40+ more research firms

## Steps to Set Up and Run

### Step 1: Setting Up IAM Role

Run create_iam_role.sh to create a role named LambdaPlaywrightRole with the required permissions:

```bash
./create_iam_role.sh
```

### Step 2: Deploying the Lambda Function

To handle complex dependencies, package the function in a Docker container using the Dockerfile. Run deploy.sh to build the Docker image, push it to ECR, and deploy it to Lambda.

```bash
./deploy.sh
```

Note: Modify ECR_ACCOUNT_ID, ECR_REGION, and LAMBDA_ROLE_ARN as needed in deploy.sh.

### Step 3: Testing the Lambda Function

Use invoke_lambda.sh to test the Lambda function:

```bash
# Basic usage
./invoke_lambda.sh
```

The script saves the Lambda response to response.json, allowing you to check the execution details.

## Logging and Monitoring

The system provides comprehensive logging for:
- Each scraped report with source, publication date, title, link, target company, and short seller
- Database write operations with success/failure status
- Total count of scraped reports
- Error handling and retry attempts

## Database Integration

The system automatically:
- Inserts scraped reports into the database
- Logs successful database writes
- Handles database connection errors gracefully
- Provides detailed error reporting

## Conclusion

This comprehensive serverless web scraping solution enables efficient, scalable data collection from 50+ financial research firms. By packaging the function in a Docker container and deploying to AWS Lambda, we ensure reliable, cost-effective scraping operations with detailed logging and database integration.