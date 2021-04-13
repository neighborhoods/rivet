import logging
from tempfile import NamedTemporaryFile

import boto3

from river import inform, s3_path_utils
from river.s3_client_config import get_s3_client_kwargs
from river.storage_formats import get_storage_fn


def read(path, bucket=None, show_progressbar=True,
         *args, **kwargs):
    """
    Downloads an object from S3 and reads it into the Python session.
    Storage format is determined by file extension, to prevent
    extension-less files in S3.

    Args:
        filename (str): The name of the file to read from in S3
        folder (str, optional): The folder/prefix the file is under in S3
        bucket (str, optional): The S3 bucket to search for the object in
        show_progresbar (bool, default True): Whether to show a progress bar
    Returns:
        object: The object downloaded from S3
    """
    path = s3_path_utils.clean_path(path)
    bucket = bucket or s3_path_utils.get_default_bucket()
    bucket = s3_path_utils.clean_bucket(bucket)

    filetype = s3_path_utils.get_filetype(path)
    read_fn = get_storage_fn(filetype, 'read')

    s3 = boto3.client('s3')
    s3_kwargs = get_s3_client_kwargs(path, bucket,
                                     operation='read',
                                     show_progressbar=show_progressbar)

    with NamedTemporaryFile(suffix='.' + filetype) as tmpfile:
        inform('Downloading from s3://{}/{}...'.format(bucket, path))
        s3.download_file(bucket, path, tmpfile.name, **s3_kwargs)
        inform('Reading from tempfile...')
        obj = read_fn(tmpfile, *args, **kwargs)
    return obj


def read_badpractice(path, bucket=None, filetype=None, show_progressbar=True,
                     *args, **kwargs):
    """
    Downloads an object from S3 and reads it into the Python session,
    without following the rules of the normal reading function.
    Storage format is determined by file extension, or as specified if the
    object is missing one.

    Although this tool aims to enforce good practice, sometimes it is necessary
    to work with other parties who may not follow the same practice, and this
    function allows for users to still read data from those parties
    Usage of this function for production-level code is strongly discouraged.

    Args:
        filename (str): The name of the file to read from in S3
        folder (str, optional): The folder/prefix the file is under in S3
        bucket (str, optional): The S3 bucket to search for the object in
        show_progresbar (bool, default True): Whether to show a progress bar
    Returns:
        object: The object downloaded from S3
    """
    logging.warning('You are using river\'s read function that allows for '
                    'files stored with inadvisible S3 paths. It is highly '
                    'recommended that you use the standard \'read\' '
                    'function to ensure that good naming practices are '
                    'followed.')

    bucket = bucket or s3_path_utils.get_default_bucket()

    if filetype is None:
        filetype = s3_path_utils.get_filetype(path)

    read_fn = get_storage_fn(filetype, 'read')

    s3 = boto3.client('s3')
    s3_kwargs = get_s3_client_kwargs(path, bucket,
                                     operation='read',
                                     show_progressbar=show_progressbar)

    with NamedTemporaryFile(suffix='.' + filetype) as tmpfile:
        inform('Downloading from s3://{}/{}...'.format(bucket, path))
        s3.download_file(bucket, path, tmpfile.name, **s3_kwargs)
        inform('Reading object from tempfile...')
        obj = read_fn(tmpfile, *args, **kwargs)
    return obj


def download_file(path, bucket=None, local_file_path=None,
                  show_progressbar=True):
    """
    Downloads a file from S3 directly to local storage

    Args:
        path (str): The key the file is under in S3
        bucket (str, optional): The S3 bucket to search for the object in
        local_file_path (str): Where to download the file to locally
        show_progresbar (bool, default True): Whether to show a progress bar
    """
    bucket = bucket or s3_path_utils.get_default_bucket()
    if local_file_path is None:
        raise ValueError('A local file path must be provided.')

    s3 = boto3.client('s3')
    s3_kwargs = get_s3_client_kwargs(path, bucket,
                                     operation='read',
                                     show_progressbar=show_progressbar)

    s3.download_file(bucket, path, local_file_path, **s3_kwargs)
