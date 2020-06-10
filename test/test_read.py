from river import read


def test_read_csv(setup_bucket_w_dfs, test_bucket, test_df, test_df_keys):
    """Tests that reading files stored as CSV works properly"""
    for key in test_df_keys['csv']:
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
