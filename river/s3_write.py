import os
from tempfile import NamedTemporaryFile

import boto3

from river import s3_path_utils
from river.storage_formats import get_storage_fn


def write(obj, path, bucket=os.getenv('RV_DEFAULT_S3_BUCKET'),
          *args, **kwargs):
    """
    Writes an object to a specified file format and uploads it to S3.
    Storage format is determined by file extension, to prevent
    extension-less files in S3.

    Args:
        obj (object): The object to be uploaded to S3
        filename (str): The path to save obj to
        bucket (str, optional): The S3 bucket to save 'obj' in
    Returns:
        str: The full path to the object in S3, without the 's3://' prefix
    """
    filetype = s3_path_utils.get_filetype(path)
    write_fn = get_storage_fn(filetype, 'write')

    path = s3_path_utils.clean_path(path)
    bucket = s3_path_utils.clean_bucket(bucket)

    s3 = boto3.client('s3')
    with NamedTemporaryFile() as tmpfile:
        write_fn(obj, tmpfile, *args, *kwargs)
        s3.upload_file(tmpfile.name, bucket, path)

    return '/'.join([bucket, path])
