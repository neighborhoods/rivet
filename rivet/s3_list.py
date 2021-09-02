import os
import re

import boto3

from rivet import s3_path_utils


def list_objects(path='',
                 bucket=None,
                 matches=None,
                 include_prefix=False, recursive=False):
    """
    Lists objects in an S3 bucket.

    Args:
        path (str, optional): The path to look in
        matches (str, optional):
            Regular expression to match the keys to. Non-matching keys
            will be removed from the returned list. If your regular expression
            includes dynamic matching (e.g., not hard-corded) on the prefix
            of keys, do NOT include the prefix in 'path'. In other words,
            if you're looking to list the objects 'potential_match_0' and
            'potential_match_1' in the folder 'hardcoded_folder_name',
            this is fine:
                list_objects(
                    matches='.*_folder_.*/potential_match_')
            this is fine:
                list_objects(
                    path='hardcoded_folder_name/'
                    matches='potential_match_')
            this is also fine, but discouraged:
                list_objects(
                    path='hardcoded_folder_name/'
                    matches='hardcoded_folder_name/potential_match_')
            this is NOT fine, and will not give desired results:
                list_objects(
                    path='hardcoded_folder_name/'
                    matches='.*_folder_.*/potential_match_')
        bucket (str): The bucket to list files from
        include_prefix (bool):
            Whether to include the objects' prefixes in the returned S3 paths
        recursive (bool): Whether to list contents of nested folders
    Returns:
        list<str>: List of S3 paths
    """
    bucket = bucket or s3_path_utils.get_default_bucket()
    s3 = boto3.client('s3')

    keys = []
    continuation_token = None
    continue_listing = True
    while continue_listing:
        list_kwargs = {}
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(Bucket=bucket, Prefix=path,
                                      **list_kwargs)
        if 'Contents' in response:
            keys.extend([obj['Key'] for obj in response['Contents']])

        continue_listing = response['IsTruncated']
        if continue_listing:
            continuation_token = response['NextContinuationToken']

    if matches:
        if matches.startswith(path):
            matches = matches[len(path):]
        keys = [key for key in keys
                if re.match(re.escape(path) + matches, key)]

    if not recursive:
        keys = list(
            {re.match(re.escape(path) + r'[^/]*/?', key).group()
             for key in keys}
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
