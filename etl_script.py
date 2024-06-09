import os
import time
import psycopg2
import boto3
from botocore.exceptions import ClientError
import environ
# Set Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'time_stamp_project_Cloud.settings')

env = environ.Env()
environ.Env.read_env()
# Initialize Django
import django

django.setup()


# Ensure the database is ready
def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname='transcribed_data',
                user='postgres',
                password='secret',
                host='db',  # Docker service name for the database
                port='5432'
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Waiting for the database to be ready...")
            time.sleep(5)


wait_for_db()

# Fetch data from PostgreSQL
conn = psycopg2.connect(
    dbname='transcribed_data',
    user='postgres',
    password='secret',
    host='db',  # Docker service name for the database
    port='5432'
)
cur = conn.cursor()

cur.execute('SELECT video_id, chapter_titles FROM timestamp_video;')
pg_data = cur.fetchall()

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb',
                          region_name=env('AWS_DEFAULT_REGION'),
                          aws_access_key_id=env('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=env('AWS_SECRET_ACCESS_KEY')
                          )

# Create DynamoDB table (if it doesn't exist already)
table_name = 'timestamp_video'
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'video_id',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'video_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)  # Wait for table creation
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print(f"Table {table_name} already exists.")
        table = dynamodb.Table(table_name)
    else:
        raise

# Insert PostgreSQL data into DynamoDB
with table.batch_writer() as batch:
    for row in pg_data:
        chapter_titles = [{'timestamp': title[0], 'description': title[1]} for title in row[1]]

        item = {
            'video_id': row[0],
            'chapter_titles': chapter_titles
        }
        batch.put_item(Item=item)

# Close PostgreSQL connection
cur.close()
conn.close()
