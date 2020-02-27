import boto3
import io
import pandas as pd
import itertools

bucket = 'danieljaegers-data'
key = 'training/iris.csv'
endpoint_name = 'decision-trees'

# Get data from S3
s3 = boto3.client('s3')
f = s3.get_object(Bucket=bucket, Key=key)

# Read the data into a datafrmae
shape = pd.read_csv(io.BytesIO(f['Body'].read()), header=None)

# Take a random sample
a = [50*i for i in range(3)]
b = [40+i for i in range(10)]
indices = [i+j for i,j in itertools.product(a,b)]
test_data = shape.iloc[indices[:-1]]
test_X = test_data.iloc[:,1:]
test_y = test_data.iloc[:,0]

# Convert the dataframe to csv because that is what the endpoint asks for
test_file = io.StringIO()
test_X.to_csv(test_file, header=None, index=None)

# Connect to SageMaker
client = boto3.client('sagemaker-runtime')
response = client.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=test_file.getvalue(),
    ContentType='text/csv',
    Accept='Accept'
)

print(response['Body'].read().decode('ascii'))