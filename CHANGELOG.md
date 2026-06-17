# Changelog

## [0.2.0] - 2026-06-16

### Python 3 Migration
- Migrated codebase from Python 2.7 to Python 3.10+
- Removed all `six` imports and Python 2/3 compatibility branching
- Replaced all `super(ClassName, self)` / `super(ClassName, cls)` with bare `super()`
- Added `encoding='utf-8'` to all text-mode `open()` calls
- Converted `%` string formatting to f-strings

### Packaging
- Replaced `setup.py` / `setup.cfg` with `pyproject.toml` (PEP 621)
- Adopted `uv` as the package manager (replaces pip + virtualenv)
- Converted `requirements.txt` to reference-only, pointing to `pyproject.toml`
- Updated `initialize.py` to use `uv venv` + `uv sync`
- Added `uv.lock` to `.gitignore`
- Removed stale `MANIFEST.in`

### Dependency Upgrades
- Flask: 1.0.2 → 3.1.3
- Werkzeug: 1.0.1 → 3.1.8
- Authlib: 0.14.3 → 1.7.2 (sqla_oauth1 replaced with manual hooks)
- RDFLib: 5.0.0 → 7.x
- Flask-RESTx: 0.5.1 → 1.3.x
- All other dependencies updated to modern versions
- Removed: `RDFLib-JSONLD` (merged into RDFLib), `six`

### Flask Configuration
- Removed deprecated `FLASK_ENV` from config and `.flaskenv`
- Set `SQLALCHEMY_TRACK_MODIFICATIONS = False`
- Fixed tuple-bug on `MAIL_SERVER` / `LOG_TO_STDOUT`
- Replaced `FLASK_DEBUG` with `DEBUG`

### OAuth (pyoslc_oauth)
- Replaced `authlib.integrations.sqla_oauth1` mixins with direct model implementations
- Replaced removed helper functions (`create_query_client_func`, `register_nonce_hooks`, etc.)
  with manual `register_hook()` calls on `AuthorizationServer`

### Linting
- Added `setup.cfg` with `max-line-length = 120` for flake8
- Fixed all pre-existing E127 (continuation indent) and E501 (line length) issues
- flake8 now passes clean across the entire codebase

### Other
- Updated `tox.ini` envlist to `py310, py311, py312, py313`
- Removed `u''` unicode prefixes from `docs/source/conf.py`
- Updated project classifiers to Python 3 only
