import boto3

session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    endpoint_url='https://hb.bizmrg.com'
)
test_bucket_name = 'boto3-test-bucket-name'
# Создание бакета
s3_client.create_bucket(Bucket=test_bucket_name)
