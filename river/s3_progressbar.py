import os
import sys

import boto3


class S3ProgressBar(object):
    def __init__(self, path, bucket, operation, width=30, fill_char='█'):
        """
        Creates, updates, and displays an animated progress bar
        for S3 operations

        Args:
            path (str): Path to an object in S3 or on the local machine
            bucket (str): The bucket that will be interacted with
            operation (str):
                What type of interaction with S3 will be performed.
                Possible values are 'read', 'write', and 'copy'
            width (int): How wide the progress bar should be
            fill_char (str):
                The character that should be used to fill the progress bar
        """
        self.width = width
        self.fill_char = fill_char

        self.progress = 0

        if operation == 'read':
            self.filesize = self._get_s3_filesize(path, bucket)
        elif operation == 'write':
            self.filesize = os.stat(path).st_size
        elif operation == 'copy':
            self.filesize = self._get_s3_filesize(path, bucket)

    def __call__(self, new_progress):
        """
        Updates and displays the progress bar upon each callback
        from the S3 client

        Args:
            new_progress (int):
                How much progress, in bytes, has been made in the
                S3 operation since the last callback
        """
        self.progress += new_progress
        pct_progress = float(self.progress) / float(self.filesize)

        filled_blocks = int(self.width * pct_progress)
        blank_blocks = self.width - filled_blocks

        if filled_blocks == self.width:
            line_end_char = '\n'
        else:
            line_end_char = '\r'
        _ = sys.stdout.write(
                '    |{}{}| ({:.2f}%){}'.format(
                    self.fill_char * filled_blocks,
                    ' ' * blank_blocks,
                    pct_progress * 100,
                    line_end_char))

        sys.stdout.flush()

    def _get_s3_filesize(self, path, bucket):
        """
        Gets the size, in bytes, of an object in S3

        Args:
            path (str): Path to an object in S3
            bucket (str): The bucket that will be interacted with
        """
        s3 = boto3.client('s3')
        return s3.get_object(
            Bucket=bucket, Key=path)['ContentLength']
