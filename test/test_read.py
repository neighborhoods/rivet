from rivet import read


def test_read_csv(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading files stored as a CSV works properly"""
    for key in test_df_keys['csv']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_csv_gz(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as a gzip-compressed CSV works properly
    """
    for key in test_df_keys['csv.gz']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_csv_zip(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as a zip-compressed CSV works properly
    """
    for key in test_df_keys['csv.zip']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_csv_bz2(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as a bzip2-compressed CSV works properly
    """
    for key in test_df_keys['csv.bz2']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_csv_xz(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as an xz-compressed CSV works properly
    """
    for key in test_df_keys['csv.xz']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_psv(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading files stored as a PSV works properly"""
    for key in test_df_keys['psv']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_psv_gz(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as a gzip-compressed PSV works properly
    """
    for key in test_df_keys['psv.gz']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_psv_zip(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as zip-compressed PSV works properly
    """
    for key in test_df_keys['psv.zip']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_psv_bz2(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as a bzip2-compressed PSV works properly
    """
    for key in test_df_keys['psv.bz2']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_psv_xz(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """
    Tests that reading files stored as an xz-compressed PSV works properly
    """
    for key in test_df_keys['psv.xz']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_feather(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading files stored as feather works properly"""
    for key in test_df_keys['feather']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_json(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading files stored as JSON works properly"""
    for key in test_df_keys['json']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_pkl(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading pickled files works properly"""
    for key in test_df_keys['pkl']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_pq(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading files stored as Parquet works properly"""
    for key in test_df_keys['pq']:
        df = read(key, test_bucket)
        assert df.equals(test_df)


def test_read_avro(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading files stored as Avro works properly"""
    for key in test_df_keys['avro']:
        df = read(key, test_bucket)
        assert df.equals(test_df)
