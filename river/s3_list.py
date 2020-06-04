import os
import re

import boto3


def list_objects(path='',
                 bucket=os.getenv('RV_DEFAULT_S3_BUCKET'),
                 include_prefix=False, recursive=False):
    """
    Lists objects in an S3 bucket.

    Args:
        bucket (str): The bucket to list files from
        path (str, optional): The path to look in
        include_prefix (bool):
            Whether to include the objects' prefixes in the returned S3 paths
        recursive (bool): Whether to list contents of nested folders
    Returns:
        list<str>: List of S3 paths
    """
    s3 = boto3.client('s3')

    response = s3.list_objects_v2(Bucket=bucket, Prefix=path)
    if 'Contents' in response:
        keys = [obj['Key'] for obj in response['Contents']]
    else:
        keys = []

    if not recursive:
        keys = list(
            {re.match(path + r'[\w. ]*/?', key).group() for key in keys}
        )
    if '/' in path and not include_prefix:
        keys = [key[path.rfind('/') + 1:] for key in keys]

    return sorted(keys)


def exists(path, bucket=os.getenv('RV_DEFAULT_S3_BUCKET')):
    """
    Checks if an object exists at a specific S3 key

    Args:
        path (str): S3 path to check for object existence at
        bucket (str): S3 bucket to check in

    Returns:
        bool: Whether an object exists at the specified key
    """
    matches = list_objects(path=path,
                           bucket=bucket,
                           include_prefix=True)
    if path in matches:
        return True
    return False
