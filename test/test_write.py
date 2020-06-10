import pickle
from tempfile import NamedTemporaryFile

import boto3
import pandas as pd

from river import write


def test_write_csv(setup_bucket_wo_contents, test_bucket,
                   test_df, test_df_keys):
    """
    Tests that writing files stored as as CSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['csv']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name)
            assert df.equals(test_df)


def test_write_pkl(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that writing pickled files works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['pkl']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            # Pickle won't be able to read from tmpfile until the connection
            # has been opened post-writing, so we need a nested open.
            with open(tmpfile.name, 'rb') as nested_open_file:
                df = pickle.load(nested_open_file)
                assert df.equals(test_df)


def test_write_pq(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that writing files stored as as Parquet works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['pq']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_parquet(tmpfile.name)
            assert df.equals(test_df)
