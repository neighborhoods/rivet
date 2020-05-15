import pickle
import os
import pandas as pd


def get_storage_fn(filetype, rw):
    if filetype not in format_fn_map.keys():
        raise ValueError('Storage type \'{storage_type}\' not supported.')
    return format_fn_map[filetype][rw]

###############################################################################

#######
# CSV #
#######


def _read_csv(tmpfile, *args, **kwargs):
    obj = pd.read_csv(tmpfile.name)
    return obj


def _write_csv(obj, tmpfile, index=False, *args, **kwargs):
    """
    Saves a DataFrame to a CSV and uploads it to S3

    Args:
        obj (pd.DataFrame): The DataFrame to be uploaded
        path (str): The full path (other than bucket) to the object in S3
        bucket (str): The S3 bucket to save 'obj' in

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
    print(os.system('ls -l ' + tmpfile.name))
    obj = pickle.load(tmpfile)
    return obj


def _write_pickle(obj, tmpfile, protocol=pickle.HIGHEST_PROTOCOL,
                  *args, **kwargs):
    """
    Pickles an object and uploads it to S3

    Args:
        obj (object): The object to be pickled and uploaded
        path (str): The full path (other than bucket) to the object in S3
        bucket (str): The S3 bucket to save 'obj' in
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
    obj = pd.read_parquet(tmpfile.name, *args, **kwargs)
    return obj


def _write_parquet(obj, tmpfile, index=False, *args, **kwargs):
    """
    Saves a DataFrame to Parquet format and uploads it to S3

    Args:
        obj (pd.DataFrame): The DataFrame to be uploaded
        path (str): The full path (other than bucket) to the object in S3
        bucket (str): The S3 bucket to save 'obj' in

    Raises:
        TypeError: if 'obj' is not a DataFrame
    """
    if not isinstance(obj, pd.DataFrame):
        raise TypeError('Storage format of \'pq\'/\'parquet\' can only '
                        'be used with DataFrames.')

    obj.to_parquet(tmpfile.name, index=index)


pq = {
    'read': _read_parquet,
    'write': _write_parquet
}

##############################################################################

# TODO
########
# AVRO #
########

##############################################################################

format_fn_map = {
   'csv': csv,
   'pickle': pkl,
   'pkl': pkl,
   'pq': pq,
   'parquet': pq
}
