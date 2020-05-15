import os


def get_filetype(filename):
    filetype = os.path.splitext(filename)[-1][1:].lower()
    return filetype


def clean_path(folder, filename):
    if folder and not folder.endswith('/'):
        folder += '/'
    path = folder + filename

    if '//' in path:
        raise ValueError('Double-forward slashes (\'//\') are not permitted '
                         'by river. Use \'river.read_badpractice_file\' '
                         'if reading such a file is necessary.')
    return path


def clean_bucket(bucket):
    # if '.' in bucket:
    #     raise ValueError('Period characters (\'.\') are not permitted '
    #                      'by river. Use \'river.read_badpractice_file\' '
    #                      'if reading such a file is necessary.')
    prefix = 's3://'
    if bucket.startswith(prefix):
        bucket = bucket[len(prefix):]
    return bucket
