import os
import re


def get_filetype(filename):
    """
    Gets the filetype of an object based on the extension in its filename

    Args:
        filename (str): The name of the file
    Returns:
        str: The filetype of the file
    """
    # If the filename isn't named according to good practice,
    # this will return nonsense - which is good. If someone is using
    # read_badpractice with an unclear file type, they should have to specify
    filetype = '.'.join(filename.split('.')[1:])
    if filetype == '':
        raise ValueError('S3 path must contain an extension designating '
                         'a valid file type. If you are reading a file, '
                         'that does not have an extension, you can use '
                         '\'rv.read_badpractice\'.')
    return filetype


def clean_folder(folder):
    if folder and not folder.endswith('/'):
        folder += '/'

    return folder


def clean_path(path):
    """
    Ensures that a provided S3 path follows the convention enforced by rivet

    Args:
        path (str): The S3 path being cleaned
        filename (str): The filename portion of a full S3 path
    Returns:
        str: The full, cleaned S3 path
    Raises:
        ValueError: If 'path' violates rivet's S3 path conventions
    """
    if '//' in path:
        raise ValueError('Double-forward slashes (\'//\') are not permitted '
                         'by rivet. Use \'rivet.read_badpractice_file\' '
                         'if reading such a file is necessary.')

    if re.search(r'\.\.', path):
        raise ValueError('Double-dots (\'..\') are not permitted by rivet.')

    if (path.find('.') < path.rfind('/')) and (path.find('.') != -1):
        raise ValueError('Period characters (\'.\') are not permitted '
                         ' by rivet except in file extensions.')
    return path


def clean_bucket(bucket):
    """
    Cleans an S3 bucket string to ensure that functionality works regardless
    of certain user behavior (e.g. including 's3://' in the bucket string)

    Args:
        bucket (str): The name of an S3 bucket

    Returns:
        str: The cleaned S3 bucket name
    """
    prefix = 's3://'
    if bucket.startswith(prefix):
        bucket = bucket[len(prefix):]
    return bucket


def get_default_bucket():
    try:
        bucket = os.environ['RV_DEFAULT_S3_BUCKET']
    except KeyError as e:
        raise Exception('Target bucket must be defined either as an '
                        'argument or via the environment variable '
                        '\'RV_DEFAULT_S3_BUCKET\'') from e
    return bucket
