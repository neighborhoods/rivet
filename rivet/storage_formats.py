import logging
import pickle

import pandas as pd
import pandavro as pdx


def get_storage_fn(filetype, rw):
    """
    Gets the appropriate storage function based on filetype and read/write

    Args:
        filetype (str): The storage type of the file being written/read
        rw (str): Whether the file is being read or written
    Returns:
        function: The storage function needed for reading/writing the filetype
    """
    if filetype not in format_fn_map.keys():
        raise ValueError(
            'Storage type \'{filetype}\' not supported.'.format(
                filetype=filetype)
        )
    return format_fn_map[filetype][rw]

###############################################################################

#######
# CSV #
#######


def _read_csv(tmpfile, *args, **kwargs):
    """
    Reads a DataFrame from a CSV

    Args:
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be read from
    Returns:
        pd.DataFrame: The DataFrame read from CSV
    """
    obj = pd.read_csv(tmpfile.name, *args, **kwargs)
    return obj


def _write_csv(obj, tmpfile, index=False, *args, **kwargs):
    """
    Saves a DataFrame to a CSV with modifiable default values

    Args:
        obj (pd.DataFrame): The DataFrame to be written to CSV
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
        index (bool, default=False): Whether to include the DataFrame index
            in the CSV, used to establish default behavior.
            Can be overridden in args/kwargs.

    Raises:
        TypeError: if 'obj' is not a DataFrame
    """
    if not isinstance(obj, pd.DataFrame):
        raise TypeError('Storage format of \'csv\' can only be used with '
                        'DataFrames.')

    obj.to_csv(tmpfile.name, index=index, *args, **kwargs)


csv = {
    'read': _read_csv,
    'write': _write_csv
}

##############################################################################

#######
# PSV #
#######


def _read_psv(tmpfile, *args, **kwargs):
    """
    Reads a DataFrame from a PSV.
    Wrapper around _write_csv with different 'sep' character.

    Args:
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be read from
    Returns:
        pd.DataFrame: The DataFrame read from PSV
    """
    return _read_csv(tmpfile, sep='|', *args, **kwargs)


def _write_psv(obj, tmpfile, *args, **kwargs):
    """
    Saves a DataFrame to a PSV with modifiable default values.
    Wrapper around _write_csv with different 'sep' character.

    Args:
        obj (pd.DataFrame): The DataFrame to be written to PSV
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
        index (bool, default=False): Whether to include the DataFrame index
            in the PSV, used to establish default behavior.
            Can be overridden in args/kwargs.

    Raises:
        TypeError: if 'obj' is not a DataFrame
    """
    _write_csv(obj, tmpfile, sep='|', *args, **kwargs)


psv = {
    'read': _read_psv,
    'write': _write_psv
}

##############################################################################

##########
# Pickle #
##########


def _read_pickle(tmpfile, *args, **kwargs):
    """
    Reads a pickled object

    Args:
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be read from
    Returns:
        object: The unpickled object
    """
    # Pickle reading from a tempfile if it hasn't been closed post-writing
    # raises an 'EOFError', so we have to create a secondary opening.
    # Will work on unix-like systems, but not Windows.
    with open(tmpfile.name, 'rb') as f:
        obj = pickle.load(f, *args, **kwargs)
    return obj


def _write_pickle(obj, tmpfile, protocol=pickle.HIGHEST_PROTOCOL,
                  *args, **kwargs):
    """
    Pickles an object with modifiable default values

    Args:
        obj (pd.DataFrame): The object to be pickled
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
        protocol (bool, default=pickle.HIGHEST_PROTOCOL):
            Pickling protocol to use. Can be overridden in args/kwargs.

    """
    pickle.dump(obj, tmpfile, protocol=protocol, *args, **kwargs)
    # Otherwise, file won't be populated until after 'tmpfile' closes
    tmpfile.flush()


pkl = {
    'read': _read_pickle,
    'write': _write_pickle
}

##############################################################################

###########
# Parquet #
###########


def _read_parquet(tmpfile, *args, **kwargs):
    """
    Reads a DataFrame from a Parquet file

    Args:
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be read from
    Returns:
        pd.DataFrame: The DataFrame read from disk
    """
    obj = pd.read_parquet(tmpfile.name, *args, **kwargs)
    return obj


