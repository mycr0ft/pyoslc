# OSLC v3 Migration Plan

## Overview

This document identifies the changes needed to add OSLC Core v3 support to pyoslc
(the current codebase implements OSLC Core v2.0).

**Strategy**: Incremental — support both v2 and v3 simultaneously using the
`OSLC-Core-Version` header mechanism defined in the v3 spec (section 4.2). v3
servers that comply with v2 *MAY* continue to identify as v2 servers with
`OSLC-Core-Version: 2.0`.

## Summary of Key Changes

| Area | v2 Status | v3 Change |
|------|-----------|-----------|
| Version header | Hard-coded `2.0` | Negotiate v2/v3 based on request header |
| Content types | RDF/XML, JSON-LD | Add Turtle (`text/turtle`) |
| Well-known URIs | Not present | Add `/.well-known/oslc/sp-catalog` |
| Discovery (OPTIONS) | Not supported | Add OPTIONS with Link headers |
| ResourceShape | Commented out, non-functional | Implement and serve shapes |
| Error responses | Plain HTTP | Use `oslc:Error`/`oslc:ExtendedError` |
| Vocabulary | 21 classes, 82 properties | Add new v3 terms |
| Accept-Post headers | Not present | Add to creation factory responses |
| ldp:constrainedBy | Not present | Add constraint link headers |
| Version negotiation | Not supported | Core-48/49/50 compliance |
| Link headers | Not used for discovery | Add `resourceType`, `constrainedBy` Link headers |
| JSON-LD context | Not present | Add PrefixDefinition-based context |

## Phased Implementation Plan

### Phase 1: Core Infrastructure

#### 1.1 Version Negotiation

**Files**: `pyoslc/rest/resource.py`

- Read `OSLC-Core-Version` request header
- Support values `"2.0"` and `"3.0"`
- Default (no header): return `"2.0"` (backward compat, per Core-50)
- Set response `OSLC-Core-Version` to match the negotiated version
- If v3 requested, adjust serialization (e.g., use `oslc:` prefixed shape URIs, v3-style properties)

**Resources**:
- Core spec §4.2: Version Compatibility
- Core-43 through Core-53

#### 1.2 Turtle Support

**Files**: `pyoslc/rest/resource.py`

- Add `text/turtle` → `turtle` mapping in `create_response()`
- v3 spec Core-7: "SHOULD provide and accept RDF documents in Turtle format"
- Verify rdflib handles `turtle` format (it does)

#### 1.3 Update OSLC-Core-Version to Support "3.0"

**Files**: `pyoslc/rest/resource.py`

- Currently hard-coded: `response.headers['OSLC-Core-Version'] = '2.0'`
- Change to: `response.headers['OSLC-Core-Version'] = self.negotiated_version`
- Default to `"2.0"` when no header or v2 requested
- Set to `"3.0"` when v3 requested and supported

### Phase 2: Discovery Enhancements

#### 2.1 Well-known URI Bootstrap

**New endpoint**: `GET /.well-known/oslc/sp-catalog`

- SHOULD serve a ServiceProviderCatalog (DIS-4)
- Redirect to the actual catalog URI (DIS-6)

**Optional**: `GET /.well-known/oslc/rootservices.xml`

- Root Services document conforming to ROOT-SERVICES spec (DIS-3)

**Resources**:
- Discovery §4.2, DIS-3 through DIS-7

#### 2.2 OPTIONS Support on LDPCs

**Files**: `app/api/adapter/namespaces/core.py`

- Add `OPTIONS` handler to resource creation endpoints
- Return:
  - `Allow: POST,GET,OPTIONS,HEAD,PUT` header
  - `Accept-Post: text/turtle, application/ld+json` header
  - `Link: <http://www.w3.org/ns/ldp#BasicContainer>; rel="type"` header
  - `Link: <type-URI>; rel="http://open-services.net/ns/core#resourceType"` headers
  - `Link: <shape-URI>; rel="http://www.w3.org/ns/ldp#constrainedBy"` header (DIS-14)

**Resources**:
- Discovery §4.3 (DIS-8 through DIS-12)
- Discovery §4.4 (DIS-13 through DIS-16)

#### 2.3 Link Headers on GET/HEAD Responses

**Files**: `app/api/adapter/namespaces/core.py`

- On resource GET responses, add:
  - `Link: <resource-type>; rel="type"` for LDP type
  - `Link: <shape-URI>; rel="http://www.w3.org/ns/ldp#constrainedBy"` for constraints

### Phase 3: Resource Shape Implementation

#### 3.1 Uncomment and Complete ResourceShape Model

**Files**: `pyoslc/resources/models.py` (lines 1326-1374)

- Uncomment the `ResourceShape` class
- Complete it with:
  - `describes` (oslc:describes) — the rdf:type this shape constrains
  - `properties` (oslc:property) — list of Property objects
  - `title` (dcterms:title)
  - `instance_shape` may be referenced by resources via `oslc:instanceShape`

#### 3.2 Create Shape Serving Endpoint

**New endpoint**: `GET /services/shapes/{shape-name}`

- Serve ResourceShape documents in RDF/XML, JSON-LD, and Turtle
- Return shapes with `oslc:describes`, `oslc:property`, etc.

#### 3.3 Connect Shapes to Capabilities

