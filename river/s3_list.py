import os
import re

import boto3


def list_objects(bucket=os.getenv('RV_DEFAULT_S3_BUCKET',
                                  'nhds-data-lake-experimental-zone'),
                 folder='', include_folder=False, recursive=False):
    s3 = boto3.client('s3')

    keys = [obj['Key'] for obj in
            s3.list_objects_v2(Bucket=bucket, Prefix=folder)['Contents']]

    if folder and not folder.endswith('/'):
        folder += '/'

    if not recursive:
        keys = list(
            {re.match(folder + r'[\w. ]*/?', key).group() for key in keys}
        )
    if not include_folder:
        keys = [key[len(folder):] for key in keys]

    return keys
