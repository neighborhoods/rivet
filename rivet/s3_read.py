import logging
from tempfile import NamedTemporaryFile

import boto3

from rivet import inform, s3_path_utils
from rivet.s3_client_config import get_s3_client_kwargs
from rivet.storage_formats import get_storage_fn


def read(path, bucket=None, show_progressbar=True,
         *args, **kwargs):
    """
    Downloads an object from S3 and reads it into the Python session.
    Storage format is determined by file extension, to prevent
    extension-less files in S3.

    Args:
        path (str): The path of the file to read from in S3
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


def read_df_in_chunks(path, bucket=None, chunk_size=10000, names=None,
                      show_progressbar=True, *args, **kwargs):
    """
    Downloads a DataFrame from S3 and reads it into the Python session in
    chunks of a specified number of rows.
    Because chunking is accomplished via splitting on rows, only textfiles
    (CSVs/PSVs) and compressed textfiles are currently supported.
    Support for reading Avro files in chunks may be added at a later date.
    Storage format is determined by file extension, to prevent
    extension-less files in S3.

    Args:
        path (str): The path of the file to read from in S3
        bucket (str, optional): The S3 bucket to search for the object in
        chunk_size (int, default 10000):
            The number of rows to read for each chunk
        names (list<str>, optional):
            Column names to apply to the chunk DataFrames. If left 'None',
            column names will be inferred by pandas.
        show_progresbar (bool, default True): Whether to show a progress bar
    Yields:
        df (pd.DataFrame):
            The chunk DataFrames read from the file downloaded from S3
    """
    row_chunkable_filetypes = ['csv', 'csv.gz', 'csv.zip', 'csv.bz2', 'csv.xz',
                               'psv', 'psv.gz', 'psv.zip', 'psv.bz2', 'psv.xz']

    path = s3_path_utils.clean_path(path)
    bucket = bucket or s3_path_utils.get_default_bucket()
    bucket = s3_path_utils.clean_bucket(bucket)

    filetype = s3_path_utils.get_filetype(path)
    if filetype not in row_chunkable_filetypes:
        raise IOError(
            'Reading files in chunks is only supported with the following '
            'formats: ' + ','.join(row_chunkable_filetypes)
        )
    read_fn = get_storage_fn(filetype, 'read')

    s3 = boto3.client('s3')
    s3_kwargs = get_s3_client_kwargs(path, bucket,
                                     operation='read',
                                     show_progressbar=show_progressbar)

    with NamedTemporaryFile(suffix='.' + filetype) as tmpfile:
        inform('Downloading from s3://{}/{}...'.format(bucket, path))
        s3.download_file(bucket, path, tmpfile.name, **s3_kwargs)
        df_chunker = read_fn(tmpfile, names=names, chunksize=chunk_size,
                             *args, **kwargs)

        row_number = 0
        for chunk in df_chunker:
            row_number += 1
            inform('Reading from tempfile (chunk #{})...'.format(row_number))
            yield chunk


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
        path (str): The path of the file to read from in S3
        bucket (str, optional): The S3 bucket to search for the object in
        filetype (str, optional):
            The filetype of the file being read. Can be used if a file was
            saved without a proper extension.
        show_progresbar (bool, default True): Whether to show a progress bar
    Returns:
        object: The object downloaded from S3
    """
    logging.warning('You are using rivet\'s read function that allows for '
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
