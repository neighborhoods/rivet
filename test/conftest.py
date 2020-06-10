import os
from tempfile import NamedTemporaryFile

import boto3
from moto import mock_s3
import pandas as pd
import pickle
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
def test_df_keys():
    return {
        'csv': ['df.csv'],
        'pkl': ['df.pkl', 'df.pickle'],
        'pq': ['df.pq', 'df.parquet']
    }


@pytest.fixture
def test_df():
    return pd.DataFrame({
        'intcol': [1, 2, 3],
        'strcol': ['four', 'five', 'six'],
        'floatcol': [7.0, 8.0, 9.0]
    })


@pytest.fixture
def mock_s3_client():
    with mock_s3():
        yield


@pytest.fixture
def setup_bucket_w_contents(mock_s3_client, test_bucket, test_keys):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=test_bucket)

    for key in test_keys:
        s3.put_object(Bucket=test_bucket, Key=key, Body='')
    yield


@pytest.fixture
def setup_bucket_wo_contents(mock_s3_client, test_bucket):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=test_bucket)

    yield


@pytest.fixture
def setup_bucket_w_dfs(mock_s3_client, test_bucket, test_df, test_df_keys):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=test_bucket)

    for key in test_df_keys['csv']:
        with NamedTemporaryFile() as tmpfile:
            test_df.to_csv(tmpfile.name, index=False)
            s3.upload_file(tmpfile.name, test_bucket, key)

    for key in test_df_keys['pkl']:
        with NamedTemporaryFile() as tmpfile:
            pickle.dump(test_df, tmpfile, protocol=pickle.HIGHEST_PROTOCOL)
            tmpfile.flush()
            s3.upload_file(tmpfile.name, test_bucket, key)

    for key in test_df_keys['pq']:
        with NamedTemporaryFile() as tmpfile:
            test_df.to_parquet(tmpfile.name, index=False)
            s3.upload_file(tmpfile.name, test_bucket, key)

    yield
