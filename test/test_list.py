from rivet import list_objects, exists


def test_list_objects_w_objects(setup_bucket_w_contents,
                                test_bucket, test_keys):
    """
    Tests that rv.list successfully returns a sorted list of keys
    present in a bucket
    """
    keys_wo_prefix = list({key if '/' not in key else key[:key.find('/') + 1]
                           for key in test_keys})
    objects = list_objects(bucket=test_bucket)
    assert objects == sorted(keys_wo_prefix)


def test_list_objects_wo_objects(setup_bucket_wo_contents,
                                 test_bucket):
    """Tests that rv.list returns an empty list when no keys are present"""
    objects = list_objects(bucket=test_bucket)
    assert objects == []


def test_list_objects_include_prefix(setup_bucket_w_contents,
                                     test_bucket, test_keys):
    """
    Tests that the 'include_prefix' functionality successfully includes
    prefixes of matching keys
    """
    key_w_nested_folder = get_key_w_nested_folder(test_keys)
    prefix = key_w_nested_folder.split('/', 1)[0] + '/'

    keys_w_prefix = []
    for key in test_keys:
        if key.startswith(prefix):
            if key[len(prefix):].count('/') == 0:
                keys_w_prefix.append(key)
            else:
                keys_w_prefix.append(key[:key.find('/', len(prefix)) + 1])

    objects = list_objects(path=prefix, bucket=test_bucket,
                           include_prefix=True)

    assert objects == sorted(keys_w_prefix)


def test_list_objects_recursive(setup_bucket_w_contents,
                                test_bucket, test_keys):
    """
    Tests that the 'recursive' functionality successfully includes any
    nested keys
    """
    key_w_nested_folder = get_key_w_nested_folder(test_keys)
    prefix = key_w_nested_folder.split('/', 1)[0] + '/'

    recursive_keys = [key[len(prefix):] for key in test_keys
                      if key.startswith(prefix)]
    objects = list_objects(path=prefix, bucket=test_bucket,
                           recursive=True)
    assert objects == sorted(recursive_keys)


def test_list_objects_include_prefix_and_recursive(setup_bucket_w_contents,
                                                   test_bucket, test_keys):
    """
    Tests that 'include_prefix' and 'recursive' work properly together
    """
    key_w_nested_folder = get_key_w_nested_folder(test_keys)
    prefix = key_w_nested_folder.split('/', 1)[0] + '/'
    recursive_keys_w_prefix = [key for key in test_keys
                               if key.startswith(prefix)]

    objects = list_objects(path=prefix, bucket=test_bucket,
                           include_prefix=True, recursive=True)
    assert objects == sorted(recursive_keys_w_prefix)


def test_exists_w_object_present(setup_bucket_w_contents,
                                 test_bucket, test_keys):
    """Tests that rv.exists will return True if a matching path is found"""
    assert exists(test_keys[0], test_bucket)


def test_exists_wo_object_present(setup_bucket_wo_contents,
                                  test_bucket, test_keys):
    """Tests that rv.exists will return False if no matching path is found"""
    assert not exists(test_keys[0], test_bucket)


def test_exists_only_exact_match(setup_bucket_w_contents,
                                 test_bucket, test_keys):
    """
    Tests that rv.exists will only return True in
    the case of an exact match
    """
    key = test_keys[0]
    partial_key = key[:len(key) - 1]
    assert not exists(partial_key[0], test_bucket)


def test_list_regexp_matching(setup_bucket_w_contents,
                              test_bucket, test_keys):
    """
    Tests that regular expression matching only returns keys that match
    the provided regular expression.
    """
    key_w_folder = get_key_w_folder_wo_nested_folder(test_keys)
    prefix, filename = key_w_folder.split('/')
    prefix += '/'
    filetype = key_w_folder.rsplit('.', 1)[-1]

    expected_keys = [filename]
    matches = r'.*\.' + filetype
    keys = list_objects(path=prefix, bucket=test_bucket, matches=matches)

    assert keys == expected_keys


def test_list_regexp_matching_recursive(setup_bucket_w_contents,
                                        test_bucket, test_keys):
    """
    Tests that regular expression matching properly handles the
    recursive parameter
    """
    key_w_folder = get_key_w_nested_folder(test_keys)
    prefix, path = key_w_folder.split('/', 1)
    prefix += '/'
    filetype = key_w_folder.rsplit('.', 1)[-1]

    expected_keys_not_recursive = [path.split('/', 1)[0] + '/']
    expected_keys_recursive = [path]

    matches = r'.*/.*\.' + filetype
    not_recursive_keys = list_objects(path=prefix,
                                      bucket=test_bucket,
                                      matches=matches)
    assert not_recursive_keys == expected_keys_not_recursive

    recursive_keys = list_objects(path=prefix,
                                  bucket=test_bucket,
                                  matches=matches,
                                  recursive=True)

    assert recursive_keys == expected_keys_recursive


def get_key_w_folder_wo_nested_folder(keys):
    """
    Given a list of S3 keys, returns the first full key containing a folder
    that does not contain a nested folder.

    Args:
        keys (list<str>): A list of candidate S3 keys
    Returns:
        str: The prefix of the first key found to contain nested folders
    """
    for key in keys:
        if key.count('/') == 1:
            return key


def get_key_w_nested_folder(keys):
    """
    Given a list of S3 keys, returns the first full key that contains
    a nested folder.

    Args:
        keys (list<str>): A list of candidate S3 keys
    Returns:
        str: The prefix of the first key found to contain nested folders
    """
    for key in keys:
        if key.count('/') > 1:
            return key
