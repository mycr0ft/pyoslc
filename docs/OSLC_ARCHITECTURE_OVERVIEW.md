# OSLC Architecture Overview

This document introduces OSLC (Open Services for Lifecycle Collaboration) for
someone new to the standard, then maps each concept to how pyoslc (the server)
and pyoslc-client implement it.

## What Is OSLC?

OSLC is an open standard for integrating engineering tools. It defines how
tools share data and link to each other over HTTP using REST and Linked Data
principles.

The core idea: every engineering artifact (requirement, test case, change
request, defect, ...) is a **resource** identified by a URL. Tools create, read,
update, and delete these resources via HTTP, and link between them using
standardised RDF properties.

## Key OSLC Concepts

### Service Provider Catalog

The entry point. A URL that returns a list of **Service Providers** available
on the server. Think of this as a table of contents for the server.

```
GET /oslc/services/catalog → list of providers
```

In pyoslc: `ServiceProviderCatalogSingleton` at `/oslc/services/catalog`
returns the catalog with all registered providers.

### Service Provider

Represents a tool or project that exposes resources. Each provider advertises
its **Services** — capabilities like "list requirements", "create test cases",
"search change requests".

```
GET /oslc/services/provider/Project-1 → provider metadata + list of services
```

In pyoslc: `ContactServiceProviderFactory` builds providers from the
`ServiceResource` subclasses registered in `manager.py`.

### Service

A capability within a provider, scoped to a **domain** (RM, QM, CM, AM, ...).
Each service includes:

- **Query Capability** — list/search resources
- **Creation Factory** — create new resources via POST
- **Selection Dialog** — pick a resource via a UI
- **Creation Dialog** — create a resource via a UI dialog

Services are defined by the `ServiceResource` subclass in
`app/api/adapter/services/specification.py`:

```python
class Specification(ServiceResource):
    domain = 'http://open-services.net/ns/rm#'
    service_path = 'provider/{id}/resources'

    def query_capability(): ...
    def creation_factory(): ...
```

### Resource

An engineering artifact identified by a URL. Every resource has:

- An **RDF type** (e.g. `oslc_rm:Requirement`)
- A set of **properties** defined by the domain vocabulary
- An optional **resource shape** describing the expected property structure

Resources are the domain models in `pyoslc/resources/domains/`:

```python
# GET /oslc/services/rm/requirement/42
class Requirement(BaseResource):
    short_title: str
    elaborated_by: set[Link]
    ...
```

### Resource Shape

An RDF document that describes the valid properties of a resource type — their
names, value types, cardinality (exactly-one, zero-or-many, etc.), and
representations (inline vs. reference).

```
GET /oslc/services/resourceShapes/requirement
  → oslc:ResourceShape with oslc:Property entries
```

Shapes are built by functions in `app/api/adapter/services/shapes.py`:

```python
def build_requirement_shape(base_uri):
    shape = ResourceShape(about=shape_uri, describes=OSLC_RM.Requirement, ...)
    shape.add_shape_property(Property(
        property_definition=DCTERMS.identifier, occurs=OSLC.Exactly-one, ...))
    ...
```

SHACL validation (OSLC v3) converts the shape to `sh:NodeShape` via
`pyoslc/shacl/converter.py`.

### Domain Vocabulary

A set of RDF terms (classes + properties) for a specific engineering domain:

| Domain | Namespace URI | OSLC Spec |
|---|---|---|
| Core | `http://open-services.net/ns/core#` | Part 7 |
| RM (Requirements) | `http://open-services.net/ns/rm#` | OSLC RM v2.1 |
| QM (Quality) | `http://open-services.net/ns/qm#` | OSLC QM v2.1 |
| CM (Change) | `http://open-services.net/ns/cm#` | OSLC CM v3.0 |
| AM (Architecture) | `http://open-services.net/ns/am#` | OSLC AM v2.1 |

Vocabularies are defined as `rdflib.ClosedNamespace` in `pyoslc/vocabularies/`:

```python
# pyoslc/vocabularies/rm.py
OSLC_RM = ClosedNamespace(
    uri=URIRef("http://open-services.net/ns/rm#"),
    terms=["Requirement", "RequirementCollection", "elaboratedBy", ...],
)
```

### OSLC-Core-Version

A request/response header that negotiates between OSLC v2 and v3 behaviour:

```
Request:    OSLC-Core-Version: 3.0
Response:   OSLC-Core-Version: 3.0
```

When absent, the server defaults to `2.0` (backward compatible). v3 adds
features such as Turtle support, LDP Link headers, JSON-LD, structured OSLC
Error responses, SHACL validation, and OPTIONS handlers.

## OSLC Communication Flow

```
┌──────────────┐    1. Discover         ┌──────────────────┐
│              │ ─────────────────────── │  Service         │
│   Client     │   GET /oslc/services/   │  Provider        │
│  (pyoslc-    │   catalog              │  Catalog         │
│   client)    │ ─────────────────────── │                  │
│              │                        └──────────────────┘
│              │                               │
│              │    2. Select Provider         │
│              │    3. GET provider/{id}       │
│              │                        ┌──────────────────┐
│              │ ─────────────────────── │  Service         │
│              │                        │  Provider        │
│              │                        │  (Project-1)     │
│              │                        └──────────────────┘
│              │                               │
│              │    4. Use Service             │
│              │    (query, create, dialog)    │
│              │                        ┌──────────────────┐
│              │ ─────────────────────── │  Resources       │
│              │                        │  (Requirement,   │
│              │                        │   TestCase, ...) │
│              │                        └──────────────────┘
│              │                               │
│              │    5. Follow Links            │
│              │    (elaboratedBy,             │
│              │     specifiedBy, ...)         │
│              │                               │
└──────────────┘                               │
                                               │
    6. Shape Discovery                         │
    GET /oslc/services/                        │
        resourceShapes/requirement             │
┌─────────────────────┐                        │
│  Resource Shape     │◄───────────────────────┘
│  (property defs,    │
│   cardinality,      │
│   value types)      │
└─────────────────────┘
```

