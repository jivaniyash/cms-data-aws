from datetime import datetime
import json
import requests
import boto3

def lambda_handler(event, context):
    # Gather info from CMS Data
    uuid = 'e54db557-cd82-4e91-a0fe-61aad5865d69' # 2023 version uuid
    offset = 5 
    data_limit = 5 # custom data limit set
    
    try:
        url = f'https://data.cms.gov/data-api/v1/dataset/{uuid}/data?offset={offset}&size={data_limit}'
        r = requests.get(url)
        data = r.json()
        print('CMS Data has retreived Successfuly. Putting in the S3 ...')
    except Exception as e:
        print(f'Error: Unable to retreive data from CMS Data. Error:{e}')

    # put the Json in S3 bucket
    json_body = json.dumps(data)
    bucket_name = 'cms-2023-project'
    now = datetime.now().strftime('%Y%m%dT%H%M%S')
    file_name = f'data-{now}.json'
    try:
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=json_body)
        print(f'{file_name} has uploaded in {bucket_name}.')
    except Exception as e:
        print(f'Error: Unable to put data in S3 bucket. Error:{e}')

    return {
        'statusCode': 200,
        'body': json.dumps('Data Retrieved & stored Successfully'),
    }