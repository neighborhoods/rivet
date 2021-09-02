import logging

import boto3

from rivet import s3_path_utils
from rivet.s3_list import list_objects


def delete(path, bucket=None, recursive=False):
    """
    Deletes object(s) at specified path

    Args:
        path (str): The S3 path to the object(s) to be deleted
        bucket (str): The bucket containing the object(s) to be deleted
        recursive (bool):
            Whether to delete all objects in the 'folder' specified in 'path',
            or to just delete a single object.
    """
    if path == '':
        raise ValueError(
            'A delete operation was about to delete the entirety of a bucket. '
            'That seems unsafe, and has been prevented.'
        )
    bucket = bucket or s3_path_utils.get_default_bucket()

    objects = list_objects(path=path, bucket=bucket,
                           include_prefix=True, recursive=True)

    if not objects:
        logging.warn('No objects found for deletion at provided path: '
                     's3://' + '/'.join([bucket, path]))
    if len(objects) > 1 and not recursive:
        raise KeyError(
            'Multiple matching objects found with provided path. '
            'Set "recursive" to True if you wish to delete all of them.')

    s3 = boto3.client('s3')
    for key in objects:
        s3.delete_object(Bucket=bucket, Key=key)
