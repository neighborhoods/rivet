# river
A user-friendly Python-to-S3 interface. Adds quality of life and convenience features around `boto3`, including the handling of reading and writing to files in proper formats.  
It also enforces good practice in S3 naming conventions.


## Usage
`river` acts as an abstraction around the S3 functionality of Amazon's `boto3` package.
Although `boto3` is very powerful, the expansive functionality it boasts can be overwhelming
and often results in users sifting through a lot of documentation to find the subset of
functionality that they need. In order to make use of this package, you will need to have
the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` configured
for the buckets you wish to interact with.

### General
1. Because S3 allows for almost anything to be used as an S3 key, it can be very easy to
lose track of what exactly you have saved in the cloud. A very important example of this is
filetype - without a file extension at the end of the S3 key, it is entirely possible to
lose track of what format a file is saved as. `river` enforces file extensions in the objects
it reads and writes.
    * Currently supported formats are: CSV, Parquet, Pickle
    * Accessible in a Python session via `river.supported_formats`

2. A default S3 bucket can be set up as an environment variable, removing the requirement
to provide it to each function call. The name of this environment variable is `RV_DEFAULT_S3_BUCKET`.

### Reading
Reading in `river` only requires two things: a key, and a bucket.

```
import river as rv

df = rv.read('test_path/test_key.csv', 'test_bucket')
```

The file will be downloaded from S3 to a temporary file on your machine, and
based on the file extension at the end of the S3 key, the proper file reading
function will be used to read the object into the Python session.

Because it cannot be expected that all teams will always utilize good practice though,
the `read_badpractice` function allows for reading of files that do not have a file
extension (or do not follow enforced key-writing practices). In addition to a key
and bucket, this function requires that a storage format is provided.

```
import river as rv

obj = rv.read_badpractice('test_path/bad_key', 'test_bucket', filetype='pkl')
```

Both the `read` and `read_badpractice` functions accept additional arguments
for the underlying file reading functions. So, if a user is familiar with
those functions, they can customize how files are read.

```
import river as rv

df = rv.read('test_path/test_key.csv', 'test_bucket', delimiter='|')
```

### Writing
Writing is handled almost identically to reading, with the additional
parameter of the object to be uploaded. `write` returns the full path to
the object written to S3, including bucket name, without the `s3://` prefix.

```
import pandas as pd
import river as rv

df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
rv.write(df, 'test_path/test_key.csv', 'test_bucket')
```

Similar to the read functionality, `write` determines which underlying write
function to use based on the file extension in the S3 key provided. It can
accept additional arguments to be passed to those functions, exactly like
in the reading functions. However, unlike the reading functions, there is
no 'bad practice' writing funcitonality. The `river` developers understand that
its users can't control the practices of other teams, but as soon as writing
begins, the package will ensure that best practice is being followed.

### Other operations
1. Listing
`river` can list the files that are present at a given location in S3, with
two different options being available for how to do so: `include_prefix` and `recursive`.

We will be using the following example S3 bucket structure:
```
test_bucket
|---- test_key_0.csv
|---- folder0/
      |---- test_key_1.pq,
|---- folder1/
      |---- test_key_2.pkl,
      |---- subfolder0/
            |---- test_key_3.pkl,
|---- folder2/
      |---- test_key_4.csv
```

`rv.list` would behave as follows with default behavior:

```
import river as rv

rv.list(path='', bucket='test_bucket')
Output: ['test_key_0.csv', 'folder0/', 'folder1/', 'folder2/']

rv.list(path='folder1/', bucket='test_bucket')
Output: ['test_key_2.pkl', 'subfolder0/']
```

The `include_prefix` option will result in the full S3 key up to the current folder
to be included in the returned list of keys.
```
import river as rv

rv.list(path='folder1/', bucket='test_bucket', include_prefix=True)
Output: ['folder1/test_key_2.pkl', 'folder1/subfolder0/']
```

The `recursive` option will result in objects stored in nested folders to be returned as well.
```
import river as rv

rv.list(path='folder1', bucket='test_bucket', recursive=True)
Output: ['test_key_2.pkl', 'subfolder0/test_key_3.pkl']
```

`include_prefix` and `recursive` can be used simultaneously.

2. Existence checks
As an extension of listing operations, `river` can check if an object exists at
a specific S3 key. Note that for existence to be `True`, there must be an
_exact_ match with the key provided

Using the following bucket structure:
```
test_bucket
|---- test_key_0.csv
```
```
import river as rv

rv.exists('test_key_0.csv', bucket='test_bucket')
Output: True

rv.exists('test_key_1.csv', bucket='test_bucket')
Output: False

rv.exists('test_key_.csv', bucket='test_bucket')
Output: False
```

3. Copying
It is possible to copy a file from one location in S3 to another using `river`.
This function is not configurable - it only takes a source and destination key and bucket.
```
import river as rv

rv.copy(source_path='test_path/df.csv',
        dest_path='test_path_destination/df.csv',
        source_bucket='test_bucket',
        dest_bucket='test_bucket_destination')
```
