import logging
import os
from tempfile import NamedTemporaryFile

import boto3

from river import s3_path_utils
from river.storage_formats import get_storage_fn


def read(filename, folder='',
         bucket=os.getenv('RV_DEFAULT_S3_BUCKET',
                          'nhds-data-lake-experimental-zone'),
         *args, **kwargs):
    filetype = s3_path_utils.get_filetype(filename)
    read_fn = get_storage_fn(filetype, 'read')

    if folder and not folder.endswith('/'):
        folder += '/'

    path = s3_path_utils.clean_path(folder, filename)
    bucket = s3_path_utils.clean_bucket(bucket)

    s3 = boto3.client('s3')
    with NamedTemporaryFile() as tmpfile:
        s3.download_file(bucket, path, tmpfile.name)
        obj = read_fn(tmpfile, *args, **kwargs)
    return obj


def read_badpractice(filename, folder='',
                     bucket=os.getenv('RV_DEFAULT_S3_BUCKET',
                                      'nhds-data-lake-experimental-zone'),
                     filetype=None, *args, **kwargs):

    logging.warning('You are using river\'s read function that allows for '
                    'files stored with inadvisible S3 paths. It is highly '
                    'recommended that you use the standard \'read\' '
                    'function to ensure that good naming practices are '
                    'followed.')

    if filetype is None:
        filetype = s3_path_utils.get_filetype(filename)

    read_fn = get_storage_fn(filetype, 'read')

    path = folder + filename

    s3 = boto3.client('s3')
    with NamedTemporaryFile() as tmpfile:
        s3.download_file(bucket, path, tmpfile.name)
        obj = read_fn(tmpfile, *args, **kwargs)
    return obj
