# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.0] 2021-04-19

### Added
- Added support for reading textfiles (optionally compressed) in chunks - may add
support for doing the same with Avro files in the future

### Changed
- Updated old docstrings
- Fixed bug where attempting to read/write to/from an extensionless S3 path
would throw an irrelevant exception (claiming that period characters are
not allowed in S3 paths outside of file extensions)

## [1.4.0] 2021-04-05

### Added
- Added support for PSV files (pipe-separated value)
- Added support for CSV and PSV files that are compressed with `zip` or `gzip`

### Changed
- Fixed Pyarrow dependency

## [1.3.2] 2021-02-10

### Added
- Session-level configuration Functionality
- Verbosity option: disable all non-logging output, for use in notebooks or pipelines.

## [1.3.1] 2020-12-15

### Changed
- Prepped to go open source!
- `pandavro` additions were merged to master and released, so now using the publicly available version
- Fields in `_version.py` are now available and viewable in-code

## [1.3.0] 2020-11-16

### Added
- Functions for just uploading/downloading a file to disk directly to/from S3

## [1.2.1] 2020-10-29

### Changed
- Relaxed `pandas` requirement

## [1.2.0] 2020-10-23

### Added
- Added 'delete' functionality

## [1.1.1] 2020-09-10

### Changed
- Hotfix for JSON writing in Hive format.

## [1.1.0] 2020-09-10

### Added
- Support for `JSON` and `feather` file formats

## [1.0.0] 2020-07-24

### Added
- General usage documentation
- Progress bar functionality for reading, writing, and copying operations
- Support for Avro filetype
- Regular expression matching functionality for `list_objects`
- `list_objects` can now return greater than 1000 objects - previously,
the list was truncated at 1000
- Bugfix: Kwargs can now be passed when writing in Parquet format. All other
formats accepted kwargs, but it was left out from Parquet as an oversight.
- Bugfix: Relaxed requirements on what was considered a valid S3 key for the
`recursive` option of `list_objects`. Prior to this, `list_objects` was filtering
out keys that it was not supposed to under certain circumstances.
S3 will not allow invalid keys in the first place, no reason we need to account for it
- Bugfix: Default values for `bucket` (as provided by environment variables)
is now evaluated at function call-time rather than upon import

### Changed
- Switched to standard NHDS CI pipeline

## [0.2.0] - 2020-06-15

### Added
- 'exists' function - check if an object exists at a specific S3 key
- Unit tests!

## [0.1.1] - 2020-05-19

### Added
- Specific error for S3 paths that do not include file extensions

### Changed
- Hotfix: `*kwargs` changed to `**kwargs` in `s3_write`
- Hotfix: Error string formatting in `get_storage_fn`

## [0.1.0] - 2020-05-15

### Added
- Ability to read files from S3
- Ability to write files to S3
- Ability to list files in S3, with specific prefixes and output settings
- Ability to copy objects between two S3 locations
- Storage formats: CSV, Pickle, Parquet

### Changed
- Default CSV writing behavior as was present prior to this code being made into its own package.
