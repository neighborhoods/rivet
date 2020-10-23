import boto3

from river import s3_path_utils
from river.s3_list import list_objects


def delete(path, bucket=None, recursive=False):
    bucket = bucket or s3_path_utils.get_default_bucket()

    objects = list_objects(path=path, bucket=bucket,
                           include_prefix=True, recursive=True)
    if len(objects) > 1 and not recursive:
        raise KeyError(
            'Multiple matching objects found with provided path. '
            'Set "recursive" to True if you wish to delete all of them.')

    s3 = boto3.client('s3')
    for key in objects:
        s3.delete_object(Bucket=bucket, Key=key)
