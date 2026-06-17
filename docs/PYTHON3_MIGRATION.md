# PyOSLC Python 3 & Modern Library Migration

## Goal

Remove all Python 2 compatibility code, modernize the packaging, and update all dependencies to their latest stable versions.

## Python Version

**Target: Python >= 3.10** (Python 2.7 EOL was Jan 2020; Python 3.7-3.9 are EOL)

## Step 1: Packaging - `setup.py` + `setup.cfg` → `pyproject.toml`

Convert from the legacy `setup.py` + `setup.cfg` pattern to a single `pyproject.toml` (PEP 621).

### Changes:
- Delete `setup.py` (move metadata to `pyproject.toml`)
- Delete `setup.cfg` (move pytest/coverage config to `pyproject.toml` or `pytest.ini`)
- Remove `MANIFEST.in` (include files via `[tool.setuptools.package-data]`)
- Create `pyproject.toml` with all metadata

## Step 2: Remove Python 2 Compatibility Code

### Dependencies to remove:
- `six` — no longer needed
- `RDFLib-JSONLD` — deprecated; built into RDFLib >= 6.0
- `Flask-Bootstrap` — unmaintained since 2019

### Code changes:
- Remove all `import six` and `from six import ...` statements
- Remove `if six.PY2` / `if six.PY3` branches
- Replace `from six.moves.urllib.parse import urlparse` with `from urllib.parse import urlparse`
- Replace `from six import b` with direct `b` prefix or `bytes()`
- Remove `from six import PY2` / `if PY2: ... else: ...` branching
- Replace `six.iteritems(d)` with `d.items()`
- Replace `six.iterkeys(d)` with `d.keys()`

### Files affected:
| File | What to change |
|------|---------------|
| `pyoslc/resources/models.py` | Remove `import six`, `six.PY2/PY3` branching in `digestion()` |
| `pyoslc/resources/domains/rm.py` | Remove `import six`, `six.iteritems` → `items()`, `six.iterkeys` → `keys()` |
| `pyoslc_oauth/resources.py` | Remove `import six`, `six.PY2/PY3` branching in `__to_resource()` |
| `pyoslc_oauth/forms.py` | Remove `from six import PY2`, `PY2`/`else` branching |
| `pyoslc/serializers/jazzxml.py` | Remove `from six import b`, use inline `\n` or `bytes()` |
| `pyoslc/serializers/configxml.py` | Remove `from six import b` |
| `app/api/adapter/namespaces/core.py` | `from six.moves.urllib.parse` → `from urllib.parse` |
| `pyoslc/resources/factories.py` | `from six.moves.urllib.parse` → `from urllib.parse` |
| `app/api/adapter/namespaces/config/routes.py` | `from six.moves.urllib.parse` → `from urllib.parse` |

## Step 3: Update Dependencies

Drop conditional version pins and update to modern versions:

| Library | Old version(s) | New version |
|---------|---------------|-------------|
| Flask | 1.0.2 / >1.0.2 | >=3.0.0 |
| Werkzeug | 1.0.1 / >1.0.1 | >=3.0.0 |
| Flask-RESTx | 0.5.1 / >0.5.1 | >=1.3.0 |
| RDFLib | 5.0.0 / >=6.0.0 | >=7.0.0 |
| python-dotenv | 0.18.0 / >0.18.0 | >=1.0.0 |
| Authlib | 0.14.3 | >=1.3.0 |
| cachelib | 0.1.1 | >=0.13.0 |
| Flask-SQLAlchemy | unversioned | >=3.1.0 |
| Flask-Login | unversioned | >=0.6.0 |
| Flask-WTF | unversioned | >=1.2.0 |
| Flask-CORS | unversioned | >=4.0.0 |
| requests | unversioned | >=2.31.0 |
| pytest | unversioned | >=8.0 |

**Removed packages:**
- `Flask-Bootstrap` (unmaintained) — replace with Bootstrap-Flask or plain Bootstrap
- `RDFLib-JSONLD` (merged into RDFLib core)
- `six` (Python 2 only)

## Step 4: Code Modernization

### 4a. `super(ClassName, self)` → `super()` (51 occurrences)

Use bare `super()` which works in Python 3 without arguments.

Affected files:
- `pyoslc/resources/models.py` (26+ calls)
- `pyoslc/resources/domains/config.py` (6 calls)
- `app/api/adapter/namespaces/core.py` (9 calls)
- `pyoslc_oauth/resources.py` (4 calls)
- `pyoslc/serializers/jazzxml.py` (1 call)
- `pyoslc/serializers/configxml.py` (1 call)
- `pyoslc/rest/resource.py` (1 call)
- `pyoslc/resources/jazz.py` (1 call)
- `app/api/adapter/namespaces/config/routes.py` (1 call)
- `app/api/adapter/namespaces/rm/csv_requirement_repository.py` (1 call)
- `app/api/adapter/services/specification.py` (1 call)

### 4b. Add `encoding='utf-8'` to text-mode `open()` calls (22 occurrences)

Files: `setup.py`, `initialize.py`, `routes.py`, `csv_requirement_repository.py`, `business.py`

### 4c. `%` string formatting → f-strings (4 occurrences)

- `app/api/adapter/services/specification.py:65`
- `app/api/adapter/resources/resource_service.py:36`
- `pyoslc/serializers/jazzxml.py:174`
- `app/api/adapter/namespaces/rm/routes.py:334`

### 4d. Old-style classes → inherit `object` (2 occurrences)

- `tests/functional/oslc.py:1` — `class PyOSLC:` → `class PyOSLC:`
- `pyoslc_oauth/resources.py:18` — `class OAuthServiceProvider:` → `class OAuthServiceProvider:`

Note: These are already new-style in Python 3 automatically, so this is optional but good practice.

### 4e. `.decode('utf-8') if not isinstance(data, str) else data`

In Python 3, `graph.serialize()` returns `bytes` for some formats and `str` for others. This pattern is correct but can be simplified:
- `pyoslc/rest/resource.py:87`
- `app/api/adapter/namespaces/core.py:143`
- `app/api/adapter/namespaces/rm/routes.py:78, 226`

### 4f. Remove `u''` string prefixes in docs

- `docs/source/conf.py`: `u'PyOSLC'` → `'PyOSLC'`, etc. (cosmetic)

## Step 5: Flask Configuration Updates

### `app/config.py`:
- `FLASK_ENV` is **deprecated** since Flask 2.3 (removed in 3.x). Use `app.debug` or `FLASK_DEBUG` env var.
- `SQLALCHEMY_TRACK_MODIFICATIONS = True` will be removed in future SQLAlchemy version. Set to `False` or remove.

### `.flaskenv`:
- `FLASK_ENV=development` → deprecated, use `FLASK_DEBUG=True`

## Step 6: Test & Tooling Config

### `tox.ini`:
- Update envlist: `py310, py311, py312` (remove `py27, py37, py38, py39`)
- Remove `py27`-specific deps if any

### `setup.cfg` pytest section:
- `minversion = 2.7` → `minversion = 8.0`
- Or migrate to `pyproject.toml`

## Step 7: Verify

```bash
# Install dev dependencies
pip install -e ".[dev,test]"

# Run linter
flake8 pyoslc app pyoslc_oauth tests

# Run tests
pytest -v

# Run with tox
tox
```
