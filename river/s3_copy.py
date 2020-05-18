import os

import boto3

from river import s3_path_utils


def copy(source_path, dest_path,
         source_bucket=os.getenv('RV_DEFAULT_S3_BUCKET'),
         dest_bucket=os.getenv('RV_DEFAULT_S3_BUCKET')):
    """
    Copy an object from one S3 location into another.

    Args:
        source_filename (str): Filename of file to copy
        source_folder (str): Folder of file to copy
        source_bucket (str): Bucket of file to copy
        dest_filename (str): Filename to copy to.
            Will be set to 'source_filename' if not provided
        dest_folder (str): Folder to copy to
        dest_bucket (str): Bucket to copy to
    """
    source_path = s3_path_utils.clean_path(source_path)
    dest_path = s3_path_utils.clean_path(dest_path)

    s3 = boto3.client('s3')

    copy_source = {
        'Bucket': source_bucket,
        'Key': source_path
    }

    s3.copy(CopySource=copy_source, Bucket=dest_bucket, Key=dest_path)
