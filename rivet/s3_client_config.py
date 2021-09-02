from rivet import get_option
from rivet.s3_progressbar import S3ProgressBar


def get_s3_client_kwargs(path, bucket, operation,
                         show_progressbar):
    """
    Assembles and returns a dictionary of kwargs for the boto3 S3 client to use

    Args:
        path (str): Path to an object in S3 or on the local machine
        bucket (str): The bucket that will be interacted with
        operation (str):
            What type of interaction with S3 will be performed. Possible values
            are 'read', 'write', and 'copy'
        show_progresbar (bool, default True): Whether to show a progress bar
    """
    s3_kwargs = {}
    if show_progressbar and get_option('verbose'):
        progressbar = S3ProgressBar(path, bucket, operation)
        s3_kwargs['Callback'] = progressbar
    return s3_kwargs
