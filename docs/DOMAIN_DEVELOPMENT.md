# OSLC Domain Development Guide

This document describes how the OSLC Requirements Management (RM) domain is
implemented in pyoslc and how to add a new domain.

## Architecture Overview

Each OSLC domain in pyoslc is spread across four layers:

| Layer | Location | RM Example |
|---|---|---|
| Vocabulary | `pyoslc/vocabularies/{domain}.py` | `rm.py` — `OSLC_RM` ClosedNamespace |
| Resource model | `pyoslc/resources/domains/{domain}.py` | `rm.py` — `Requirement`, `RequirementCollection` |
| Adapter namespace | `app/api/adapter/namespaces/{domain}/` | `rm/` — routes, models, parsers |
| Services | `app/api/adapter/services/` | `shapes.py`, `specification.py` |

The adapter namespace is registered in
`app/api/adapter/oslc.py` and served under
`/oslc/services/rm/` (blueprint prefix `/oslc` + namespace `path='/rm'`).

## Layer-by-Layer Breakdown (RM Reference)

### 1. Vocabulary (`pyoslc/vocabularies/rm.py`)

Defines the OSLC namespace as an `rdflib.ClosedNamespace` so RDF serialisation
uses the `oslc_rm:` prefix instead of expanding the full URI.

```python
OSLC_RM = ClosedNamespace(
    uri=URIRef("http://open-services.net/ns/rm#"),
    terms=[
        "Requirement", "RequirementCollection",
        "affectedBy", "elaboratedBy", "implementedBy",
        "specifiedBy", "satisfiedBy", "trackedBy", "validatedBy",
        "uses", "elaborates", "specifies", "satisfies",
        "decomposedBy", "decomposes", "constrainedBy", "constrains",
        "rmServiceProviders",
    ]
)
```

The namespace is imported by the resource model, the routes, and the shapes.

### 2. Resource Model (`pyoslc/resources/domains/rm.py`)

`Requirement` extends `BaseResource` (from `pyoslc/resources/models.py`) with
RM-specific properties (`elaborated_by`, `specified_by`, etc.).

Domain models implement four serialisation methods:

| Method | Input | Output |
|---|---|---|
| `to_rdf(graph, base_url, attributes)` | `rdflib.Graph` | Same graph with triples added |
| `from_json(data, attributes)` | JSON dict | Mutates `self` |
| `from_rdf(g, attributes)` | `rdflib.Graph` | Mutates `self` |
| `to_mapped_object(attributes)` | — | Plain dict for CSV/DB |

The `attributes` parameter is the **specification map** — a dict that bridges
external field names to private mangled attribute names and OSLC property URIs:

```python
# app/api/adapter/mappings/specification.py
specification_map = {
    'Title':      {'attribute': '_BaseResource__title',       'oslc_property': 'DCTERMS.title'},
    'Source':     {'attribute': '_Requirement__elaborated_by','oslc_property': 'OSLC_RM.elaboratedBy'},
    'Status':     {'attribute': '_Requirement__decomposed_by','oslc_property': 'OSLC_RM.decomposedBy'},
    ...
}
```

### 3. Adapter Namespace (`app/api/adapter/namespaces/rm/`)

```
rm/
├── __init__.py    — Namespace definition + resource registration
├── routes.py      — Flask-RESTx Resource classes (RequirementList, RequirementItem)
├── models.py      — Swagger/Flask-RESTx model definitions
├── parsers.py     — Request parser definitions
├── csv_requirement_repository.py
├── oxigraph_requirement_repository.py
```

#### `__init__.py`

Creates a `flask_restx.Namespace` and registers route classes:

```python
rm_ns = Namespace(name='rm', description='Requirements Management', path='/rm')
rm_ns.add_resource(RequirementList, "/requirement")
rm_ns.add_resource(RequirementItem, "/requirement/<string:id>")
```

#### `routes.py`

Each route class is a `flask_restx.Resource` subclass. The `RequirementList`
class handles `GET` (list all) and `POST` (create). The `RequirementItem` class
handles `GET` (single), `PUT` (update), and `DELETE`.

Key pattern — routes delegate to `business.py`, not to repositories directly:

```python
from app.api.adapter.namespaces.business import create_requirement
```

#### `models.py`

Flask-RESTx models for Swagger documentation. Two levels:

- `base_requirement` — core fields (title, description, identifier, ...)
- `requirement` — inherits base + RM-specific fields (elaborated_by, ...)
- `specification` — flat field list used by the POST/PUT parser

#### `parsers.py`

`reqparse.RequestParser` definitions mapping HTTP form fields to internal fields.

### 4. Business Layer (`app/api/adapter/namespaces/business.py`)

A thin layer between routes and the repository:

