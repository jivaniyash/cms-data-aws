# Serverless Data Ingestion Pipeline using AWS Lambda, S3 & RDS
CMS (Centers for Medicare & Medicaid Services) [API](https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider-and-drug/api-docs) provides information on prescription drugs provided to Medicare beneficiaries enrolled in Part D (Prescription Drug Coverage), by physicians and other health care providers, aggregated by provider and drug in the US.

### Project Scope
For this project, 2023 Year records are used from the cms database. This project showcases how different AWS Services are configured & provisioned to follow AWS best security practices to allow for least privilege by assigning IAM Roles & Policies  

### Data Flow Steps
![Architecture Diagram](<images/AWS Architecture CMS - Lambda & RDS.drawio.png>) 

Following are the steps AWS Services follow - 
1. LambdaA runs the Python scripts to fetch the CMS Data using the CMS API and stores it in an S3 bucket (cms-2023-project)
2. S3 Bucket has an Event Notification triggered, which is configured to run LambdaB once a new object is uploaded successfully in the S3 bucket with the predefined prefix & suffix set for the key name 
3. LambdaB, which is under the Private subnet, follows the steps -
    - Connects to S3 using a VPC Endpoint
    - Retrieves the raw data from the triggered Event Notification
    - Connect to RDS MySQL Database Instance
    - Create the Table if it doesn't exist & store the data

### Additional Notes - 
- LambdaB & RDS Spans to MultiAZ for High Availability (us-east-1a & us-east-1b) (Not shown in Diagram)
- LambdaB & RDS are associated with different security groups to talk to AWS Services securely
- Since RDS is placed inside a private subnet, LambdaB needs to be placed inside a VPC
- IAM Policies are created to allow Lambda A & B to connect with S3 & RDS and are attached to IAM Roles
- VPC Endpoint is configured to allow target S3 requests
- Route Tables are associated with Private Subnets
- Inbound & Outbound rules are set to receive incoming & outgoing traffic to services inside the Security groups

### Project Steps:
1. Create a VPC with 2 Private Subnets & 2 Security Groups and configure firewall rules (Inbound & Outbound)
2. Create a VPC Endpoint using the S3 Gateway service
3. Create a S3 Bucket to store data & allow permissions & configure Event Notification
4. Create LambdaA & LambdaB & follow instructions @ [lambdaA](lambdaA/Instructions.md) & [lambdaB](lambdaB/Instructions.md)
5. Create RDS Instance, configuring MySQLDB Engine, Credentials, Storage & Instance & Connectivity
