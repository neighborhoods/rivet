import os
from tempfile import NamedTemporaryFile

import boto3

from river import s3_path_utils
from river.storage_formats import get_storage_fn


def write(obj, filename, folder='',
          bucket=os.getenv('RV_DEFAULT_S3_BUCKET',
                           'nhds-data-lake-experimental-zone'),
          *args, **kwargs):
    """
    Uploads an object to S3, in a storage format decided by its file extension

    Args:
        obj (object): The object to be uploaded to S3
        filename (str): The filename to save 'obj' as
        folder (str, optional): The folder/prefix to save 'obj' under
        bucket (str, optional): The S3 bucket to save 'obj' in
    Returns:
        str: The full path to the object in S3, without the 's3://' prefix
    """
    filetype = s3_path_utils.get_filetype(filename)
    write_fn = get_storage_fn(filetype, 'write')

    if folder and not folder.endswith('/'):
        folder += '/'

    path = s3_path_utils.clean_path(folder, filename)
    bucket = s3_path_utils.clean_bucket(bucket)

    s3 = boto3.client('s3')
    with NamedTemporaryFile() as tmpfile:
        write_fn(obj, tmpfile, *args, *kwargs)
        s3.upload_file(tmpfile.name, bucket, path)

    return '/'.join([bucket, path])