- Calls `get_requirement_repository()` to obtain the configured backend
- Constructs `Requirement` domain objects from input data
- Delegates to `repo.find()` / `.list()` / `.create()` / `.update()` / `.delete()`

### 5. Repository (`app/api/adapter/resources/repository.py`)

The `RequirementRepository` ABC defines the interface:

```
find(id: str)       → Requirement | None
list()              → list[Requirement]
create(requirement) → None (raises on duplicate)
update(id, req)     → None (raises NotFound)
delete(id)          → bool (raises NotFound)
csv_path()          → str | None
```

Two implementations exist:

| Backend | Class | File |
|---|---|---|
| CSV | `CsvRequirementRepository` | `rm/csv_requirement_repository.py` |
| Oxigraph | `OxigraphRequirementRepository` | `rm/oxigraph_requirement_repository.py` |

The factory `get_requirement_repository()` in `repository.py` selects the
implementation based on `STORAGE_BACKEND` in app config.

### 6. Shapes (`app/api/adapter/services/shapes.py`)

`build_requirement_shape()` constructs a `ResourceShape` with `Property`
definitions for each OSLC RM property (identifier, title, description, creator,
shortTitle, subject, elaboratedBy, specifiedBy, constrainedBy, etc.).

Served at `/oslc/services/resourceShapes/requirement`.

### 7. Service Provider Registration (`app/api/adapter/services/specification.py`)

The `Specification` class (extends `ServiceResource`) declares the RM domain's
OSLC capabilities:

```python
class Specification(ServiceResource):
    domain = 'http://open-services.net/ns/rm#'
    service_path = 'provider/{id}/resources'
```

It implements `query_capability()`, `creation_factory()`,
`selection_dialog()`, and `creation_dialog()` — each returning a dict that
populates the service provider's service listing.

The service provider is wired through:

- `app/api/adapter/manager.py` — `CSVImplementation.get_service_provider_info()`
  returns metadata for providers (currently hardcoded to `Project-1` /
  `Specification`).
- `app/api/adapter/services/factories.py` — `ContactServiceProviderFactory`
  builds the provider from registered service resources.
- `app/api/adapter/services/providers.py` — `ServiceProviderCatalogSingleton`
  manages the catalog and provider instances.

### 8. Adapter Namespace Registration (`app/api/adapter/oslc.py`)

```python
api.add_namespace(adapter_ns)   # core OSLC endpoints (catalog, provider, shapes, ...)
api.add_namespace(rm_ns)        # RM-specific endpoints (/requirement, /requirement/<id>)
api.add_namespace(config_ns)    # configuration management
```

The blueprint is registered in `app/__init__.py`:

```python
from app.api.adapter import oslc
oslc.init_app(app)
```

## Adding a New Domain

This section walks through adding a Quality Management (QM) domain as an
example. The same steps apply to any OSLC domain (CM, AM, etc.).

### Step 1 — Create a Vocabulary

**File:** `pyoslc/vocabularies/qm.py`

