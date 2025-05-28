# LambdaB Setup

This lambda function fetches the Data from S3 & store the data in RDS MySQL DB.

### AWS CloudShell Steps
Follow the steps to create a zip file from scratch using AWS CloudShell

1. Create a directory & files
    ```bash
    mkdir lambdaB
    cd ./lambdaB
    echo pymysql > requirements.txt
    ```
2. Create `lambda_function.py` Python file
Copy the code from ./lambdaB/lambda_function.py & Paste it in Nano Editor
    ```bash
    nano lambda_function.py
    ```
3. Install the dependencies in the current directory & Make a zip file & copy it to S3
    ```bash
    pip install -r requirements.txt -t .
    zip -r lambdaB.zip .
    aws s3 cp lambdaB.zip s3://my-lambda-functions-123/
    ```
### AWS Console Steps
- Create 3 IAM Inline Policy
    - [GetS3@cms-2023-project](../IAMpolicy/GetS3@cms-2023-project.json) to retreive the Json object from S3 Bucket
    - [lambdaInsideVPC](../IAMpolicy/lambdaInsideVPC.json) to create ENI(Elastic Network Interface) to connect with RDS
    - [CloudWatchLogsforLambda](../IAMpolicy/CloudWatchLogsforLambda.json) to create and Put logs in CloudWatch
- Create a new IAM Role `LambdaB` & Attach the above policy
- Create a LambdaB function from AWS Lambda Service
- Choose timeout to `10-15` sec to allow connection to RDS
- Add Environment Variables pertaining to RDS MySQL DB
    - `host` - database.databaseid.us-east-1.rds.amazonaws.com
    - `user` - admin
    - `password` - password
    - `database` - DBname
    - `port` - Port (3306)
- Select the VPC, Private Subnet & Security group
- Use AWS Console to Upload the Zip file from S3 bucket - `s3://my-lambda-functions-123/lambdaB.zip`
- Create a sample test-case & test the function