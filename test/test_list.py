from river import list_objects, exists


def test_list_objects_w_objects(setup_bucket_w_contents,
                                test_bucket, test_keys):
    keys_wo_prefix = sorted(list(
        {key if '/' not in key else key[:key.find('/') + 1]
         for key in test_keys}))
    objects = list_objects(bucket=test_bucket)
    assert objects == keys_wo_prefix


def test_list_objects_wo_objects(setup_bucket_wo_contents,
                                 test_bucket):
    objects = list_objects(bucket=test_bucket)
    assert objects == []


def test_list_objects_include_prefix(setup_bucket_w_contents,
                                     test_bucket, test_keys):
    prefix = None
    idx = 0
    while prefix is None:
        current_key = test_keys[idx]
        if current_key.count('/') > 1:
            prefix = current_key.rsplit('/', 2)[0] + '/'
        idx += 1

    keys_w_prefix = []
    for key in test_keys:
        if key.startswith(prefix):
            if key[len(prefix):].count('/') == 0:
                keys_w_prefix.append(key)
            else:
                keys_w_prefix.append(key[:key.find('/', len(prefix)) + 1])

    objects = list_objects(path=prefix, bucket=test_bucket,
                           include_prefix=True)

    assert objects == keys_w_prefix


def test_list_objects_recursive(setup_bucket_w_contents,
                                test_bucket, test_keys):
    pass


def test_list_objects_include_prefix_and_recursive(setup_bucket_w_contents,
                                                   test_bucket, test_keys):
    pass


def test_exists_w_object_present(setup_bucket_w_contents,
                                 test_bucket, test_keys):
    assert exists(test_keys[0], test_bucket)


def test_exists_wo_object_present(setup_bucket_wo_contents,
                                  test_bucket, test_keys):
    assert not exists(test_keys[0], test_bucket)


def test_exists_wo_only_exact_match(setup_bucket_w_contents,
                                    test_bucket, test_keys):
    key = test_keys[0]
    partial_key = key[:len(key) - 1]
    assert not exists(partial_key[0], test_bucket)