Define a `ClosedNamespace` with the OSLC QM URI and the terms your domain
needs. See the [OSLC QM vocabulary](http://open-services.net/ns/qm) for the
full list.

### Step 2 — Create a Resource Model

**File:** `pyoslc/resources/domains/qm.py`

Extend `BaseResource` (or another domain model if yours inherits from one) with
domain-specific properties. Implement or override `to_rdf`, `from_json`,
`from_rdf`, and `to_mapped_object` as needed.

A stub already exists:

```python
class TestCase(BaseResource):
    pass
```

Replace `pass` with proper QM properties (e.g. `tested_by`, `validates`, `uses`, ...)
following the `Requirement` pattern in `rm.py`.

### Step 3 — Create a Specification Map

**File:** `app/api/adapter/mappings/specification_qm.py`

Map external field names to private attributes and OSLC property URIs for the
new domain. Alternatively, extend the existing `specification.py` map.

### Step 4 — Create an Adapter Namespace

```
app/api/adapter/namespaces/qm/
├── __init__.py    — Namespace + resource registration
├── routes.py      — Resource classes
├── models.py      — Swagger models
├── parsers.py     — Request parsers
```

Follow the `rm/` structure exactly:

- `__init__.py`: create `qm_ns = Namespace(...)`, call `add_resource()`
- `routes.py`: implement `TestCaseList(Resource)` and `TestCaseItem(Resource)`,
  delegate business logic to `business.py` (extend it with QM functions)
- `models.py`: define Flask-RESTx models for Swagger
- `parsers.py`: define `reqparse.RequestParser` instances

### Step 5 — Add Business Functions

Extend `app/api/adapter/namespaces/business.py` with QM-specific functions
(`get_test_case`, `create_test_case`, etc.) — or create a separate
`business_qm.py` for clarity.

The functions should use the repository factory pattern via
`get_requirement_repository()` if the same storage backend is reused, or a new
repository ABC if QM needs different storage semantics.

### Step 6 — Add Shapes

Extend `app/api/adapter/services/shapes.py` with a
`build_test_case_shape()` function that defines the QM resource shape
properties.

Register it in `app/api/adapter/namespaces/core.py` so it's served at
`/oslc/services/resourceShapes/testcase`.

### Step 7 — Add a Service Resource

**File:** `app/api/adapter/services/specification.py`

Add a `TestCase(ServiceResource)` class analogous to `Specification`:

```python
class TestCase(ServiceResource):
    domain = 'http://open-services.net/ns/qm#'
    service_path = 'provider/{id}/resources'

    @staticmethod
    def query_capability():
        return {
            'title': 'Query Capability',
            'label': 'Test Case Query',
            'resource_shape': 'resourceShapes/testcase',
            'resource_type': ['http://open-services.net/ns/qm#TestCase'],
            'usages': []
        }
```

If the QM domain should appear as a separate service provider, add a new entry
in `app/api/adapter/manager.py`:

```python
service_providers.append({
    'id': 'Project-2',
    'name': 'PyOSLC Service Provider for QM',
    'class': TestCase   # your new ServiceResource subclass
})
```

If it should share the existing provider, add the QM capabilities to the
existing `Specification` class instead.

### Step 8 — Implement a Repository (Optional)

If the new domain needs its own storage (not sharing the RM CSV/Oxigraph
backends), create a repository ABC and implementation(s):

- `app/api/adapter/resources/qm_repository.py` — ABC
- `app/api/adapter/namespaces/qm/csv_test_case_repository.py`
- Or reuse `RequirementRepository` if the storage model is compatible

If sharing RM's storage, the existing `get_requirement_repository()` factory
can be used by QM business functions directly.

### Step 9 — Register the Namespace

In `app/api/adapter/oslc.py`, add:

```python
from app.api.adapter.namespaces.qm import qm_ns
api.add_namespace(qm_ns)
```

### Step 10 — Add Tests

Add test cases in the test suite following the existing RM test pattern.
At minimum, test CRUD operations for the new domain's endpoints.

## Summary of Files to Create/Modify

| Action | File |
|---|---|
| **Create** | `pyoslc/vocabularies/{domain}.py` |
| **Create** | `pyoslc/resources/domains/{domain}.py` |
| **Create** | `app/api/adapter/mappings/specification_{domain}.py` |
| **Create** | `app/api/adapter/namespaces/{domain}/__init__.py` |
| **Create** | `app/api/adapter/namespaces/{domain}/routes.py` |
| **Create** | `app/api/adapter/namespaces/{domain}/models.py` |
| **Create** | `app/api/adapter/namespaces/{domain}/parsers.py` |
| **Modify** | `app/api/adapter/namespaces/business.py` (add functions) |
| **Modify** | `app/api/adapter/services/shapes.py` (add shape builder) |
| **Modify** | `app/api/adapter/services/specification.py` (add ServiceResource) |
| **Modify** | `app/api/adapter/manager.py` (add provider entry) |
| **Modify** | `app/api/adapter/oslc.py` (register namespace) |
| **Modify** | `app/api/adapter/namespaces/core.py` (register shape route) |
| *Optional* | `app/api/adapter/resources/{domain}_repository.py` (ABC) |
| *Optional* | `app/api/adapter/namespaces/{domain}/*_repository.py` (impl) |

## Multi-Domain Architecture

OSLC v3 (and v2) allows a single server to serve multiple domains. The
`ServiceProviderCatalog` → `ServiceProvider` → `Service` hierarchy is designed
for this — each `Service` declares a `domain` URI, and a single provider can
aggregate services from any number of domains.

### How pyoslc Currently Supports Multi-Domain

| Mechanism | Status | Details |
|---|---|---|
| **Domain namespace isolation** | Already works | Each domain gets its own `Namespace` (`rm_ns`, `qm_ns`, ...) at its own URL prefix (`/rm`, `/qm`, ...) |
| **Service domain declaration** | Already works | Each `ServiceResource` subclass (`Specification`, `TestCase`, ...) declares `domain = <namespace URI>` |
| **Catalog domain aggregation** | Already works | `ServiceProviderCatalogSingleton.get_domains()` iterates all services' `.domain` attributes automatically |
| **Provider-level routes** | Hardcoded to RM | `/provider/<id>/resources/requirement` in `core.py` is the only provider resource route |

### Two Approaches for Provider-Level Routes

Each approach uses the same per-domain namespace routes (`/rm/requirement`,
`/qm/testcase`, etc.) but differs in how the OSLC provider-level discovery
routes (`/provider/<id>/resources/<resource-type>`) are structured.

#### Approach A — Per-domain provider routes in `core.py` (simpler, recommended)

Add routes to `core.py` for each new domain alongside the existing RM routes:

| Route | Domain | Route class |
|---|---|---|
| `/provider/<id>/resources/requirement` | RM | `ResourceOperation` (existing) |
| `/provider/<id>/resources/requirement/<rid>` | RM | `ResourcePreview` (existing) |
| `/provider/<id>/resources/testcase` | QM | `TestResourceOperation` (new) |
| `/provider/<id>/resources/testcase/<rid>` | QM | `TestResourcePreview` (new) |

Each new route class duplicates the pattern from `ResourceOperation` /
`ResourcePreview` but calls QM-specific business functions (`get_test_case_list`,
`create_test_case`, etc.) and QM-specific shapes (`resourceShapes/testcase`).

**Pros:** No refactoring of existing code; fully isolated; additive changes only.
**Cons:** Duplicates routing logic for each domain.

#### Approach B — Domain-agnostic dispatch (cleaner for 5+ domains)

Refactor `core.py` to parameterize the resource type in the URL:

```python
@adapter_ns.route('/provider/<service_provider_id>/resources/<domain_type>')
class ResourceOperation(OslcResource):

    def get(self, service_provider_id, domain_type):
        business = _domain_dispatch(domain_type)
        data = business.list(...)
        ...

    def post(self, service_provider_id, domain_type):
        business = _domain_dispatch(domain_type)
        resource = business.create(...)
        ...

@adapter_ns.route('/provider/<service_provider_id>/resources/<domain_type>/<resource_id>')
class ResourcePreview(OslcResource):
    ...
```

Where `_domain_dispatch()` maps `domain_type` to the correct business module:

```python
_domain_registry = {
    'requirement': 'app.api.adapter.namespaces.business',
    'testcase':    'app.api.adapter.namespaces.business_qm',
}

def _domain_dispatch(domain_type):
    module = importlib.import_module(_domain_registry[domain_type])
    return module
```

**Pros:** One route definition drives all domains; adding a domain is a
single-entry registry update.
**Cons:** Touches `core.py`, `business.py`, and the repository factory;
requires `importlib` or a registry pattern.

### Service Provider Registration for Multiple Domains

The `Specification` class in `specification.py` declares the RM domain. For a
second domain, add a sibling class:

```python
# Already in specification.py — add this:
class TestCase(ServiceResource):
    domain = 'http://open-services.net/ns/qm#'
    service_path = 'provider/{id}/resources'

    @staticmethod
    def query_capability():
        return {
            'title': 'Query Capability',
            'label': 'Test Case Query',
            'resource_shape': 'resourceShapes/testcase',
            'resource_type': ['http://open-services.net/ns/qm#TestCase'],
            'usages': []
        }

    @staticmethod
    def creation_factory():
        return {
            'title': 'Creation Factory',
            'label': 'Test Case Factory',
            'resource_shape': ['resourceShapes/testcase'],
            'resource_type': ['http://open-services.net/ns/qm#TestCase'],
            'usages': []
        }
```

In `manager.py`, you can either:

1. **Share one provider** — add the new class's capabilities to the existing
   `Specification` class so the `Project-1` provider serves both domains.

2. **Separate providers** — add a new entry so each domain gets its own provider:

```python
service_providers = [
    {
        'id': 'Project-1',
        'name': 'PyOSLC Service Provider for RM',
        'class': Specification
    },
    {
        'id': 'Project-2',
        'name': 'PyOSLC Service Provider for QM',
        'class': TestCase
    },
]
```

The catalog automatically aggregates domains from all registered providers
(`ServiceProviderCatalogSingleton.get_domains()`).

### URL Layout Comparison

A single-domain server (RM only) exposes:

```
/oslc/services/catalog
/oslc/services/provider/Project-1
/oslc/services/provider/Project-1/resources/requirement
/oslc/services/provider/Project-1/resources/requirement/{id}
/oslc/services/rm/requirement
/oslc/services/rm/requirement/{id}
/oslc/services/resourceShapes/requirement
```

A multi-domain server (RM + QM) exposes:

```
/oslc/services/catalog
/oslc/services/provider/Project-1              (RM)
/oslc/services/provider/Project-2              (QM)
/oslc/services/provider/Project-1/resources/requirement
/oslc/services/provider/Project-1/resources/requirement/{id}
/oslc/services/provider/Project-2/resources/testcase
/oslc/services/provider/Project-2/resources/testcase/{id}
/oslc/services/rm/requirement
/oslc/services/rm/requirement/{id}
/oslc/services/qm/testcase
/oslc/services/qm/testcase/{id}
/oslc/services/resourceShapes/requirement
/oslc/services/resourceShapes/testcase
```

The ServiceProviderCatalog at `/oslc/services/catalog` lists both `Project-1`
and `Project-2`, each advertising its domain's services.