## How pyoslc-server Implements Each Layer

| OSLC Concept | pyoslc Implementation | Key File(s) |
|---|---|---|
| Service Provider Catalog | `ServiceProviderCatalogSingleton` | `app/api/adapter/services/providers.py` |
| Service Provider | `ContactServiceProviderFactory` | `app/api/adapter/services/factories.py` |
| Service (capabilities) | `Specification` / `TestCase` (subclasses of `ServiceResource`) | `app/api/adapter/services/specification.py` |
| Domain vocabulary | `ClosedNamespace` in `pyoslc/vocabularies/` | `pyoslc/vocabularies/rm.py` |
| Resource model | `BaseResource` subclass with `to_rdf()` / `from_rdf()` | `pyoslc/resources/domains/rm.py` |
| Resource shape | `ResourceShape` + `Property` objects | `app/api/adapter/services/shapes.py` |
| REST endpoints | Flask-RESTx `Resource` classes | `app/api/adapter/namespaces/core.py`, `rm/routes.py` |
| Storage backend | `RequirementRepository` ABC + implementations | `app/api/adapter/resources/repository.py` |
| OSLC Error response | `OslcResource.build_error_response()` | `pyoslc/rest/resource.py` |
| SHACL validation | `oslc_shape_to_shacl()` + `validate_resource()` | `pyoslc/shacl/converter.py` |
| Version negotiation | `OslcResource.get_requested_version()` | `pyoslc/rest/resource.py` |

## How pyoslc-client Consumes the Architecture

[pyoslc-client](https://github.com/cslab/pyoslc-client) is a standalone CLI
tool (no dependency on pyoslc-server) that walks the same OSLC discovery flow:

| CLI Command | OSLC Concept | What It Does |
|---|---|---|
| `pyoslc discover <rootservices>` | Root Services → Catalog | Fetches the root services document, extracts the catalog URL |
| `pyoslc catalog <url>` | Service Provider Catalog | Lists all service providers in the catalog |
| `pyoslc providers <url>` | Service Providers | Lists each provider with its offered services |
| `pyoslc query <url>` | Query Capability | Executes `oslc.where` / `oslc.select` queries against a service |
| `pyoslc get <url>` | Resource (Read) | Fetches and displays a single resource by URL |
| `pyoslc create <url> <file>` | Creation Factory | POSTs an RDF file to a creation factory URL |
| `pyoslc shape <url>` | Resource Shape | Fetches and displays the resource shape for a resource type |
| `pyoslc validate <url>` | SHACL Validation | Downloads the resource shape, converts to SHACL, and validates |

Typical client flow:

```bash
# 1. Discover the server's catalog via root services
pyoslc discover http://pyoslc.example.com/.well-known/oslc/sp-catalog

# 2. List providers and find the RM provider
pyoslc catalog http://pyoslc.example.com/oslc/services/catalog

# 3. Query requirements
pyoslc query 'http://pyoslc.example.com/oslc/services/provider/Project-1/resources/requirement'

# 4. Create a requirement (from a Turtle file)
pyoslc create 'http://pyoslc.example.com/oslc/services/provider/Project-1/resources/requirement' \
    new_req.ttl
```

## RDF Serialisation

OSLC supports multiple RDF formats. pyoslc negotiates them via the `Accept`
header:

| Format | Header Value | pyoslc internal name |
|---|---|---|
| RDF/XML | `application/rdf+xml` | `xml` |
| Turtle (v3) | `text/turtle` | `turtle` |
| JSON-LD (v3) | `application/ld+json` | `json-ld` |
| JSON | `application/json` | `json-ld` (aliased) |

The server serialises an `rdflib.Graph` into the requested format. The client
parses the response back into an `rdflib.Graph` for display or further
processing.

## OSLC v3 Additions

Compared to OSLC v2, v3 adds (all implemented in pyoslc):

| Feature | v2 | v3 |
|---|---|---|
| RDF format | RDF/XML only | RDF/XML + Turtle + JSON-LD |
| Discovery headers | — | LDP `Link: rel="type"` on resources |
| Resource shape | `oslc:ResourceShape` | Same + SHACL conversion |
| Error responses | Custom HTML/XML | Structured `oslc:Error` |
| OPTIONS | — | `Allow` + `Accept-Post` headers |
| Version negotiation | — | `OSLC-Core-Version` header (default 2.0) |

## Further Reading

- [OSLC Core v3.0 Specification](https://docs.oasis-open-projects.org/oslc-op/core/v3.0/oslc-core.html)
- [OSLC RM v2.1 Specification](https://open-services.net/bin/view/Main/RmSpecificationV2)
- [pyoslc OSLC v2/v3 Compatibility](OSLC_V2_V3_COMPATIBILITY.md)
- [pyoslc Domain Development Guide](DOMAIN_DEVELOPMENT.md)
- [pyoslc-client CLI](https://github.com/cslab/pyoslc-client)
