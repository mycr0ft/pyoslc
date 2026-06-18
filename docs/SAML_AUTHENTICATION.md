# SAML Authentication for pyoslc

pyoslc does not have built-in SAML support, but the existing dependency stack
makes adding SAML Service Provider (SP) authentication straightforward.

## Existing Pieces That Apply

| Component | What it provides |
|---|---|
| **Authlib** (1.x) | `AuthlibSAMLRPClient` — SAML SP client: IdP metadata parsing, AuthnRequest generation, assertion validation, SLO |
| **Flask-Login** | Session management after SAML auth — just call `login_user(user)` in the ACS route |
| **pyoslc_oauth blueprint pattern** | Proves how to add auth routes: create a blueprint, register it in `init_app` |
| **Flask-SQLAlchemy / User model** | `pyoslc_oauth/models.py` has a `User` model — can be reused or extended for SAML-asserted identities |

## Dependencies

Authlib's SAML support requires `xmlsec1` at the system level and the `authlib[saml]`
extra at the Python level:

```bash
# System
sudo apt install xmlsec1          # Debian/Ubuntu
sudo dnf install xmlsec1          # Fedora
brew install xmlsec1              # macOS

# Python
uv add 'authlib[saml]>=1.0,<2.0'
```

## Proposed Implementation

```
app/api/saml/
├── __init__.py
├── routes.py          — SP login, ACS, metadata endpoints
└── duo_config.py      — DUO-specific IdP metadata helpers (optional)
```

### SP Metadata Flow (DUO)

DUO's SAML integration provides IdP metadata at a URL like:

```
https://sso.duosecurity.com/saml2/sp/metadata/<integration-key>
```

The SP metadata (your pyoslc instance) must be registered with DUO so it knows
the ACS URL and audience. Authlib can generate this automatically.

### Route Outline

```python
# app/api/saml/routes.py
from flask import Blueprint, request, redirect
from flask_login import login_user, logout_user, login_required
from authlib.integrations.flask_client import (
    SamlClient, SamlClientConfig, SamlClientError
)
from pyoslc_oauth.models import User

saml_bp = Blueprint('saml', __name__, url_prefix='/saml')

@saml_bp.route('/login')
def sp_login():
    """Initiate SP-initiated SSO — redirect to DUO."""
    ...

@saml_bp.route('/acs', methods=['POST'])
def acs():
    """Assertion Consumer Service: DUO POSTs the SAML response here."""
    # 1. Validate SAML response via AuthlibSAMLRPClient
    # 2. Extract name_id / attributes
    # 3. Find-or-create User
    # 4. login_user(user)
    # 5. Redirect to original target (or /)
    ...

@saml_bp.route('/metadata')
def sp_metadata():
    """Return SP metadata XML for registration in DUO admin."""
    ...

@saml_bp.route('/logout')
@login_required
def sp_logout():
    """Local logout (SLO optional)."""
    logout_user()
    return redirect('/')
```

### Registration

In `app/__init__.py` (or a new `app/api/saml/__init__.py` called from
`create_app`):

```python
from app.api.saml.routes import saml_bp
app.register_blueprint(saml_bp)
```

### Configuration

Add to `app/config.py` or a `.env` file:

```python
SAML_METADATA_URL = "https://sso.duosecurity.com/saml2/sp/metadata/<integration-key>"
SAML_ACS_URL = "https://your-pyoslc-instance/saml/acs"
SAML_ENTITY_ID = "pyoslc"
SAML_IDP_CERT = "..."  # or load from file
```

### User Mapping

The ACS route maps the SAML assertion to a local `User`. Common strategies:

| SAML Attribute | User Model Field |
|---|---|
| `name_id` (email) | `User.username` |
| `Email` / `mail` | `User.email` |
| `givenName` | `User.display_name` |

Use `User.query.filter_by(username=name_id).first()` and create the user if
they don't exist (JIT provisioning).

## DUO-Specific Notes

- DUO acts as the SAML **IdP**. pyoslc is the **SP**.
- DUO's SAML integration uses **HTTP-POST** binding for both login and ACS
  (not Artifact or PAOS).
- The IdP metadata URL includes the **integration key** (provided by DUO admin).
- DUO requires the SP ACS URL to be registered exactly — Authlib's `SAML_ACS_URL`
  must match what you enter in the DUO admin console.
- DUO's assertion typically includes `email`, `groups`, `given_name`, `family_name`
  as SAML attributes (configurable per integration).
- Pyoslc should accept IdP-initiated SSO too (DUO dashboard → pyoslc tile):
  the ACS endpoint is the same; just handle the `RelayState` to redirect to the
  right app page.

## Comparison with Existing OAuth1

| Aspect | OAuth1 (current) | SAML (proposed) |
|---|---|---|
| Use case | Machine-to-machine (consumer key/secret) | Browser SSO (user login) |
| Flask-Login session | After `login()` in `PyOSLCApplication` | After ACS assertion validation |
| User creation | Manual DB entry | JIT provisioning from assertion |
| Auth protocol | HMAC-SHA1 signed requests | XML signature / XML Encryption |
| Library | Authlib OAuth1Server | AuthlibSAMLRPClient |

Both can coexist — OAuth1 for API client identification, SAML for UI login.

## References

- [Authlib SAML SP Client docs](https://docs.authlib.org/en/latest/client/saml.html)
- [Authlib Flask SAML example](https://github.com/lepture/authlib/tree/main/example/saml)
- [DUO SAML Integration Guide](https://duo.com/docs/sso)
