import boto3
import json
import creds

runtime = boto3.client('sagemaker-runtime')

response = runtime.invoke_endpoint(
    EndpointName='twitter-svc-2020-03-05-20-11-32-238',
    Body=json.dumps(creds.tweets),
    ContentType='application/json')

print(response['Body'].read())
