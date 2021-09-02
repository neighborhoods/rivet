import pickle
from tempfile import NamedTemporaryFile

import boto3
import pandas as pd

from rivet import write


def test_write_csv(setup_bucket_wo_contents, test_bucket,
                   test_df, test_df_keys):
    """Tests that writing files stored as a CSV works properly"""
    s3 = boto3.client('s3')

    for key in test_df_keys['csv']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name)
            assert df.equals(test_df)


def test_write_csv_gz(setup_bucket_wo_contents, test_bucket,
                      test_df, test_df_keys):
    """
    Tests that writing files stored as a gzip-compressed CSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['csv.gz']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".csv.gz") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name)
            assert df.equals(test_df)


def test_write_csv_zip(setup_bucket_wo_contents, test_bucket,
                       test_df, test_df_keys):
    """
    Tests that writing files stored as a zip-compressed CSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['csv.zip']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".csv.zip") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name)
            assert df.equals(test_df)


def test_write_csv_bz2(setup_bucket_wo_contents, test_bucket,
                       test_df, test_df_keys):
    """
    Tests that writing files stored as a bzip2-compressed CSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['csv.bz2']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".csv.bz2") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name)
            assert df.equals(test_df)


def test_write_csv_xz(setup_bucket_wo_contents, test_bucket,
                      test_df, test_df_keys):
    """
    Tests that writing files stored as an xz-compressed CSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['csv.xz']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".csv.xz") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name)
            assert df.equals(test_df)


def test_write_psv(setup_bucket_wo_contents, test_bucket,
                   test_df, test_df_keys):
    """Tests that writing files stored as a PSV works properly"""
    s3 = boto3.client('s3')

    for key in test_df_keys['psv']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name, sep='|')
            assert df.equals(test_df)


def test_write_psv_gz(setup_bucket_wo_contents, test_bucket,
                      test_df, test_df_keys):
    """
    Tests that writing files stored as a gzip-compressed PSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['psv.gz']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".psv.gz") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name, sep='|')
            assert df.equals(test_df)


def test_write_psv_zip(setup_bucket_wo_contents, test_bucket,
                       test_df, test_df_keys):
    """
    Tests that writing files stored as a zip-compressed PSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['psv.zip']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".psv.zip") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name, sep='|')
            assert df.equals(test_df)


def test_write_psv_bz2(setup_bucket_wo_contents, test_bucket,
                       test_df, test_df_keys):
    """
    Tests that writing files stored as a bzip2-compressed PSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['psv.bz2']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".psv.bz2") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name, sep='|')
            assert df.equals(test_df)


def test_write_psv_xz(setup_bucket_wo_contents, test_bucket,
                      test_df, test_df_keys):
    """
    Tests that writing files stored as an xz-compressed PSV works properly
    """
    s3 = boto3.client('s3')

    for key in test_df_keys['psv.xz']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile(suffix=".psv.xz") as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_csv(tmpfile.name, sep='|')
            assert df.equals(test_df)


def test_write_feather(setup_bucket_wo_contents, test_bucket,
                       test_df, test_df_keys):
    """Tests that writing files stored as feather works properly"""
    s3 = boto3.client('s3')

    for key in test_df_keys['feather']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_feather(tmpfile.name)
            assert df.equals(test_df)


def test_write_json(setup_bucket_wo_contents, test_bucket,
                    test_df, test_df_keys):
    """Tests that writing files stored as JSON works properly"""
    s3 = boto3.client('s3')

    for key in test_df_keys['json']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_json(tmpfile.name)
            assert df.equals(test_df)


def test_write_pkl(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that writing pickled files works properly"""
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
    """Tests that writing files stored as Parquet works properly"""
    s3 = boto3.client('s3')

    for key in test_df_keys['pq']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_parquet(tmpfile.name)
            assert df.equals(test_df)


def test_write_avro(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that writing files stored as Avro works properly"""
    s3 = boto3.client('s3')

    for key in test_df_keys['pq']:
        write(test_df, key, test_bucket)

        with NamedTemporaryFile() as tmpfile:
            s3.download_file(test_bucket, key, tmpfile.name)
            df = pd.read_parquet(tmpfile.name)
            assert df.equals(test_df)
