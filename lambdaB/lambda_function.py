import pymysql
import json
import os
import boto3

def lambda_handler(event, context):
    try:        
        s3 = boto3.client('s3')
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_name = event['Records'][0]['s3']['object']['key']
        print(f'Bucket Name: {bucket_name}, File Name: {file_name}')
        
        raw_data = s3.get_object(Bucket=bucket_name, Key=file_name)
        raw_data = json.loads(raw_data['Body'].read()) 
        print('Data retrieved from S3 successfully.')
    except Exception as e:
        print(f'Error: Unable to load data from S3 bucket. Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error loading data from S3: {str(e)}')
        }
    
    # Processing Steps Here ---
    processed_data = raw_data

    host = os.environ.get('host')
    user = os.environ.get('user')
    password = os.environ.get('password')
    database = os.environ.get('database')
    port = int(os.environ.get('port'))

    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connect_timeout=5,
            autocommit=True
        )
        print('Connected to RDS successfully')
    except Exception as e:
        print(f'Error: Unable to connect to RDS. Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error connecting to RDS: {str(e)}')
        }
    
    create_table_query = """
        CREATE TABLE IF NOT EXISTS cms_2023 (
            Prscrbr_NPI INT,
            Prscrbr_Last_Org_Name VARCHAR(255),
            Prscrbr_First_Name VARCHAR(255),
            Prscrbr_City VARCHAR(255),
            Prscrbr_State_Abrvtn VARCHAR(255),
            Prscrbr_State_FIPS VARCHAR(255),
            Prscrbr_Type VARCHAR(255),
            Prscrbr_Type_Src VARCHAR(255),
            Brnd_Name VARCHAR(255),
            Gnrc_Name VARCHAR(255),
            Tot_Clms VARCHAR(255),
            Tot_30day_Fills VARCHAR(255),
            Tot_Day_Suply VARCHAR(255),
            Tot_Drug_Cst VARCHAR(255),
            Tot_Benes VARCHAR(255),
            GE65_Sprsn_Flag VARCHAR(255),
            GE65_Tot_Clms VARCHAR(255),
            GE65_Tot_30day_Fills VARCHAR(255),
            GE65_Tot_Drug_Cst VARCHAR(255),
            GE65_Tot_Day_Suply VARCHAR(255),
            GE65_Bene_Sprsn_Flag VARCHAR(255),
            GE65_Tot_Benes VARCHAR(255)
        )
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
        print('Table created successfully')
    except Exception as e:
        print(f'Error: Unable to create table. Error: {e}')
        return {
            'body': json.dumps(f'Error creating table: {str(e)}')
        }
    
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO cms_2023 (
                    Prscrbr_NPI, Prscrbr_Last_Org_Name, Prscrbr_First_Name, Prscrbr_City, Prscrbr_State_Abrvtn, Prscrbr_State_FIPS, Prscrbr_Type, Prscrbr_Type_Src, Brnd_Name, Gnrc_Name, Tot_Clms, Tot_30day_Fills, Tot_Day_Suply, Tot_Drug_Cst, Tot_Benes, GE65_Sprsn_Flag, GE65_Tot_Clms, GE65_Tot_30day_Fills, GE65_Tot_Drug_Cst, GE65_Tot_Day_Suply, GE65_Bene_Sprsn_Flag, GE65_Tot_Benes
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            for row in processed_data:
                values = (
                        row['Prscrbr_NPI'], row['Prscrbr_Last_Org_Name'], row['Prscrbr_First_Name'], row['Prscrbr_City'],
                        row['Prscrbr_State_Abrvtn'], row['Prscrbr_State_FIPS'], row['Prscrbr_Type'], row['Prscrbr_Type_Src'],
                        row['Brnd_Name'], row['Gnrc_Name'], row['Tot_Clms'], row['Tot_30day_Fills'], row['Tot_Day_Suply'],
                        row['Tot_Drug_Cst'], row['Tot_Benes'], row['GE65_Sprsn_Flag'], row['GE65_Tot_Clms'],
                        row['GE65_Tot_30day_Fills'], row['GE65_Tot_Drug_Cst'], row['GE65_Tot_Day_Suply'], row['GE65_Bene_Sprsn_Flag'], row['GE65_Tot_Benes']
                    )
                cursor.execute(insert_query, values)
        print(f'{len(processed_data)} rows inserted successfully')
        return {
            'statusCode': 200,
            'body': json.dumps(f'{len(processed_data)} rows inserted into RDS successfully')
        }
    except Exception as e:
        print(f'Error: Unable to insert data into RDS. Error: {e}')
        return {
            'body': json.dumps(f'Error inserting data into RDS: {str(e)}')
        }