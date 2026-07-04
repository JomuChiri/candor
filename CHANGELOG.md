# Changelog

## [0.4] - 2026-07-04
### Added
- **Help system**: `help <module>` shows aliases, actions, and usage.
- **Metadata system**: `metadata <module>` outputs structured JSON for modules.
- **Doctor checks**: `doctor <tool>` validates installation, path, and version.
- **Reporting**: `report latest` saves Markdown/HTML reports of job execution.
- **Config loader**: YAML configuration support with defaults for tools.
- **Progress indicators**: staged execution feedback (Planning, Executing, Collecting output).
- **Job history**: record, list, and reload jobs with intent, plan, and result tracking.

### Changed
- CLI banner updated to `Candor SOC Assistant v0.4`.
- Refined `ExecutionResult` status handling (success, warning, failed).
- Improved error handling for invalid targets and unknown modules.

### Fixed
- Corrected imports for `load_job`, `save_report`, and `doctor`.
- Added `Job` dataclass to history for structured persistence.
- Removed redundant `parse_intent` calls and misplaced execution blocks.
