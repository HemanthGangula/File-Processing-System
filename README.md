# File Processing System

## Overview
This project implements a **serverless file processing system** using **AWS Lambda, S3, and DynamoDB**. The system automatically processes CSV files uploaded to an S3 bucket, extracts metadata, and stores it in a DynamoDB table. This is designed with **least privilege access control** and can handle files up to **10MB**.

## Features
- **Automatic Processing:** Uploading a CSV file to the S3 bucket triggers a Lambda function.
- **Metadata Extraction:** The Lambda function extracts relevant metadata (row count, column count, column names, etc.).
- **Storage in DynamoDB:** The extracted metadata is stored in a DynamoDB table.
- **Minimal Permissions:** Follows the principle of least privilege, ensuring secure access.
- **Fully Customizable:** Can be adapted for different file formats, metadata extraction logic, and database choices.

## Architecture
1. A **CSV file** is uploaded to **`<bucket_name>`**.
2. An **S3 event** triggers **Lambda (`<lambda_function_name>`)**.
3. **Lambda extracts metadata** and stores it in **DynamoDB (`<database_name>`)**.
4. (Optional) A notification mechanism can be integrated.

## Setup Instructions
### 1. IAM Role Setup
Create an **IAM Role (`<iam_role_name>`)** with permissions to access **S3, Lambda, DynamoDB, and CloudWatch Logs**.

### 2. S3 Bucket Setup
Create an **S3 bucket (`<bucket_name>`)** and set up an event notification to trigger Lambda on `PutObject` events for `.csv` files.

### 3. DynamoDB Table Setup
Create a **DynamoDB table (`<database_name>`)** with:
- **Partition Key:** `filename` (String)
- **Sort Key:** `upload_timestamp` (Number)

### 4. Lambda Function Setup
- Create a **Lambda function (`<lambda_function_name>`)** with **Python 3.12** runtime.
- Attach the **IAM Role (`<iam_role_name>`)**.
- Configure **environment variables**:
  ```plaintext
  S3_BUCKET_NAME = <bucket_name>
  DYNAMODB_TABLE = <database_name>
  ```
- Set **memory: 256MB**, **timeout: 30s**, **ephemeral storage: 512MB**.
- Attach **S3 trigger** with **suffix `.csv`** and enable **recursive invocation prevention**.

## Deployment
### 1. Install Dependencies
Ensure you have **AWS CLI** and required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Package and Upload Lambda Code
Run the following commands to update the Lambda function:
```bash
rm function.zip
zip -r function.zip . -x "*.zip" "*.pyc" "__pycache__/*"
aws lambda update-function-code --function-name <lambda_function_name> --zip-file fileb://function.zip --region us-east-1
```

### 3. Verify Data in DynamoDB
Check if metadata is stored correctly in DynamoDB:
```bash
aws dynamodb scan --table-name <database_name>
```

## Limitations
- Designed for **CSV files up to 10MB**.

## Customization
This system can be modified to:
- Process **different file types (JSON, XML, etc.)**.
- Extract **custom metadata fields**.
- Integrate **notification mechanisms** (SNS, SQS, etc.).
- Use **alternative databases** (RDS, Elasticsearch, etc.).

## Conclusion
This project provides a **scalable, serverless, and secure** file processing solution using AWS services. It follows best practices like **least privilege IAM policies** and **event-driven automation**. Future improvements can include **error handling, notifications, and local development using LocalStack**.

---
**Note:** Ensure that **`<bucket_name>`**, **`<database_name>`**, **`<lambda_function_name>`**, and **`<iam_role_name>`** are replaced with the actual resource names in your AWS account.

