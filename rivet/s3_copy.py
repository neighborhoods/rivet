import boto3

from rivet import inform, s3_path_utils
from rivet.s3_client_config import get_s3_client_kwargs


def copy(source_path,
         dest_path,
         source_bucket=None,
         dest_bucket=None,
         show_progressbar=True,
         clean_source_path=True):
    """
    Copy an object from one S3 location into another.

    Args:
        source_path (str): Path of file to copy
        dest_path (str): Path to copy file to
        source_bucket (str): Bucket of file to copy
        dest_bucket (str): Bucket to copy to
        show_progressbar (bool, default True): Whether to show a progress bar
    """
    source_bucket = source_bucket or s3_path_utils.get_default_bucket()
    dest_bucket = dest_bucket or s3_path_utils.get_default_bucket()

    if clean_source_path:
        source_path = s3_path_utils.clean_path(source_path)
    dest_path = s3_path_utils.clean_path(dest_path)

    s3 = boto3.client('s3')
    s3_kwargs = get_s3_client_kwargs(source_path, source_bucket,
                                     operation='copy',
                                     show_progressbar=show_progressbar)

    copy_source = {
        'Bucket': source_bucket,
        'Key': source_path
    }

    inform("Copying object from s3://{}/{} to s3://{}/{}".format(
        source_bucket,
        source_path,
        dest_bucket,
        dest_path
    ))
    s3.copy(CopySource=copy_source, Bucket=dest_bucket, Key=dest_path,
            **s3_kwargs)
