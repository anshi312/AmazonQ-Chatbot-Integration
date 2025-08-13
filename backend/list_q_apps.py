import boto3

client = boto3.client(
    'qbusiness',
    region_name='us-east-1',
    aws_access_key_id='XXXX',
    aws_secret_access_key='XXXXX+XX'
)

response = client.list_applications()
for app in response['applications']:
    print("App ID:", app['applicationId'], "| Name:", app.get('name', 'N/A'))
