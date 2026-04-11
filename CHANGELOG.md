# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial test suite for core logic and CLI
- GitHub Actions CI workflow
- CONTRIBUTING.md guide

### Changed
- Enhanced README with more usage examples

## [0.0.2] - 2024-04-10

### Added
- Support for HTTP protocol (in addition to HTTPS)
- Interactive selection when converting SSH to HTTPS/HTTP
- Dry-run mode (`--dry-run` / `-n`)
- Version flag (`--version` / `-v`)
- Internationalization support (i18n)
- Rich console output with tables and panels

### Changed
- Improved URL conversion logic
- Better error handling and user feedback

## [0.0.1] - 2024-04-09

### Added
- Initial release
- Basic HTTPS ↔ SSH conversion
- CLI with Typer
- Support for multiple remotes