def _write_parquet(obj, tmpfile, index=False, *args, **kwargs):
    """
    Saves a DataFrame to Parquet format

    Args:
        obj (pd.DataFrame): The DataFrame to be written to Parquet
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
        index (bool, default=False): Whether to include the DataFrame index
            in the Parquet file, used to establish default behavior.
            Can be overridden in args/kwargs.

    Raises:
        TypeError: if 'obj' is not a DataFrame
    """
    if not isinstance(obj, pd.DataFrame):
        raise TypeError('Storage format of \'pq\'/\'parquet\' can only '
                        'be used with DataFrames.')

    obj.to_parquet(tmpfile.name, index=index, *args, **kwargs)


pq = {
    'read': _read_parquet,
    'write': _write_parquet
}

##############################################################################

########
# AVRO #
########


def _read_avro(tmpfile, remove_timezone_from_type=True, *args, **kwargs):
    """
    Reads a DataFrame from an Avro file

    Args:
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be read from
    Returns:
        pd.DataFrame: The DataFrame read from Avro
    """

    # Pandavro reading from a tempfile if it hasn't been closed post-writing
    # raises an 'ValueError', so we have to create a secondary opening.
    # Will work on unix-like systems, but not Windows.
    with open(tmpfile.name, 'rb') as f:
        df = pdx.read_avro(f, *args, **kwargs)

    if remove_timezone_from_type:
        datetime_cols = df.columns[df.dtypes == 'datetime64[ns, UTC]']
        df[datetime_cols] = df[datetime_cols].apply(
            lambda x: x.dt.tz_convert(None))
    return df


def _write_avro(df, tmpfile, times_as_micros=False, *args, **kwargs):
    """
    Saves a DataFrame to Avro format

    Args:
        obj (pd.DataFrame): The DataFrame to be written to Avro
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
        save_datetimes_as_millis (bool):
            Whether to save timestamps as milliseconds or
            leave it as the pandavro default microseconds
    """
    pdx.to_avro(tmpfile, df, times_as_micros=times_as_micros, *args, **kwargs)


avro = {
    'read': _read_avro,
    'write': _write_avro
}

##############################################################################

########
# JSON #
########


def _read_json(tmpfile, *args, **kwargs):
    """
    Reads a DataFrame from a JSON file

    Args:
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be read from
    Returns:
        pd.DataFrame: The DataFrame read from JSON
    """
    df = pd.read_json(tmpfile.name)
    return df


def _write_json(df, tmpfile, hive_format=False, *args, **kwargs):
    """
    Saves a DataFrame to JSON format

    Args:
        obj (pd.DataFrame): The DataFrame to be written to Avro
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
        hive_format (bool):
            Whether to format the JSON to be read as part of a Hive table.
            Note: Data formatted this way will not be natively readable
            back into a Python session.
    """
    if hive_format:
        # Nested open, original tmpfile behaves slightly differently
        with open(tmpfile.name, 'w') as f:
            for row in df.iterrows():
                row[1].to_json(f)
                f.write('\n')
    else:
        df.to_json(tmpfile.name)


json = {
    'read': _read_json,
    'write': _write_json
}

##############################################################################

###########
# Feather #
###########


def _read_feather(tmpfile, *args, **kwargs):
    """
    Reads a DataFrame from a feather file

    Args:
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be read from
    Returns:
        pd.DataFrame: The DataFrame read from feather
    """
    df = pd.read_feather(tmpfile.name)
    return df


def _write_feather(df, tmpfile, *args, **kwargs):
    """
    Saves a DataFrame to feather format

    Args:
        obj (pd.DataFrame): The DataFrame to be written to Avro
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
    """
    if any(df.dtypes == 'object'):
        logging.info(
            'WARNING: Columns of dtype "object" detected in dataframe '
            'being written to feather format. Feather does not support '
            'python objects/classes or collection types, such as lists '
            'and dictionaries, and will produce unexpected results. '
            'If this column merely contains strings, then this message '
            'can be ignored.')
    df.to_feather(tmpfile.name)


feather = {
    'read': _read_feather,
    'write': _write_feather
}

##############################################################################

format_fn_map = {
   'avro': avro,
   'csv': csv,
   'csv.gz': csv,
   'csv.zip': csv,
   'csv.bz2': csv,
   'csv.xz': csv,
   'psv': psv,
   'psv.gz': psv,
   'psv.zip': psv,
   'psv.bz2': psv,
   'psv.xz': psv,
   'feather': feather,
   'json': json,
   'pickle': pkl,
   'pkl': pkl,
   'pq': pq,
   'parquet': pq
}
