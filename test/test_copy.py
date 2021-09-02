from tempfile import NamedTemporaryFile

import boto3
import pandas as pd

from rivet import copy


def test_copy(setup_bucket_w_dfs, test_bucket, test_df_keys):
    """
    Tests that the rv.copy successfully copies an object from one
    S3 key to another without mutating it.
    """
    source_path = test_df_keys['csv'][0]

    dot_ind = source_path.find('.')
    dest_path = source_path[:dot_ind] + '_copy' + source_path[dot_ind:]
    print(source_path)
    print(dest_path)
    copy(source_path=source_path, dest_path=dest_path,
         source_bucket=test_bucket, dest_bucket=test_bucket)

    s3 = boto3.client('s3')
    print(s3.list_buckets())
    print(s3.list_objects_v2(Bucket=test_bucket))
    with NamedTemporaryFile() as tmpfile:
        s3.download_file(test_bucket, source_path, tmpfile.name)
        source_df = pd.read_csv(tmpfile.name)
    with NamedTemporaryFile() as tmpfile:
        s3.download_file(test_bucket, dest_path, tmpfile.name)
        dest_df = pd.read_csv(tmpfile.name)

    assert source_df.equals(dest_df)
