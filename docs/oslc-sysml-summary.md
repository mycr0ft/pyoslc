# OSLC SysML v2 Domain — Extension Plan for pyoslc

## 1. Specification Summary

**Source:** [OSLC SysML v2.0 Part 1: Specification](https://oslc-op.github.io/oslc-specs/specs/sysml/sysml-spec.html)
**Vocabulary:** [Part 2: Vocabulary](https://oslc-op.github.io/oslc-specs/specs/sysml/sysml-vocab.html) + [SysML-vocab.ttl](https://oslc-op.github.io/oslc-specs/specs/sysml/SysML-vocab.ttl)
**Constraints:** [Part 3: Constraints](https://oslc-op.github.io/oslc-specs/specs/sysml/sysml-shapes.html) + [SysML-shapes.ttl](https://oslc-op.github.io/oslc-specs/specs/sysml/SysML-shapes.ttl)

### 1.1 Purpose

Defines RESTful interfaces for **SysML v2** model-based systems engineering (MBSE) artifacts, enabling integration with other OSLC domains (Requirements, Change Management, Quality Management, Architecture Management).

### 1.2 Namespace Discrepancy (IMPORTANT)

| Context | Namespace URI | Prefix |
|---------|--------------|--------|
| Spec Part 1 (prose) | `http://open-services.net/ns/sysmlv2#` | `oslc_sysmlv2` |
| Actual Turtle vocabulary | `https://www.omg.org/spec/sysml/vocabulary#` | `oslc_sysml` |
| Shapes/constraints | `https://www.omg.org/spec/SysML/20250201/shapes/` | `oslc_sysml_shapes` |

**Decision needed:** Which namespace to use in pyoslc. The vocabulary Turtle file (authoritative machine-readable source) uses `https://www.omg.org/spec/sysml/vocabulary#`. The spec prose uses `http://open-services.net/ns/sysmlv2#`. The shapes file also uses the OMG URI. **Recommendation: use the OMG vocabulary URI** since that's what the machine-readable artifacts reference.

### 1.3 Key Design Principles

1. **SysML Elements are AM Resources:** `oslc_sysml:Element` subclasses `oslc_am:Resource`. All SysML elements inherit from the Architecture Management resource type.
2. **Two mandatory access types:** Servers MUST allow direct URL access to at least `Element` and `Relationship`.
3. **Ordered multi-valued properties via reification:** All SysML v2 relationships MUST be reified with `oslc_sysmlv2:order` to preserve ordering. Uses `rdf:Statement` reification pattern.
4. **Domain declared as AM:** ServiceProviders declare `oslc:domain` = `http://open-services.net/ns/am#`.
5. **Vocabulary subsets allowed:** Servers MAY limit which SysML types are directly accessible.

### 1.4 Server Compliance Matrix

| Requirement | Level |
|-------------|-------|
| OSLC Core 3 compliance | MUST |
| RDF/XML representations | MUST |
| XML representations | MUST |
| JSON representations | MAY |
| ServiceProvider resource | MUST |
| ServiceProviderCatalog resource | MUST |
| `oslc:serviceProvider` on resources | MUST |
| Query capabilities on `oslc_am:Resource` | MUST |
| `oslc.where` + `oslc.searchTerms` | MUST |
| `If-Match` concurrency (if update/delete supported) | MUST |
| Resource update (PUT) / delete (DELETE) | SHOULD |
| Query on `oslc_am:LinkType` | SHOULD |
| Selection dialogs | SHOULD |
| Resource preview | SHOULD |
| Resource shapes | SHOULD |
| Pagination | SHOULD |
| Creation factories | MAY |
| Creation dialogs | MAY |
| Partial GET/PUT (`oslc.properties`) | MAY |
| LDP Patch | MAY |

---

## 2. Vocabulary Summary

### 2.1 Class Hierarchy (182 classes)

The SysML v2 metamodel has a deep inheritance tree. Key root classes and their subtrees:

```
oslc_am:Resource
└── Element                          # Root of all SysML elements
    ├── Namespace                    # Container for Elements
    │   ├── Type                     # Classifier base
    │   │   ├── Classifier
    │   │   │   ├── Class
    │   │   │   │   ├── Structure
    │   │   │   │   │   ├── Metaclass
    │   │   │   │   │   ├── Association
    │   │   │   │   │   │   └── AssociationStructure
    │   │   │   │   │   │       └── ConnectionDefinition
    │   │   │   │   │   │           ├── AllocationDefinition
    │   │   │   │   │   │           ├── InterfaceDefinition
    │   │   │   │   │   │           └── FlowDefinition
    │   │   │   │   │   └── ItemDefinition
    │   │   │   │   │       ├── PartDefinition
    │   │   │   │   │       │   ├── RenderingDefinition
    │   │   │   │   │       │   └── ViewDefinition
    │   │   │   │   │       ├── MetadataDefinition
    │   │   │   │   │       └── PortDefinition
    │   │   │   │   ├── Behavior
    │   │   │   │   │   ├── Function → Predicate
    │   │   │   │   │   ├── ActionDefinition
    │   │   │   │   │   │   ├── CalculationDefinition → CaseDefinition
    │   │   │   │   │   │   │   ├── UseCaseDefinition
    │   │   │   │   │   │   │   ├── AnalysisCaseDefinition
    │   │   │   │   │   │   │   └── VerificationCaseDefinition
    │   │   │   │   │   │   ├── StateDefinition
    │   │   │   │   │   │   └── FlowDefinition
    │   │   │   │   │   └── Interaction
    │   │   │   │   └── OccurrenceDefinition (+ Class)
    │   │   │   │       ├── ConstraintDefinition → RequirementDefinition
    │   │   │   │       │   ├── ConcernDefinition
    │   │   │   │       │   └── ViewpointDefinition
    │   │   │   │       ├── ItemDefinition (+ Structure)
    │   │   │   │       └── PortDefinition (+ Structure)
    │   │   │   ├── DataType → AttributeDefinition → EnumerationDefinition
    │   │   │   └── Definition (abstract parent of all *Definition classes)
    │   │   └── Feature → Step, Usage, Connector, Multiplicity, etc.
    │   └── Package → LibraryPackage
    ├── Relationship                 # Root of all SysML relationships
    │   ├── Membership → OwningMembership, FeatureMembership, etc.
    │   ├── Specialization → Subsetting, Subclassification, FeatureTyping
    │   ├── Import → MembershipImport, NamespaceImport, Expose
    │   ├── Dependency
    │   ├── Annotation
    │   ├── Conjugation
    │   └── ... (many more)
    └── AnnotatingElement → Comment → Documentation, TextualRepresentation
```

### 2.2 Key Properties by Category

**Element-level (inherited by all):**
- `elementId` (Exactly-one, string) — unique SysML element identifier
- `aliasIds` (Zero-or-many, string)
- `declaredName`, `declaredShortName`, `name`, `shortName`, `qualifiedName` (strings)
- `isImpliedIncluded`, `isLibraryElement` (Exactly-one, boolean)
- `ownedElement`, `ownedRelationship`, `ownedAnnotation` (Zero-or-many, resource links)
- `owner`, `owningNamespace`, `owningMembership`, `owningRelationship` (resource links)
- `documentation`, `textualRepresentation` (Zero-or-many)

**Relationship-level:**
- `source` (Zero-or-many, range: Element) — **ordered via reification**
- `target` (Zero-or-many, range: Element) — **ordered via reification**
- `relatedElement`, `ownedRelatedElement`, `owningRelatedElement`
- `isImplied` (Exactly-one, boolean)

**Type/Classifier-level:**
- `isAbstract`, `isConjugated`, `isSufficient` (Exactly-one, boolean)
- `feature`, `directedFeature`, `endFeature`, `ownedFeature`, `inheritedFeature`
- `input`, `output`
- `multiplicity`
- `ownedSpecialization`, `ownedConjugator`, `ownedDifferencing`, `ownedDisjoining`, etc.

**Feature-level:**
- `direction` (Zero-or-one, enum: in/out/inout)
- `isComposite`, `isConstant`, `isDerived`, `isEnd`, `isOrdered`, `isPortion`, `isReference`, `isUnique`, `isVariable` (Exactly-one, boolean)
- `featureTarget`, `endOwningType`, `crossFeature`
- `ownedTyping`, `ownedSubsetting`, `ownedRedefinition`, `ownedFeatureChaining`, etc.

**Usage-level:**
- `definition`, `owningDefinition`, `owningUsage`
- `nested*` properties (30+ types: nestedAction, nestedPart, nestedPort, nestedRequirement, etc.)
- `portionKind` (Zero-or-one, enum: snapshot/timeslice)
- `mayTimeVary` (Exactly-one, boolean)

**Definition-level (owned):**
- `owned*` properties (30+ types: ownedAction, ownedPart, ownedPort, ownedRequirement, etc.)

**OSLC/Dublin Core metadata (on all elements):**
- `dcterms:identifier` (Exactly-one, readOnly)
- `dcterms:title` (Exactly-one)
- `dcterms:description` (Zero-or-one)
- `dcterms:created`, `dcterms:modified` (Zero-or-one)
- `dcterms:creator`, `dcterms:contributor` (Zero-or-many)
- `oslc:serviceProvider` (Zero-or-many, readOnly: false)
- `oslc:shortTitle`, `oslc:instanceShape`
- OSLC linking: `derives`, `elaborates`, `external`, `refine`, `satisfy`, `trace`

### 2.3 Enumerations (19 individuals)

| Enum Type | Values |
|-----------|--------|
| FeatureDirectionKind | `in`, `out`, `inout` |
| VisibilityKind | `public`, `protected`, `private` |
| TriggerKind | `after`, `at`, `when` |
| RequirementConstraintKind | `assumption`, `requirement` |
| StateSubactionKind | `entry`, `do`, `exit` |
| TransitionFeatureKind | `trigger`, `guard`, `effect` |
| PortionKind | `snapshot`, `timeslice` |

---

## 3. RDF Reification for Ordered Properties

The spec mandates triple reification for ordering multi-valued properties:

```turtle
:r a oslc_sysml:Relationship .
:e a oslc_sysml:Element .
:f a oslc_sysml:Element .

# Actual triples
:r oslc_sysml:source :e .
:r oslc_sysml:source :f .

# Reified statements with order
:s_1 a rdf:Statement ;
  rdf:subject :r ;
  rdf:predicate oslc_sysml:source ;
  rdf:object :e ;
  oslc_sysmlv2:order 1 .

:s_2 a rdf:Statement ;
  rdf:subject :r ;
  rdf:predicate oslc_sysml:source ;
  rdf:object :f ;
  oslc_sysmlv2:order 2 .
```

**Implementation note:** The `to_rdf()` method in the SysML resource model must emit reification triples for all ordered properties. The `from_rdf()` method must reconstruct ordering from reified statements.

---

## 4. Implementation Plan for pyoslc

### 4.1 Layer 1: Vocabulary (`pyoslc/vocabularies/sysml.py`)

Create a `ClosedNamespace` for the SysML vocabulary. Given the large number of terms (182 classes + 341 properties + 19 individuals = 542 terms), this will be a large namespace definition.

Also need to extend `pyoslc/vocabularies/am.py` with the `Resource` class term (currently only has `LinkType` and `amServiceProviders`).

```python
OSLC_SYSML = ClosedNamespace(
    uri=URIRef("https://www.omg.org/spec/sysml/vocabulary#"),
    terms=[
        # 182 classes
        "Element", "Relationship", "Namespace", "Type", "Feature",
        "Classifier", "Class", "Structure", "Definition", "Usage",
        # ... all 182 classes ...
        
        # 341 properties
        "elementId", "aliasIds", "declaredName", "source", "target",
        # ... all 341 properties ...
        
        # 19 individuals
        "in", "out", "inout", "public", "private", "protected",
        # ... all 19 individuals ...
    ]
)
```

### 4.2 Layer 2: Domain Resource Models (`pyoslc/resources/domains/sysml.py`)

Given the massive class hierarchy, recommend a **layered approach** starting with the base classes and adding specialized types incrementally:

**Phase 1 — Core (required by spec):**
- `SysMLElement(BaseResource)` — maps to `oslc_sysml:Element`, subclasses `oslc_am:Resource`
- `SysMLRelationship(SysMLElement)` — maps to `oslc_sysml:Relationship`, with ordered `source`/`target`

**Phase 2 — Common structural types:**
- `SysMLNamespace(SysMLElement)` — for Package, Namespace
- `SysMLType(SysMLElement)` — for Type, Classifier, Class
- `SysMLFeature(SysMLElement)` — for Feature
- `SysMLDefinition(SysMLType)` — for Definition and subclasses
- `SysMLUsage(SysMLFeature)` — for Usage and subclasses

**Phase 3 — Domain-specific types (as needed):**
- `PartDefinition`, `PartUsage`, `PortDefinition`, `PortUsage`
- `RequirementDefinition`, `RequirementUsage`
- `ActionDefinition`, `ActionUsage`
- `ItemDefinition`, `ItemUsage`
- etc.

Each class needs:
- `__init__()` with domain-specific attributes
- `to_rdf(graph, base_url, attributes)` with reification support for ordered properties
- `from_rdf(g, attributes)` with order reconstruction
- `from_json(data, attributes)`
- `update(data, attributes)`

### 4.3 Layer 3: Resource Shapes (`app/api/adapter/services/shapes.py`)

Add shape builder functions:
- `build_sysml_element_shape(base_uri)` — 36 properties
- `build_sysml_relationship_shape(base_uri)` — 42 properties (Element + Relationship-specific)

For Phase 2+, add shapes for each new type.

### 4.4 Layer 4: Specification (`app/api/adapter/services/sysml_specification.py`)

```python
class SysMLSpecification(ServiceResource):
    domain = 'http://open-services.net/ns/am#'
    service_path = 'provider/{id}/sysml'
    
    @staticmethod
    def query_capability(): ...
    
    @staticmethod
    def creation_factory(): ...
    
    @staticmethod
    def selection_dialog(): ...
```

### 4.5 Layer 5: Routes (`app/api/adapter/namespaces/sysml/`)

- `__init__.py` — Flask-RESTX namespace registration
- `routes.py` — `SysMLElementList`, `SysMLElementItem`, `SysMLRelationshipList`, `SysMLRelationshipItem`
- `models.py` — Flask-RESTX API models
- `parsers.py` — Request parsers

### 4.6 Layer 6: Repository (`app/api/adapter/namespaces/sysml/`)

- `sysml_repository.py` — `SysMLElementRepository` ABC + CSV/Oxigraph implementations

### 4.7 Layer 7: Attribute Mappings (`app/api/adapter/mappings/sysml.py`)

Map external field names to Python attributes and OSLC properties for SysML elements.

### 4.8 Registration

1. Register `SysMLSpecification` via `config_service_resource()` in `core.py`
2. Add `sysml_ns` to `api.add_namespace()` in `oslc.py`
3. Add SysML service provider to `CSVImplementation.get_service_provider_info()` in `manager.py`
4. Bind `OSLC_SYSML` namespace in `oslc.py` `init_app()`

---

## 5. Key Implementation Challenges

### 5.1 RDF Reification for Ordering
The existing `BaseResource.to_rdf()` doesn't support reification. Need to:
- Add a utility function for emitting `rdf:Statement` reification triples
- Add a utility function for reconstructing ordered lists from reified statements in `from_rdf()`
- Consider a mixin class `OrderedPropertyMixin`

### 5.2 AM Vocabulary Extension
The existing `pyoslc/vocabularies/am.py` is minimal (only `LinkType` and `amServiceProviders`). Need to add `Resource` as a term since SysML Elements subclass it.

### 5.3 Large Vocabulary Size
542 terms is much larger than existing domains (RM has ~30 terms). Consider:
- Code generation from the Turtle vocabulary file
- Lazy loading of terms
- Splitting into sub-namespaces (e.g., `sysml_core`, `sysml_types`, `sysml_properties`)

### 5.4 Deep Inheritance
The 7+ level inheritance chains (Element → Namespace → Type → Classifier → Class → Structure → ItemDefinition → PartDefinition) need careful Python MRO management. Consider using mixins for shared property sets rather than deep inheritance.

### 5.5 Namespace URI Decision
Need to resolve the `http://open-services.net/ns/sysmlv2#` vs `https://www.omg.org/spec/sysml/vocabulary#` discrepancy. The machine-readable artifacts use the OMG URI.

---

## 6. Completed Implementation

All 8 phases are implemented across 67 resource model classes, 130 REST API routes, and ~540 vocabulary terms.

| Phase | Scope | Classes | Status |
|-------|-------|---------|--------|
| **1. Foundation** | Element, Relationship | 2 | ✅ |
| **2. Structural** | Namespace, Type, Package, Definition, Usage | 5 | ✅ |
| **3. Parts & Ports** | ItemDefinition, ItemUsage, PartDefinition, PartUsage, PortDefinition, PortUsage | 6 | ✅ |
| **4. Requirements** | RequirementDefinition, RequirementUsage, ConcernDefinition, ConcernUsage | 4 | ✅ |
| **5. Behavior** | ActionDefinition, ActionUsage, StateDefinition, StateUsage | 4 | ✅ |
| **6. Constraints** | ConstraintDefinition, ConstraintUsage | 2 | ✅ |
| **7. Views** | ViewDefinition, ViewUsage, ViewpointDefinition, ViewpointUsage | 4 | ✅ |
| **8. Full** | Feature, Classifier, OccurrenceDefinition, OccurrenceUsage, Class, Structure, DataType, Behavior, Function, Predicate, LibraryPackage, AttributeDefinition, AttributeUsage, EnumerationDefinition, EnumerationUsage, CalculationDefinition, CalculationUsage, CaseDefinition, CaseUsage, UseCaseDefinition, UseCaseUsage, AnalysisCaseDefinition, AnalysisCaseUsage, VerificationCaseDefinition, VerificationCaseUsage, ConnectionDefinition, ConnectionUsage, FlowDefinition, FlowUsage, InterfaceDefinition, InterfaceUsage, AllocationDefinition, AllocationUsage, RenderingDefinition, RenderingUsage, ReferenceUsage, ConjugatedPortDefinition, ConnectorAsUsage, SuccessionAsUsage, BindingConnectorAsUsage | 40 | ✅ |

**Total: 67 resource model classes** with full shapes, REST routes, models, parsers, and business logic.

Membership subtypes (19 classes), Relationship subtypes (17 classes), Annotation types (6 classes), Expression types (12 classes), Behavioral subtypes (20 classes), Metadata types (6 classes), and other fine-grained metamodel classes exist as resource model classes but are not yet exposed via OSLC REST routes.

---

## 7. Integration with Sibling Projects

Two companion projects in the same workspace will eventually connect to pyoslc's SysML OSLC domain:

### 7.1 sysmlpy (`~/sysmlpy`)

A pure Python library (v0.34.1) for constructing, parsing, and visualizing SysML v2.0 models.

- **ANTLR4-based parser** with 100% OMG XPect conformance (123/123 tests)
- **Programmatic model construction** API (`Part`, `Item`, `Attribute`, `Action`, `Requirement`, etc.)
- **Semantic analysis** engine (undefined symbol detection, import resolution, OCL checks)
- **17 PlantUML visualization views** for model rendering
- **Multiple graph backends**: InMemory, NetworkX, Kuzu, Cayley
- Published on PyPI as `sysmlpy`

**Integration opportunities:**
- Use `sysmlpy.loads()` / `sysmlpy.analyze()` as a **parsing and validation backend** for OSLC POST operations
- Convert sysmlpy model objects → OSLC RDF triples via `SysMLElement.to_rdf()`
- PlantUML views → OSLC **resource preview** (UI Preview) rendering
- sysmlpy's `Store` protocol (NetworkX, Kuzu, Cayley) as a **shared data backend**

### 7.2 sysmlpy-api-services (`~/sysmlpy-api-services`)

A Flask REST API implementing the **OMG SysML v2 API Services** specification (JSON-based, not OSLC).

- **OMG API endpoints**: Projects, Commits, Branches, Tags, Elements, Relationships, Query, Schema
- **100 SysML v2 `@type` values** matching the OMG element taxonomy
- **NetworkX DiGraph** storage backend (`GraphStore`)
- Swagger/OpenAPI documentation at `/docs/`

**Integration opportunities:**
- **OMG-API-to-OSLC gateway**: translate between OMG JSON format (`@type`, `identifier`, `qualifiedName`) and OSLC RDF (`oslc_sysml:Element`, `elementId`, `qualifiedName`)
- **Shared element taxonomy**: the 100 OMG API types are a subset of pyoslc's 182 OSLC vocabulary classes
- **Shared NetworkX store**: `GraphStore` could serve as a backend for both the OMG API and OSLC endpoints
- **Cayley backend bridge**: sysmlpy's Cayley store (RDF quad store via HTTP) is closer to OSLC's RDF format

### 7.3 Architecture Vision

```
sysmlpy (parser/builder/validator)
    │
    ├──→ sysmlpy-api-services (OMG REST API, JSON)
    │         │
    │         └──→ GraphStore (NetworkX / Kuzu / Cayley)
    │                    │
    └──→ pyoslc (OSLC REST API, RDF)
              │
              └──→ SysML OSLC Repository ──→ shared store
```

The three projects share the same SysML v2 metamodel but expose it through different APIs:
- **sysmlpy**: Python library (no API)
- **sysmlpy-api-services**: OMG SysML v2 REST API (JSON)
- **pyoslc**: OSLC SysML v2 API (RDF/Linked Data)
