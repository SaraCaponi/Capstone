import boto3

from sagemaker.sklearn.estimator import SKLearn

from sagemaker.sklearn.model import SKLearnModel

sm_boto3 = boto3.client('sagemaker')

my_training_job_name = "twitter-svc-2020-03-05-20-11-32-238"
sklearn_estimator = SKLearn.attach(my_training_job_name)

sklearn_estimator.deploy(
    instance_type='ml.c5.large',
    initial_instance_count=1
)
