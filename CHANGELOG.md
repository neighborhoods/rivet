# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2020-05-15

### Added
- Ability to read files from S3
- Ability to write files to S3
- Ability to list files in S3, with specific prefixes and output settings
- Ability to copy objects between two S3 locations
- Storage formats: CSV, Pickle, Parquet

### Changed
- Default CSV writing behavior as was present prior to this code being made into its own package.