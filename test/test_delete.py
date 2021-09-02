import pytest

from rivet import delete, list_objects


def test_delete(setup_bucket_w_contents, test_bucket, test_keys):
    key = list_objects('', test_bucket, include_prefix=True, recursive=True)[0]
    delete(key, test_bucket)
    assert key not in list_objects('', test_bucket,
                                   include_prefix=True, recursive=True)


def test_delete_recursive(setup_bucket_w_contents, test_bucket):
    keys = list_objects('', test_bucket, include_prefix=True, recursive=True)

    # Get prefix that matches multiple keys
    multi_match_prefix = None
    i = 0
    while not multi_match_prefix:
        key = keys[i]
        if '/' in key:
            prefix = key.split('/')[0]
            if len([cand_key for cand_key in keys
                    if cand_key.startswith(prefix)]) > 1:
                multi_match_prefix = prefix + '/'
        i += 1

    delete(multi_match_prefix, test_bucket, recursive=True)

    remaining_keys = list_objects('', test_bucket,
                                  include_prefix=True, recursive=True)

    assert ~any([key.startswith(prefix) for key in remaining_keys])


def test_bucket_nuke_protection():
    with pytest.raises(ValueError, match='seems unsafe'):
        delete('', '')
