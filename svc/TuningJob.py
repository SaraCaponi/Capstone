import sagemaker
from sagemaker.tuner import ContinuousParameter, CategoricalParameter

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

hyperparameter_ranges = {
    'use_idf': CategoricalParameter(['true', 'false']),
    'smooth_idf': CategoricalParameter(['true', 'false']),
    'sublinear_tf': CategoricalParameter(['true', 'false']),
    'C': ContinuousParameter(0.0001, 100, 'Logarithmic')
    # 'penalty': CategoricalParameter(['l1', 'l2']),
    # 'loss': CategoricalParameter(['hinge', 'squared_hinge'])
}

Optimizer = sagemaker.tuner.HyperparameterTuner(
    estimator=sklearn_estimator,
    hyperparameter_ranges=hyperparameter_ranges,
    base_tuning_job_name='twitter-svc-tuner',
    objective_type='Maximize',
    objective_metric_name='accuracy',
    metric_definitions=[
        {'Name': 'accuracy',
         'Regex': 'Accuracy: ([0-9.]+).*$'}
    ],
    max_jobs=20,
    max_parallel_jobs=3
)

Optimizer.fit({'train':creds.trainpath, 'test':creds.testpath})

# results = Optimizer.analytics().dataframe()
# print(results.head())
