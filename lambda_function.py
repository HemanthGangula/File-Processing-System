import os
import json
import boto3
import pandas as pd
import urllib.parse
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            file_key = record['s3']['object']['key']
            file_key = urllib.parse.unquote_plus(file_key)

            file_path = f"/tmp/{os.path.basename(file_key)}"
            s3_client.download_file(bucket_name, file_key, file_path)

            df = pd.read_csv(file_path)
            row_count = len(df)
            column_count = len(df.columns)
            column_names = list(df.columns)

            response = s3_client.head_object(Bucket=bucket_name, Key=file_key)
            file_size_bytes = response['ContentLength']

            metadata = {
                'filename': file_key,
                'upload_timestamp': int(datetime.utcnow().timestamp()),
                'file_size_bytes': file_size_bytes,
                'row_count': row_count,
                'column_count': column_count,
                'column_names': column_names
            }

            table = dynamodb.Table(DYNAMODB_TABLE)
            table.put_item(Item=metadata)

            print(f"✅ Successfully processed {file_key} and stored metadata in DynamoDB")

        return {
            'statusCode': 200,
            'body': json.dumps('Processing successful!')
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }
