# -*- coding: utf-8 -*-
"""STEP product-structure resources for the OSLC adapter.

A STEP AP242 product is emphatically NOT a SysML element — it is an
engineered product item carried by its own standard.  These resources
sit at the ``oslc:Resource`` level (OSLC Core), typed by the STEP
domain vocabulary, with cross-links back into the SysML world via
``oslc:link`` (P3's Vee join).

The vocabulary lives at ``https://github.com/mycr0ft/stepper/vocab#``
(same terms stepper's ``stepper structure`` emitter uses, so resources
loaded from P1 output round-trip cleanly).
"""

from rdflib import RDF, URIRef, Literal
from rdflib.namespace import DCTERMS
from rdflib.extras.describer import Describer

from pyoslc.resources.models import BaseResource
from pyoslc.vocabularies.core import OSLC

OSLC_CORE = "http://open-services.net/ns/core#"

STEP_VOCAB = "https://github.com/mycr0ft/stepper/vocab#"


class StepResource(BaseResource):
    """Base for all STEP-domain resources: about/identifier/title/
    description + the STEP source reference (#instance-id in file)."""

    def __init__(self, about=None, types=None, description=None,
                 identifier=None, title=None, source_ref=None,
                 file_ref=None, service_provider=None, relation=None):
        super().__init__(about, types, None, description, identifier,
                         None, title, None, None, None, None, None,
                         None, None, None, service_provider, relation)
        self.__source_ref = source_ref if source_ref is not None else ""
        self.__file_ref = file_ref if file_ref is not None else ""

    @property
    def source_ref(self):
        return self.__source_ref

    @source_ref.setter
    def source_ref(self, value):
        self.__source_ref = value or ""

    @property
    def file_ref(self):
        return self.__file_ref

    @file_ref.setter
    def file_ref(self, value):
        self.__file_ref = value or ""

    def _step_base_rdf(self, d, graph, base_url):
        if self.identifier:
            d.value(DCTERMS.identifier, Literal(self.identifier))
        if self.title:
            d.value(DCTERMS.title, Literal(self.title))
        if self.description:
            d.value(DCTERMS.description, Literal(self.description))
        if self.source_ref:
            d.value(URIRef(STEP_VOCAB + "sourceRef"),
                    Literal(self.source_ref))
        if self.file_ref:
            d.value(URIRef(STEP_VOCAB + "file"),
                    Literal(self.file_ref))

    def _step_url(self, base_url, identifier):
        """Resolve resource URL; tolerate a None identifier."""
        if identifier and identifier not in (base_url or "").split("/"):
            return (base_url or "").rstrip("/") + "/" + identifier
        return base_url


class StepProduct(StepResource):
    """A PRODUCT from a P21 exchange file."""

    rdf_type = URIRef(STEP_VOCAB + "Product")

    def __init__(self, about=None, identifier=None, title=None,
                 description=None, source_ref=None, file_ref=None,
                 product_id=None, service_provider=None, relation=None):
        super().__init__(about=about, identifier=identifier, title=title,
                         description=description, source_ref=source_ref,
                         file_ref=file_ref, service_provider=service_provider,
                         relation=relation)
        self.__product_id = product_id if product_id is not None else ""

    @property
    def product_id(self):
        return self.__product_id

    @product_id.setter
    def product_id(self, value):
        self.__product_id = value or ""

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind("step", URIRef(STEP_VOCAB))
        identifier = self.identifier
        base_url = self._step_url(base_url, identifier)
        d = Describer(graph, base=base_url)
        d.about(base_url)
        d.rdftype(self.rdf_type)
        d.rdftype(URIRef(OSLC_CORE + 'Resource'))
        self._step_base_rdf(d, graph, base_url)
        if self.__product_id:
            d.value(URIRef(STEP_VOCAB + "productId"),
                    Literal(self.__product_id))
        return graph

    def from_rdf(self, g):
        for r in g.subjects(RDF.type, self.rdf_type):
            self.about = str(r)
            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = str(o)
            for o in g.objects(r, URIRef(STEP_VOCAB + "sourceRef")):
                self.source_ref = str(o)


