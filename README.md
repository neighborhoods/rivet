# rivet
A user-friendly Python-to-S3 interface. Adds quality of life and convenience features around `boto3`, including the handling of reading and writing to files in proper formats.  While there is nothing that you can do with `rivet` that you can't do with `boto3`, `rivet`'s primary focus is ease-of-use. By handling lower-level operations such as client establishment and default argument specification behind the scenes, the cost of entry to interacting with cloud storage from within Python is lowered.
It also enforces good practice in S3 naming conventions.


## Usage
`rivet` acts as an abstraction around the S3 functionality of Amazon's `boto3` package.
Although `boto3` is very powerful, the expansive functionality it boasts can be overwhelming
and often results in users sifting through a lot of documentation to find the subset of
functionality that they need. In order to make use of this package, you will need to have
the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` configured
for the buckets you wish to interact with.

### General
1. Because S3 allows for almost anything to be used as an S3 key, it can be very easy to
lose track of what exactly you have saved in the cloud. A very important example of this is
filetype - without a file extension at the end of the S3 key, it is entirely possible to
lose track of what format a file is saved as. `rivet` enforces file extensions in the objects
it reads and writes.
    * Currently supported formats are: CSV, JSON, Avro, Feather, Parquet, Pickle
    * Accessible in a Python session via `rivet.supported_formats`

2. A default S3 bucket can be set up as an environment variable, removing the requirement
to provide it to each function call. The name of this environment variable is `RV_DEFAULT_S3_BUCKET`.

### Reading
Reading in `rivet` only requires two things: a key, and a bucket.

```
import rivet as rv

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
import rivet as rv

obj = rv.read_badpractice('test_path/bad_key', 'test_bucket', filetype='pkl')
```

Both the `read` and `read_badpractice` functions accept additional arguments
for the underlying file reading functions. So, if a user is familiar with
those functions, they can customize how files are read.

```
import rivet as rv

df = rv.read('test_path/test_key.csv', 'test_bucket', delimiter='|')
```

### Writing
Writing is handled almost identically to reading, with the additional
parameter of the object to be uploaded. `write` returns the full path to
the object written to S3, including bucket name, without the `s3://` prefix.

```
import pandas as pd
import rivet as rv

df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
rv.write(df, 'test_path/test_key.csv', 'test_bucket')
```

Similar to the read functionality, `write` determines which underlying write
function to use based on the file extension in the S3 key provided. It can
accept additional arguments to be passed to those functions, exactly like
in the reading functions. However, unlike the reading functions, there is
no 'bad practice' writing funcitonality. The `rivet` developers understand that
its users can't control the practices of other teams, but as soon as writing
begins, the package will ensure that best practice is being followed.

### Other operations
1. Listing<br>
`rivet` can list the files that are present at a given location in S3, with
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

  - `rv.list` would behave as follows with default behavior:
     ```
     import rivet as rv

     rv.list(path='', bucket='test_bucket')
     Output: ['test_key_0.csv', 'folder0/', 'folder1/', 'folder2/']

     rv.list(path='folder1/', bucket='test_bucket')
     Output: ['test_key_2.pkl', 'subfolder0/']
     ```

  - `include_prefix` option will result in the full S3 key up to the current folder
 to be included in the returned list of keys.
     ```
     import rivet as rv

     rv.list_objects(path='folder1/', bucket='test_bucket', include_prefix=True)
     Output: ['folder1/test_key_2.pkl', 'folder1/subfolder0/']
     ```

  - The `recursive` option will result in objects stored in nested folders to be returned as well.
    ```
    import rivet as rv

    rv.list(path='folder1', bucket='test_bucket', recursive=True)
    Output: ['test_key_2.pkl', 'subfolder0/test_key_3.pkl']
    ```

  - `include_prefix` and `recursive` can be used simultaneously.

  - Regular expression matching on keys can be performed with the `matches` parameter.
      - You can account for your key prefix:
          1. In the `path` argument (highly encouraged for the above reasons): `rv.list_objects(path='folder0/')`
          2. Hard-coded as part of the regular expression in your `matches` argument: `rv.list_objects(matches='folder0/.*')`
          3. or by accounting for it in the matching logic of your regular expression: `rv.list_objects(matches='f.*der0/.*')`

      - When you are using both `path` and `matches` parameters, however, there is one situation you need to be cautious of:
          1. Hard-coding the path in `path` and using `matches` to match on anything that comes _after_ the path works great: `rv.list_objects(path='folder0/', matches='other_.*.csv')`
          2. Hard-coding the path in `path` and including the hard-coded path in `matches` works fine, but is discouraged for a number of reasons: `rv.list_objects(path='folder0/', matches='folder0/other_.*.csv')`
          3. What **will not** work is hard-coding the path in `path` and dynamically matching it in `matches`: `rv.list_objects(path='folder0/', matches='f.*der0/other_.*.csv')`
              - This is because including the path in the regular expression interferes with the logic of the function. When you provide the hard-coded path both in `path` and in the beginning of `matches`, it can be detected and removed from the regular expression, but there is no definitive way to do this when you are matching on it.

      - So, in general, try to separate the keep `path` and `matches` entirely separate if at all possible.

2. Existence checks<br>
As an extension of listing operations, `rivet` can check if an object exists at
a specific S3 key. Note that for existence to be `True`, there must be an
_exact_ match with the key provided

Using the following bucket structure:
```
test_bucket
|---- test_key_0.csv
```
```
import rivet as rv

rv.exists('test_key_0.csv', bucket='test_bucket')
Output: True

rv.exists('test_key_1.csv', bucket='test_bucket')
Output: False

rv.exists('test_key_.csv', bucket='test_bucket')
Output: False
```

3. Copying<br>
It is possible to copy a file from one location in S3 to another using `rivet`.
This function is not configurable - it only takes a source and destination key and bucket.
```
import rivet as rv

rv.copy(source_path='test_path/df.csv',
        dest_path='test_path_destination/df.csv',
        source_bucket='test_bucket',
        dest_bucket='test_bucket_destination')
```

### Session-Level Configuration
`rivet` outputs certain messages to the screen to help interactive users
maintain awareness of what is being performed behind-the-scenes. If this
is not desirable (as may be the case for notebooks, pipelines, usage of
`rivet` within other packages, etc.), all non-logging output can be
disabled with `rv.set_option('verbose', False)`.
