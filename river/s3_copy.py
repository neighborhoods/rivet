import os

import boto3

from river import s3_path_utils


def copy(source_filename, source_folder='',
         source_bucket=os.getenv(
             'RV_DEFAULT_S3_BUCKET', 'nhds-data-lake-experimental-zone'),
         dest_filename=None, dest_folder='',
         dest_bucket=os.getenv(
             'RV_DEFAULT_S3_BUCKET', 'nhds-data-lake-experimental-zone')):
    if dest_filename is None:
        dest_filename = source_filename

    source_path = s3_path_utils.clean_path(source_folder, source_filename)
    dest_path = s3_path_utils.clean_path(dest_folder, dest_filename)
    s3 = boto3.client('s3')

    copy_source = {
        'Bucket': source_bucket,
        'Key': source_path
    }

    s3.copy(CopySource=copy_source, Bucket=dest_bucket, Key=dest_path)