- `QueryCapability.resource_shape` should reference a real shape URI
- `CreationFactory.resource_shape` should reference real shape URIs
- BaseResource `instance_shape` should reference the shape for each resource type

### Phase 4: Vocabulary Updates

#### 4.1 New v3 Terms

**Files**: `pyoslc/vocabularies/core.py`

Add these missing v3 vocabulary terms (new in v3 vs v2):

**New Classes**:
- `Any` — Any value type is allowed
- `Cardinality` — The number of allowed values for a property
- `Representation` — Specifies how a resource is represented
- `ResourceShapeConstraints` — Resource Shape Constraints metadata
- `ResourceValueType` — Specifies how an object reference is represented
- `ImpactType` — Enumeration of impact types
- `AllValues` (if needed for Resource Shape machinery)

**New Properties**:
- `cause` — An error that is a cause of this error
- `executes` — Link from a current action to the future action it realizes
- `futureAction` — Links to an action not currently executable
- `order` — Computed property for sorted query results
- `postBody` — POST body for next page retrieval
- `publisher` — (Archaic, use dcterms:publisher instead)
- `score` — Relevance score for query results
- `shortId` — Short ID property (some domains use it)

**Deduplicate**: Several terms appear twice in the set literal (Compact, Preview, 
document, hintHeight, hintWidth, initialHeight, icon, smallPreview, largePreview).
Clean these up.

**Verify against v3 vocabulary**: Cross-reference the full 27 classes and 81 properties
from the v3 spec with the current 21 classes and 82 properties. Some renames/deprecations
may apply.

#### 4.2 Deprecation Markers

The v3 spec marks these as Archaic:
- `oslc:initialHeight` (use `oslc:hintHeight`/`oslc:hintWidth` instead)
- `oslc:publisher` (use `dcterms:publisher` instead)

Add deprecation comments but keep them for backward compat.

### Phase 5: Error Response Improvements

#### 5.1 Structured OSLC Error Responses

**Files**: `app/api/adapter/namespaces/core.py`, `pyoslc/rest/resource.py`

- When v3 version is negotiated, return structured `oslc:Error` / `oslc:ExtendedError`
  responses instead of plain HTML/JSON error bodies
- Error response should include:
  - `oslc:statusCode` (integer HTTP status)
  - `oslc:message` (human-readable message)
  - `oslc:extendedError` (optional, additional details)

#### 5.2 Error Handler Registration

- Register Flask error handlers that produce OSLC Error responses
- Support content negotiation for error responses

### Phase 6: Existing Bug Fixes (for v2 as well)

While doing v3 work, fix these existing bugs found during analysis:

1. **`BaseResource.add_contributor()`** — uses `.append()` on `set()`, should use `.add()`
   (Same for `add_creator()`, `add_subject()`, `add_type()`)
2. **`OAuthConfiguration.__init__`** — default value for `oauth_request_token_uri` 
   references `oauth_access_token_uri` instead of `oauth_request_token_uri`
3. **`OAuthConfiguration.to_rdf()`** — uses property URI `OSLC.oauthConfiguration` 
   as rdf:type instead of class URI `OSLC.OAuthConfiguration`
4. **`ResourceShape`** — fully commented out, needs to be made functional

### Phase 7: Testing

- Update existing tests to verify v3 responses
- Add tests for version negotiation
- Add tests for Turtle serialization
- Add tests for OPTIONS endpoints
- Add tests for ResourceShape serving
- Verify backward compat: existing v2 clients should see no change

## References

### OSLC Core v3 Specification Parts

1. **Part 1: Overview** — Version compatibility (§4.2), capabilities overview
2. **Part 2: Discovery** — Well-known URIs, OPTIONS, Link headers, SPC/SP/Service shapes
3. **Part 3: Resource Preview** — Compact/Preview resources
4. **Part 4: Delegated Dialogs** — Dialog resources
5. **Part 5: Attachments** — Attachment container/descriptor
6. **Part 6: Resource Shape** — ResourceShape, Property, constraint definitions
7. **Part 7: Vocabulary** — Complete term definitions (27 classes, 81 properties)
8. **Part 8: Constraints** — Standard shape constraints on Core terms

### Current Implementation Files

| File | Relevance |
|------|-----------|
| `pyoslc/rest/resource.py` | Version header, content negotiation, serialization |
| `pyoslc/resources/models.py` | All resource model classes, including commented-out ResourceShape |
| `app/api/adapter/namespaces/core.py` | Discovery endpoints, CRUD operations, preview/dialogs |
| `app/api/adapter/services/providers.py` | ServiceProviderCatalog singleton, provider initialization |
| `app/api/adapter/services/specification.py` | Specification classes defining capabilities |
| `app/api/adapter/exceptions.py` | Custom HTTP exceptions |
| `pyoslc/vocabularies/core.py` | OSLC Core vocabulary definitions |
| `app/api/adapter/dialogs/routes.py` | Dialog UI endpoints |
| `app/api/adapter/namespaces/config/routes.py` | Config management dialogs |

## Quick Wins (can be done first)

1. Add Turtle serialization to `create_response()` (~5 lines)
2. Fix BaseResource `set.append()` bug (~4 lines)
3. Fix OAuthConfiguration type URI bug (~2 lines)
4. Fix OAuthConfiguration default value bug (~1 line)
5. Add OPTIONS handler to creation endpoints (~20 lines)
6. Add version negotiation with default v2 fallback (~15 lines)
