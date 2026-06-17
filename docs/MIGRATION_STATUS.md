# PyOSLC Python 3 Migration — Status

## Environment

| Item | Value |
|------|-------|
| Python runtime | 3.13.5 |
| Package manager | uv (at `/home/jfox/.local/bin/uv`) |
| Virtual env | `.venv` (created by `uv venv`) |
| Install method | `uv sync` (reads `pyproject.toml`) |
| Test framework | pytest 9.1 |

## Installed Dependency Versions

| Package | Version | Constraint |
|---------|---------|------------|
| Flask | 3.1.3 | `>=3.0,<4.0` |
| Werkzeug | 3.1.8 | `>=3.0,<4.0` |
| Authlib | 1.7.2 | `>=1.0,<2.0` |
| RDFLib | (resolved) | `>=7.0.0` |
| Flask-RESTx | (resolved) | `>=1.3.0` |
| Flask-Bootstrap | (resolved) | `>=3.3.7.1` |
| Flask-SQLAlchemy | (resolved) | `>=3.1.0` |
| Flask-Login | (resolved) | `>=0.6.0` |
| Flask-WTF | (resolved) | `>=1.2.0` |
| Flask-CORS | (resolved) | `>=4.0.0` |
| python-dotenv | (resolved) | `>=1.0.0` |
| cachelib | (resolved) | `>=0.13.0` |
| requests | (resolved) | `>=2.31.0` |

## Completed Work

### Packaging
- `pyproject.toml` created (PEP 621) with all metadata, dependencies, and tool configs
- `setup.py` kept as backward-compat stub for `pip install -e .`
- `setup.cfg` removed (config migrated to `pyproject.toml` + new minimal `setup.cfg` for flake8)
- `MANIFEST.in` still present (not yet removed — verify it's unused)
- `requirements.txt` converted to comment-only, points users to `uv sync`
- `initialize.py` updated to use `uv venv` + `uv sync`
- `tox.ini` updated: envlist = `py310, py311, py312`, minversion = `4.0`
- `uv.lock` added to `.gitignore`

### Python 2 Compatibility — All Removed
- `six` removed entirely — no leftover imports anywhere in the codebase
- `from six.moves.urllib.parse import urlparse` → `from urllib.parse import urlparse` (3 files)
- `if six.PY2` / `if six.PY3` branching removed (3 locations)
- All `super(ClassName, self)` / `super(ClassName, cls)` → `super()` (~75 instances, 11 files)
- `encoding='utf-8'` added to all text-mode `open()` calls (~20 instances, 6 files)
- `%` formatting converted to f-strings (2 instances)

### Flask Configuration
- `app/config.py`: `FLASK_ENV` removed, `SQLALCHEMY_TRACK_MODIFICATIONS = False`, tuple-bug fixed (`MAIL_SERVER` / `LOG_TO_STDOUT`)
- `.flaskenv`: `FLASK_ENV` removed

### Flask 3.x + Authlib 1.x Upgrade
- Flask upgraded from 2.3.3 → **3.1.3**, Werkzeug from 2.3.8 → **3.1.8**, Authlib from 0.15.6 → **1.7.2**
- Replaced `authlib.integrations.sqla_oauth1` (removed in Authlib 1.x) with direct model implementations (`pyoslc_oauth/models.py`)
- Replaced `create_query_client_func`, `register_nonce_hooks`, `register_temporary_credential_hooks`, `register_token_credential_hooks` with manual `register_hook()` calls (`pyoslc_oauth/server.py`)
- All required methods (`get_client_secret`, `get_default_redirect_uri`, `get_oauth_token`, `get_oauth_token_secret`, etc.) implemented directly on `Client` and `TokenCredential` models
- `_app_ctx_stack` deprecation resolved — no longer triggered by Authlib 1.x

### Linting
- `setup.cfg` created with `max-line-length = 120` for flake8
- `pyproject.toml` includes `[tool.flake8]` config (note: flake8 reads from `setup.cfg`, not `pyproject.toml`)

## Key Decisions

| Decision | Reason |
|----------|--------|
| Flask-Bootstrap kept | Templates depend on it; migrating to Bootstrap-Flask would require template rewrites |
| PEP 621 format used | uv-native; no Poetry dependency |
| flake8 in `setup.cfg` not `pyproject.toml` | flake8 does not read `[tool.flake8]` from `pyproject.toml` — only reads from `setup.cfg`, `.flake8`, or `tox.ini` |
| Direct `register_hook` for OAuth 1.0 | Authlib 1.x removed `sqla_oauth1` helpers; implemented hooks manually |

## Verification

| Check | Result |
|-------|--------|
| `uv sync --extra test` | 80 packages resolved, 1 installed (pyoslc itself) |
| `pytest -v` | **34 passed** in 1.71s |
| `flake8 pyoslc app pyoslc_oauth` | **Clean** — 0 issues |

## Remaining / Future Work

| Task | Priority | Notes |
|------|----------|-------|
| ~~Upgrade to Flask 3.0+ / Authlib 1.x+~~ | Done | Flask 3.1.3, Werkzeug 3.1.8, Authlib 1.7.2 — all constraints lifted |
| Migrate from Flask-Bootstrap to Bootstrap-Flask | Low | Templates use `{% extends "bootstrap/base.html" %}` — Bootstrap-Flask uses a different approach |
| ~~Fix pre-existing E127/E501 lint issues~~ | Done | All continuation line indent and line length issues fixed |
| ~~Remove `u''` prefixes from `docs/source/conf.py`~~ | Done | Python 3 strings are Unicode by default |
| ~~Remove `MANIFEST.in`~~ | Done | Stale paths; `pyproject.toml` package-data covers it |
| Add Python 3.13 to `tox.ini` envlist | Low | Currently `py310, py311, py312` |
