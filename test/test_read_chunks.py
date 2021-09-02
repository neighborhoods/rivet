from rivet import read_df_in_chunks


uncompressed_formats = [
    'csv',
    'psv'
]

compressed_formats = [
    'csv.gz',
    'csv.zip',
    'csv.bz2',
    'csv.xz',
    'psv.gz',
    'psv.zip',
    'psv.bz2',
    'psv.xz'
]


def test_read_df_in_chunks_uncompressed(setup_bucket_w_dfs, test_bucket,
                                        test_df, test_df_keys):
    """
    Tests that reading DataFrames in chunks works for uncompressed textfiles
    """
    chunk_size = 2

    for format in uncompressed_formats:
        for key in test_df_keys[format]:
            current_row = 0
            for df_chunk in read_df_in_chunks(key, test_bucket):
                assert test_df.loc[current_row:
                                   current_row + chunk_size].equals(df_chunk)
                current_row += chunk_size


def test_read_df_in_chunks_compressed(setup_bucket_w_dfs, test_bucket,
                                      test_df, test_df_keys):
    """
    Tests that reading DataFrames in chunks works for compressed textfiles
    """
    chunk_size = 2

    for format in compressed_formats:
        for key in test_df_keys[format]:
            current_row = 0
            for df_chunk in read_df_in_chunks(key, test_bucket):
                assert test_df.loc[current_row:
                                   current_row + chunk_size].equals(df_chunk)
                current_row += chunk_size
