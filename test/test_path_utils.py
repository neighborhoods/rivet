import pytest

from rivet.s3_path_utils import get_filetype, clean_path


def test_refuses_no_filetype():
    """
    Tests that 'get_filetype' will raise an error if the key
    has no filetype extension
    """
    with pytest.raises(ValueError, match='must contain an extension'):
        get_filetype('invalid_key')


def test_clean_path():
    """
    Tests that 'clean_path' raises errors in accordance with good
    path name practices.
    """
    with pytest.raises(ValueError,
                       match='Double-forward slashes .* not permitted'):
        double_slash_path = 'folder0/folder1//df.csv'
        clean_path(double_slash_path)
    with pytest.raises(ValueError,
                       match='Double-dots .* not permitted'):
        double_dot_path = 'folder0/folder1/df..csv'
        clean_path(double_dot_path)
    with pytest.raises(ValueError,
                       match='Period characters .* not permitted'):
        dot_before_extnesion_path = 'folder0/folder.1/df.csv'
        clean_path(dot_before_extnesion_path)
