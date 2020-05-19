import os
import re

import boto3

from river import s3_path_utils


def list_objects(folder='',
                 bucket=os.getenv('RV_DEFAULT_S3_BUCKET'),
                 include_folder=False, recursive=False):
    """
    Lists objects in an S3 bucket.

    Args:
        bucket (str): The bucket to list files from
        folder (str, optional): The folder to look in
        include_folder (bool):
            Whether to include the folder in the returned S3 paths
        recursive (bool): Whether to list contents of nested folders
    Returns:
        list<str>: List of S3 paths
    """
    s3 = boto3.client('s3')
    folder = s3_path_utils.clean_folder(folder)

    keys = [obj['Key'] for obj in
            s3.list_objects_v2(Bucket=bucket, Prefix=folder)['Contents']]

    if not recursive:
        keys = list(
            {re.match(folder + r'[\w. ]*/?', key).group() for key in keys}
        )
    if not include_folder:
        keys = [key[len(folder):] for key in keys]

    return keys