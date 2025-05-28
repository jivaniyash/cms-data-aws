# LambdaA Setup

This lambda function fetches the CMS Data using API (Internet Access) & store the raw data in S3 bucket.

### AWS CloudShell Steps
Follow the steps to create a zip file from scratch using AWS CloudShell

1. Create a directory & files
```bash
mkdir lambdaA
cd ./lambdaA
echo requests > requirements.txt
```
2. Create `lambda_function.py` Python file
Copy the code from ./lambdaA/lambda_function.py & Paste it in Nano Editor
```bash
nano lambda_function.py
```
3. Install the dependencies in the current directory & Make a zip file & copy it to S3
```bash
pip install -r requirements.txt -t .
zip -r lambdaA.zip .
aws s3 cp lambdaA.zip s3://my-lambda-functions-123/
```

### AWS Console Steps
- Create 2 IAM Inline Policy
    - [PutS3@cms-2023-project](../IAMpolicy/PutS3@cms-2023-project.json) to Put Json objects in S3 Bucket 
    - [CloudWatchLogsforLambda](../IAMpolicy/CloudWatchLogsforLambda.json) to create and Put logs in CloudWatch
- Create a new IAM Role `LambdaA` & attach the above policy 
- Create a LambdaA function from AWS Lambda Service
- Use AWS Console to Upload the Zip file from S3 bucket - `s3://my-lambda-functions-123/lambdaA.zip`
- Create a sample test-case & test the function