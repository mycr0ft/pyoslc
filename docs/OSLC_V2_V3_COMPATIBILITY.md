# OSLC Core v2 / v3 Compatibility

## Overview

PyOSLC started as an OSLC Core v2.0 implementation. The `oslc-v3` branch adds
backward-compatible OSLC Core v3.0 support so that both v2 and v3 clients can
use the same server.

**Design principle**: The server defaults to `OSLC-Core-Version: 2.0` behavior
when no version header is sent (per spec Core-50). Clients that send
`OSLC-Core-Version: 3.0` receive v3-style responses. All existing v2
functionality is preserved.

---

## Key Differences Between v2 and v3

| Feature | v2 | v3 |
|---|---|---|
| **Version header** | Not used (`2.0` assumed) | `OSLC-Core-Version` request/response header |
| **Turtle format** | Optional | SHOULD support (`text/turtle`) |
| **Well-known URIs** | Not defined | `/.well-known/oslc/sp-catalog` (DIS-4) |
| **Discovery (OPTIONS)** | Not defined | Link headers, Allow, Accept-Post (DIS-8–DIS-12) |
| **LDP compatibility** | Not required | Link headers with `rel="type"` (LDP) |
| **Resource shapes** | Optional, loosely defined | `oslc:ResourceShape` with `oslc:Property` |
| **Error responses** | Plain text / HTML | Structured `oslc:Error` / `oslc:ExtendedError` |
| **Shape constraints** | Not linked | `constrainedBy` Link header + `oslc:instanceShape` |
| **Content negotiation** | RDF/XML, JSON | Add JSON-LD, Turtle |
| **Vocabulary** | ~21 classes, ~82 properties | 27 classes, 81 properties |
| **Delegated dialogs** | Dialog resources | Unchanged (backward compat) |
| **Resource preview** | Compact / Preview | Unchanged |

---

## Adaptations Made

### Version Negotiation
**File**: `pyoslc/rest/resource.py`

- `get_requested_version()` reads the `OSLC-Core-Version` request header
- Valid values: `"2.0"` and `"3.0"`; defaults to `"2.0"` when absent or invalid
- All responses carry `OSLC-Core-Version` matching the request

The `create_response()` method applies it automatically to every response.

### Turtle Support
**File**: `pyoslc/rest/resource.py`

`text/turtle` is now accepted and mapped to the `turtle` rdflib serializer.

### Well-Known URI
**File**: `app/web/routes.py`

`GET /.well-known/oslc/sp-catalog` redirects (HTTP 302) to the real catalog at
`/oslc/services/catalog`, satisfying DIS-6.

### OPTIONS Discovery
**File**: `app/api/adapter/namespaces/core.py`

Every OSLC resource endpoint now has an `OPTIONS` handler returning `Allow`,
`OSLC-Core-Version`, and (for LDP containers) `Accept-Post` headers.

| Endpoint | Allow |
|---|---|
| `/services/catalog` | `GET, OPTIONS, HEAD` |
| `/services/provider/{id}` | `GET, OPTIONS, HEAD` |
| `/services/provider/{id}/resources/requirement` | `POST, GET, OPTIONS, HEAD, PUT` |
| `/services/provider/{id}/resources/requirement/{req}` | `GET, PUT, DELETE, OPTIONS, HEAD` |
| `/services/resourceShapes/{name}` | `GET, OPTIONS, HEAD` |
| `/services/rootservices` | `GET, OPTIONS, HEAD` |

### LDP Link Headers
**File**: `app/api/adapter/namespaces/core.py`

- Collection endpoints (catalog, provider, query result) send:
  `Link: <http://www.w3.org/ns/ldp#BasicContainer>; rel="type"`
- Single-resource endpoints send:
  `Link: <http://www.w3.org/ns/ldp#Resource>; rel="type"`

### Resource Shapes
**File**: `pyoslc/resources/models.py`

- New `ResourceShape` and `Property` model classes with full `to_rdf()` serialization
- Served at `GET /services/resourceShapes/{name}` in RDF/XML, JSON-LD, and Turtle
- The requirement shape defines all 15 properties from the domain model with
  proper `oslc:occurs`, `oslc:valueType`, and `oslc:propertyDefinition`

**File**: `app/api/adapter/services/shapes.py` (new)

- `build_requirement_shape()` creates the `requirement` shape describing
  `oslc_rm:Requirement`

**File**: `pyoslc/resources/domains/rm.py`

- Resources now serialize `oslc:instanceShape` pointing to their shape URI

### Vocabulary Updates
**File**: `pyoslc/vocabularies/core.py`

- Added 6 new v3 classes: `Any`, `Cardinality`, `ImpactType`, `Representation`,
  `ResourceShapeConstraints`, `ResourceValueType`
- Added 3 new v3 properties: `cause`, `order`, `score`
- Removed 9 duplicate terms that appeared twice in the set literal

### Structured Error Responses
**File**: `pyoslc/resources/models.py`

- New `Error` and `ExtendedError` model classes

**File**: `pyoslc/rest/resource.py`

- `build_error_response()` helper creates an RDF graph with `oslc:Error`, sets
  `oslc:statusCode` and `oslc:message`

**File**: `app/api/adapter/__init__.py`

- Blueprint error handlers for 400, 404, 406, 415, 500 return structured OSLC
  errors instead of plain text or JSON

### Existing Bug Fixes (v2 and v3)

- `BaseResource` set accessors: `append()` → `add()` (4 methods)
- `OAuthConfiguration` `rdf:type`: property URI → class URI
- `OAuthConfiguration` default value: references `oauth_request_token_uri`
  instead of `oauth_access_token_uri`

---

## Backward Compatibility

All existing v2 behavior is preserved:

- Requests without `OSLC-Core-Version` get `2.0` responses
- Existing v2 resource representations are unchanged
- All 34 existing tests pass without modification
- No database or configuration changes required

---

## References

- [OSLC Core v3.0 Part 1: Overview](https://docs.oasis-open-projects.org/oslc-op/core/v3.0/csprd03/part1-overview/oslc-core-v3.0-csprd03-part1-overview.html)
- [OSLC Core v3.0 Part 2: Discovery](https://docs.oasis-open-projects.org/oslc-op/core/v3.0/csprd03/part2-discovery/oslc-core-v3.0-csprd03-part2-discovery.html)
- [OSLC Core v3.0 Part 6: Resource Shape](https://docs.oasis-open-projects.org/oslc-op/core/v3.0/csprd03/part6-resource-shape/oslc-core-v3.0-csprd03-part6-resource-shape.html)
- [OSLC Core v3.0 Part 7: Vocabulary](https://docs.oasis-open-projects.org/oslc-op/core/v3.0/csprd03/part7-core-vocabulary/oslc-core-v3.0-csprd03-part7-core-vocabulary.html)
- [OSLC Core v3.0 Part 8: Constraints](https://docs.oasis-open-projects.org/oslc-op/core/v3.0/csprd03/part8-constraints/oslc-core-v3.0-csprd03-part8-constraints.html)
- [Migration Plan](OSLC_V3_MIGRATION.md)
