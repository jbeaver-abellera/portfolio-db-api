import sys
import logging as logger
import psycopg2
import json
import os
import boto3
from datetime import datetime
import pytz

user_name = os.environ['USERNAME']
password = os.environ['PASSWORD']
rds_host = os.environ['RDS_HOST']
rds_port = os.environ['RDS_PORT']
db_name = os.environ['DB_NAME']

try:
    conn = psycopg2.connect(host=rds_host, user=user_name, password=password, dbname=db_name, port=rds_port)

    # # ------------ Testing Only ------------------ #
    # event, context = '', ''
    # lambda_handler(event=event, context=context)
    # # -------------------------------------------- #
    
except psycopg2.Error as e:
    logger.error("Unexpected error: Could not connect to Postgres instance.")
    logger.error(e)
    sys.exit

logger.info("Success: Connection to RDS Postgres successful!")
    
def lambda_handler(event, context):
    items = []
    # item_count = 0
    
    
    try:
        conn = psycopg2.connect(host=rds_host, user=user_name, password=password, dbname=db_name, port=rds_port)

    except psycopg2.Error as e:
        logger.error("Unexpected error: Could not connect to Postgres instance.")
        logger.error(e)
        sys.exit(1)

    logger.info("Success: Connection to RDS Postgres successful!")
    
    with conn.cursor() as cur:
        table_name = 'view_counter'
        #TO DO: get last data from table, as it is the latest timestamp
        cur.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1")
        logger.info("The following items have been found in the db.")
        last_row = cur.fetchone() #also the last row
        count = last_row[1]
        row_id = last_row[0]
        new_count = last_row[1] + 1
        timestamp = get_timestamp()
        
        
        #TO DO: create a new row with updated view and timestamp.
        cur.execute(f"INSERT INTO {table_name} (id, views, timestamp) VALUES (\'{row_id +1}\', \'{new_count}\', \'{timestamp}\')")
        cur.close()
        
    conn.commit()
            
    logger.info(f"New View Count: {new_count}")
    return {
        'statusCode': 200,
        'body': json.dumps(f'{count}')
    }

def get_timestamp():
    tz = pytz.timezone('Asia/Singapore')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %z")

def get_json(count):
    """Retrieve JSON from server."""
    # Business Logic Goes Here.
    response = {
        "statusCode": 200,
        "headers": {},
        "body": count
    }
    return response

# # ------------ Testing Only ------------------ #
# event, context = '', ''
# lambda_handler(event=event, context=context)
# # -------------------------------------------- #