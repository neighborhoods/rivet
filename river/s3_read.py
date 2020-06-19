import logging
import os
from tempfile import NamedTemporaryFile

import boto3

from river import s3_path_utils
from river.storage_formats import get_storage_fn


def read(path, bucket=os.getenv('RV_DEFAULT_S3_BUCKET'),
         *args, **kwargs):
    """
    Downloads an object from S3 and reads it into the Python session.
    Storage format is determined by file extension, to prevent
    extension-less files in S3.

    Args:
        filename (str): The name of the file to read from in S3
        folder (str, optional): The folder/prefix the file is under in S3
        bucket (str, optional): The S3 bucket to search for the object in
    Returns:
        object: The object downloaded from S3
    """
    filetype = s3_path_utils.get_filetype(path)
    read_fn = get_storage_fn(filetype, 'read')

    path = s3_path_utils.clean_path(path)
    bucket = s3_path_utils.clean_bucket(bucket)

    s3 = boto3.client('s3')
    with NamedTemporaryFile() as tmpfile:
        s3.download_fileobj(bucket, path, tmpfile)
        tmpfile.flush()
        obj = read_fn(tmpfile, *args, **kwargs)
    return obj


def read2(path, bucket=os.getenv('RV_DEFAULT_S3_BUCKET'),
          *args, **kwargs):
    """
    Downloads an object from S3 and reads it into the Python session.
    Storage format is determined by file extension, to prevent
    extension-less files in S3.

    Args:
        filename (str): The name of the file to read from in S3
        folder (str, optional): The folder/prefix the file is under in S3
        bucket (str, optional): The S3 bucket to search for the object in
    Returns:
        object: The object downloaded from S3
    """
    filetype = s3_path_utils.get_filetype(path)
    read_fn = get_storage_fn(filetype, 'read')

    path = s3_path_utils.clean_path(path)
    bucket = s3_path_utils.clean_bucket(bucket)

    s3 = boto3.client('s3')
    with NamedTemporaryFile() as tmpfile:
        s3.download_file(bucket, path, tmpfile.name)
        obj = read_fn(tmpfile, *args, **kwargs)
    return obj


def read_badpractice(path, bucket=os.getenv('RV_DEFAULT_S3_BUCKET'),
                     filetype=None, *args, **kwargs):
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
    Returns:
        object: The object downloaded from S3
    """
    logging.warning('You are using river\'s read function that allows for '
                    'files stored with inadvisible S3 paths. It is highly '
                    'recommended that you use the standard \'read\' '
                    'function to ensure that good naming practices are '
                    'followed.')

    if filetype is None:
        filetype = s3_path_utils.get_filetype(path)

    read_fn = get_storage_fn(filetype, 'read')

    s3 = boto3.client('s3')
    with NamedTemporaryFile() as tmpfile:
        s3.download_fileobj(bucket, path, tmpfile)
        tmpfile.flush()
        obj = read_fn(tmpfile, *args, **kwargs)
    return obj