class StepProductDefinition(StepResource):
    """A PRODUCT_DEFINITION: the usage of a product in a context —
    OSLC-visible counterpart of the structure backbone node.

    Links (all optional, set as URIRef lists):
    - product: the StepProduct this defines
    - shape_representations: geometry carriers for this definition
    - sysml_links: oslc:link edges into the SysML domain (P3)
    """

    rdf_type = URIRef(STEP_VOCAB + "ProductDefinition")

    def __init__(self, about=None, identifier=None, title=None,
                 description=None, source_ref=None, file_ref=None,
                 product=None, shape_representations=None,
                 sysml_links=None, service_provider=None, relation=None):
        super().__init__(about=about, identifier=identifier, title=title,
                         description=description, source_ref=source_ref,
                         file_ref=file_ref, service_provider=service_provider,
                         relation=relation)
        self.__product = product if product is not None else []
        self.__shape_representations = (shape_representations
                                        if shape_representations is not None
                                        else [])
        self.__sysml_links = sysml_links if sysml_links is not None else []

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, value):
        self.__product = value or []

    def add_product(self, uri):
        self.__product.append(uri)

    @property
    def shape_representations(self):
        return self.__shape_representations

    @shape_representations.setter
    def shape_representations(self, value):
        self.__shape_representations = value or []

    def add_shape_representation(self, uri):
        self.__shape_representations.append(uri)

    @property
    def sysml_links(self):
        return self.__sysml_links

    @sysml_links.setter
    def sysml_links(self, value):
        self.__sysml_links = value or []

    def add_sysml_link(self, uri):
        self.__sysml_links.append(uri)

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind("step", URIRef(STEP_VOCAB))
        identifier = self.identifier
        base_url = self._step_url(base_url, identifier)
        d = Describer(graph, base=base_url)
        d.about(base_url)
        d.rdftype(self.rdf_type)
        d.rdftype(URIRef(OSLC_CORE + 'Resource'))
        self._step_base_rdf(d, graph, base_url)
        for p in self.__product:
            d.value(URIRef(STEP_VOCAB + "product"), URIRef(p))
        for s in self.__shape_representations:
            d.value(URIRef(STEP_VOCAB + "shapeRepresentation"), URIRef(s))
        for sl in self.__sysml_links:
            d.value(OSLC.link, URIRef(sl))
        return graph

    def from_rdf(self, g):
        for r in g.subjects(RDF.type, self.rdf_type):
            self.about = str(r)
            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = str(o)
            for o in g.objects(r, URIRef(STEP_VOCAB + "product")):
                self.add_product(str(o))
            for o in g.objects(r, URIRef(STEP_VOCAB + "shapeRepresentation")):
                self.add_shape_representation(str(o))
            for o in g.objects(r, OSLC.link):
                self.add_sysml_link(str(o))


