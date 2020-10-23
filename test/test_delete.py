from river import delete, list_objects


def test_delete(setup_bucket_w_contents, test_bucket, test_keys):
    key = test_keys[0]
    delete(key, test_bucket)
    assert key not in list_objects('', test_bucket,
                                   include_prefix=True, recursive=True)


def test_delete_recursive(setup_bucket_w_contents, test_bucket):
    delete('', test_bucket, recursive=True)
    assert list_objects('', test_bucket) == []
