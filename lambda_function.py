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
    
    with conn.cursor() as cur:
        table_name = 'view_counter'
        #TO DO: get last data from table, as it is the latest timestamp
        cur.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1")
        logger.info("The following items have been found in the db.")
        last_row = cur.fetchone() #also the last row
        row_id = last_row[0]
        new_count = last_row[1] + 1
        timestamp = get_timestamp()
        
        
        #TO DO: create a new row with updated view and timestamp.
        cur.execute(f"UPDATE {table_name} SET views={new_count}, timestamp=\'{timestamp}\' WHERE id={row_id}")
        cur.close()
        
    conn.commit()
    # Close the cursor and connection
    conn.close()
        
    logger.info(f"New View Count: {new_count}")
    return items

def get_timestamp():
    tz = pytz.timezone('Asia/Singapore')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %z")


