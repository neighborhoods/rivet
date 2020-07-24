# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- General usage documentation
- Progress bar functionality for reading, writing, and copying operations
- Support for Avro filetype
- Regular expression matching functionality for `list_objects`
- Bugfix: Kwargs can now be passed when writing in Parquet format
- Bugfix: Relaxed requirements on what was considered a valid S3 key for the
`recursive` option of `list_objects` - S3 will handle that for the function,
no reason we need to account for it
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