class StepShapeRepresentation(StepResource):
    """A SHAPE_*_REPRESENTATION: the geometry carrier of a product
    definition. geometry_item_count is the representation's item
    population (not the shape graph — that's P3/visualization work)."""

    rdf_type = URIRef(STEP_VOCAB + "ShapeRepresentation")

    def __init__(self, about=None, identifier=None, title=None,
                 description=None, source_ref=None, file_ref=None,
                 representation_kind=None, geometry_item_count=0,
                 service_provider=None, relation=None):
        super().__init__(about=about, identifier=identifier, title=title,
                         description=description, source_ref=source_ref,
                         file_ref=file_ref, service_provider=service_provider,
                         relation=relation)
        self.__representation_kind = (representation_kind
                                      if representation_kind is not None
                                      else "")
        self.__geometry_item_count = (geometry_item_count
                                      if geometry_item_count is not None
                                      else 0)

    @property
    def representation_kind(self):
        return self.__representation_kind

    @representation_kind.setter
    def representation_kind(self, value):
        self.__representation_kind = value or ""

    @property
    def geometry_item_count(self):
        return self.__geometry_item_count

    @geometry_item_count.setter
    def geometry_item_count(self, value):
        self.__geometry_item_count = int(value or 0)

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind("step", URIRef(STEP_VOCAB))
        identifier = self.identifier
        base_url = self._step_url(base_url, identifier)
        d = Describer(graph, base=base_url)
        d.about(base_url)
        d.rdftype(self.rdf_type)
        d.rdftype(URIRef(OSLC_CORE + 'Resource'))
        self._step_base_rdf(d, graph, base_url)
        if self.__representation_kind:
            d.value(URIRef(STEP_VOCAB + "representationKind"),
                    Literal(self.__representation_kind))
        d.value(URIRef(STEP_VOCAB + "geometryItemCount"),
                Literal(self.__geometry_item_count))
        return graph

    def from_rdf(self, g):
        for r in g.subjects(RDF.type, self.rdf_type):
            self.about = str(r)
            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = str(o)
            for o in g.objects(r, URIRef(STEP_VOCAB + "representationKind")):
                self.representation_kind = str(o)
            for o in g.objects(r, URIRef(STEP_VOCAB + "geometryItemCount")):
                self.geometry_item_count = int(o)


class StepFile(StepResource):
    """The P21 exchange file itself — provenance anchor: schema name,
    product count, and the check-gate verdict when stepper has run."""

    rdf_type = URIRef(STEP_VOCAB + "StepFile")

    def __init__(self, about=None, identifier=None, title=None,
                 description=None, schema_name=None, product_count=0,
                 check_verdict=None, file_ref=None,
                 service_provider=None, relation=None):
        super().__init__(about=about, identifier=identifier, title=title,
                         description=description, file_ref=file_ref,
                         service_provider=service_provider, relation=relation)
        self.__schema_name = schema_name if schema_name is not None else ""
        self.__product_count = product_count if product_count is not None else 0
        self.__check_verdict = (check_verdict
                                if check_verdict is not None else "")

    @property
    def schema_name(self):
        return self.__schema_name

    @schema_name.setter
    def schema_name(self, value):
        self.__schema_name = value or ""

    @property
    def product_count(self):
        return self.__product_count

    @product_count.setter
    def product_count(self, value):
        self.__product_count = int(value or 0)

    @property
    def check_verdict(self):
        return self.__check_verdict

    @check_verdict.setter
    def check_verdict(self, value):
        self.__check_verdict = value or ""

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind("step", URIRef(STEP_VOCAB))
        identifier = self.identifier
        base_url = self._step_url(base_url, identifier)
        d = Describer(graph, base=base_url)
        d.about(base_url)
        d.rdftype(self.rdf_type)
        d.rdftype(URIRef(OSLC_CORE + 'Resource'))
        self._step_base_rdf(d, graph, base_url)
        if self.__schema_name:
            d.value(URIRef(STEP_VOCAB + "schemaName"),
                    Literal(self.__schema_name))
        d.value(URIRef(STEP_VOCAB + "productCount"),
                Literal(self.__product_count))
        if self.__check_verdict:
            d.value(URIRef(STEP_VOCAB + "checkVerdict"),
                    Literal(self.__check_verdict))
        return graph

    def from_rdf(self, g):
        for r in g.subjects(RDF.type, self.rdf_type):
            self.about = str(r)
            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = str(o)
            for o in g.objects(r, URIRef(STEP_VOCAB + "schemaName")):
                self.schema_name = str(o)
            for o in g.objects(r, URIRef(STEP_VOCAB + "productCount")):
                self.product_count = int(o)
            for o in g.objects(r, URIRef(STEP_VOCAB + "checkVerdict")):
                self.check_verdict = str(o)