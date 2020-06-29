from river.s3_progressbar import S3ProgressBar


def get_s3_client_kwargs(path, bucket,
                         show_progressbar):
    s3_kwargs = {}
    if show_progressbar:
        progressbar = S3ProgressBar(path, bucket)
        s3_kwargs['Callback'] = progressbar
    return s3_kwargs
