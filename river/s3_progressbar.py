import os
import sys

import boto3


class S3ProgressBar(object):
    def __init__(self, path, bucket, operation, width=30, fill_char='█'):
        self.width = width
        self.fill_char = fill_char

        self.progress = 0

        if operation == 'read':
            self.filesize = self._get_s3_filesize(path, bucket)
            verb = 'Reading'
        elif operation == 'write':
            self.filesize = os.stat(path).st_size
            verb = 'Writing'
        elif operation == 'copy':
            self.filesize = self._get_s3_filesize(path, bucket)
            verb = 'Copying'

        sys.stdout.write('{} {}...\n'.format(
            verb,
            path
        ))

    def __call__(self, new_progress):
        self.progress += new_progress
        # self.bar.show_progress()
        pct_progress = float(self.progress) / float(self.filesize)
        filled_blocks = int(self.width * pct_progress)
        blank_blocks = self.width - filled_blocks
        _ = sys.stdout.write('    |{}{}| ({:.2f}%)\r'.format(
            self.fill_char * filled_blocks,
            ' ' * blank_blocks,
            pct_progress * 100)
        )
        sys.stdout.flush()

    def _get_s3_filesize(self, path, bucket):
        s3 = boto3.client('s3')
        self.filesize = s3.get_object(
            Bucket=bucket, Key=path)['ContentLength']
