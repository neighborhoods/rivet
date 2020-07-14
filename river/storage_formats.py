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


# TODO - any way to resolve lost dtypes, like when reading datetimes?
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

def _read_avro(tmpfile, *args, **kwargs):
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

    datetime_cols = df.columns[df.dtypes == 'datetime64[ns, UTC]']
    df[datetime_cols] = df[datetime_cols].apply(
        lambda x: x.dt.tz_convert(None))
    return df


def _write_avro(df, tmpfile, *args, **kwargs):
    """
    Saves a DataFrame to Avro format

    Args:
        obj (pd.DataFrame): The DataFrame to be written to Avro
        tmpfile (tempfile.NamedTemporaryFile):
            Connection to the file to be written to
    """
    pdx.to_avro(tmpfile, df, *args, **kwargs)


avro = {
    'read': _read_avro,
    'write': _write_avro
}

##############################################################################

# TODO
#######
# ORC #
#######

##############################################################################

format_fn_map = {
   'avro': avro,
   'csv': csv,
   'pickle': pkl,
   'pkl': pkl,
   'pq': pq,
   'parquet': pq
}
