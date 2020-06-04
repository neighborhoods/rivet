import os

import boto3
from moto import mock_s3
import pytest


@pytest.fixture(autouse=True, scope='session')
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture
def test_bucket():
    return 'test_bucket'


@pytest.fixture
def test_keys():
    return sorted([
        'test_key_0.csv',
        'folder0/test_key_1.pq',
        'folder1/test_key_2.pkl',
        'folder1/subfolder0/test_key_3.pkl',
        'folder2/'
    ])


@pytest.fixture
def setup_bucket_w_contents(test_bucket, test_keys):
    with mock_s3():
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=test_bucket)

        for key in test_keys:
            s3.put_object(Bucket=test_bucket, Key=key, Body='')
        yield


@pytest.fixture
def setup_bucket_wo_contents(test_bucket):
    with mock_s3():
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=test_bucket)

        yield
