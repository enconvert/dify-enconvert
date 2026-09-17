# Changelog

All notable changes to this plugin are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-09-17

### Changed

- Perceive URL's summary line states when a read was a detected content-free block (`is_blocked`,
  a normal 200 with empty outputs) and when it was not billed (`billed` false: blocked, `http_error`
  or `login_wall`). The raw JSON message already carried both fields.

## [0.0.1] - 2026-08-27

### Added

- Initial release.
- Six tools: Perceive URL, Web Search, Discover URLs, Extract Structured, Convert File to Markdown,
  Convert File to PDF.
- The convert tools take a Dify file input; the plugin makes no requests to user-supplied URLs.
- Perceive inlines markdown and HTML output (up to 256 KB) instead of returning only a signed URL.
- API-key credential (`X-API-Key`) validated on connect against `GET /v1/whoami`.
