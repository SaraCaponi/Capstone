import creds

from sagemaker.sklearn.estimator import SKLearn

sklearn_estimator = SKLearn(
    entry_point='svc.py',
    source_dir='svc/',
    role=creds.execution_role,
    train_instance_count=1,
    train_instance_type='ml.m5.large',
    framework_version='0.20.0',
    base_job_name='twitter-svc',
    metric_definitions=[
        {'Name': 'accuracy',
         'Regex': 'Accuracy: ([0-9.]+).*$'}]
)

sklearn_estimator.fit({'train':creds.trainpath, 'test':creds.testpath})
