from tempfile import NamedTemporaryFile

import boto3

from river import s3_path_utils
from river.s3_client_config import get_s3_client_kwargs
from river.storage_formats import get_storage_fn


def write(obj, path, bucket=None,
          show_progressbar=True, *args, **kwargs):
    """
    Writes an object to a specified file format and uploads it to S3.
    Storage format is determined by file extension, to prevent
    extension-less files in S3.

    Args:
        obj (object): The object to be uploaded to S3
        filename (str): The path to save obj to
        bucket (str, optional): The S3 bucket to save 'obj' in
        show_progresbar (bool, default True): Whether to show a progress bar
    Returns:
        str: The full path to the object in S3, without the 's3://' prefix
    """
    bucket = bucket or s3_path_utils.get_default_bucket()

    filetype = s3_path_utils.get_filetype(path)
    write_fn = get_storage_fn(filetype, 'write')

    path = s3_path_utils.clean_path(path)
    bucket = s3_path_utils.clean_bucket(bucket)

    s3 = boto3.client('s3')

    with NamedTemporaryFile() as tmpfile:
        print('Writing object to tempfile...')
        write_fn(obj, tmpfile, *args, **kwargs)
        s3_kwargs = get_s3_client_kwargs(tmpfile.name, bucket,
                                         operation='write',
                                         show_progressbar=show_progressbar)
        print('Uploading to s3://{}/{}...'.format(bucket, path))
        s3.upload_file(tmpfile.name, bucket, path, **s3_kwargs)

    return '/'.join([bucket, path])
