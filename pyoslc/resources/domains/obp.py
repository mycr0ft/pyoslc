# -*- coding: utf-8 -*-
"""OBP domain (Phase C item 3): ISO/TS 10303-3001 Business Object Model
resources + the ISO/TS 10303-400 UUID identity vocabulary.

Where the P2 `step` domain serves the MIM-level structure
(StepProduct/… — the Part 21 entity names), the OBP domain serves
the *business-object* view of the same data: the CamelCase classes
ISO's AP242 BOM (`managed_model_based_3d_engineering_bom`) defines —
`Part`, `PartVersion`, `IndividualPartView`, `External*GeometricModel`,
`NextAssemblyViewUsage` — which are exactly the classes ISO/TS 10303-400
(SysML mapping) addresses. Feeding this domain means a SysML-side
client sees STEP data in the vocabulary the standards mapping uses.

Identity: OBP nodes carry the v12 `uuid_attribute_schema` vocabulary.
`Hash_based_v5_uuid_attribute` = content-addressed identity (uuid +
hash_function + identified_item) — a STEP-side stable id. Vee links
may optionally be expressed in the standard's own form
(`Uuid_relationship`: uuid_1 + uuid_2 + role) instead of (or in
addition to) the P3 qn/ref form.

Data source: stepper's `stepper.bom.to_obp()` (P21 → OBP mapping,
verified against the real -3001 BOM). OBP resources here are OSLC
Core Resources typed by the OBP vocabulary; ids are
`obp:<Class>#<step-ref>` — provenance-carrying by construction.
"""

from rdflib import RDF, URIRef, Literal
from rdflib.namespace import DCTERMS
from rdflib.extras.describer import Describer

from pyoslc.resources.models import BaseResource
from pyoslc.vocabularies.core import OSLC

OSLC_CORE = "http://open-services.net/ns/core#"

OBP_VOCAB = "https://github.com/mycr0ft/stepper/vocab/obp#"
UUID_VOCAB = "https://github.com/mycr0ft/stepper/vocab/uuid#"


class OBPResource(BaseResource):
    """Base for OBP-domain resources: obp_class + the STEP provenance
    ref (the `#123` the mapping consumed) + the OBP attribute values."""

    def __init__(self, about=None, identifier=None, title=None,
                 description=None, obp_class=None, step_ref=None,
                 attributes=None, obp_refs=None, service_provider=None,
                 relation=None):
        super().__init__(about, None, None, description, identifier,
                         None, title, None, None, None, None, None,
                         None, None, None, service_provider, relation)
        self.__obp_class = obp_class if obp_class is not None else ""
        self.__step_ref = step_ref if step_ref is not None else ""
        self.__attributes = dict(attributes) if attributes else {}
        self.__obp_refs = list(obp_refs) if obp_refs else []

    @property
    def obp_class(self):
        return self.__obp_class

    @obp_class.setter
    def obp_class(self, value):
        self.__obp_class = value or ""

    @property
    def step_ref(self):
        return self.__step_ref

    @step_ref.setter
    def step_ref(self, value):
        self.__step_ref = value or ""

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, value):
        self.__attributes = dict(value or {})

    @property
    def obp_refs(self):
        return self.__obp_refs

    @obp_refs.setter
    def obp_refs(self, value):
        self.__obp_refs = list(value or [])

    def add_obp_ref(self, target: str):
        self.__obp_refs.append(target)

    def _obp_rdf(self, d, graph):
        if self.obp_class:
            d.rdftype(URIRef(OBP_VOCAB + self.obp_class))
        if self.step_ref:
            d.value(URIRef(UUID_VOCAB + "stepRef"), Literal(self.step_ref))
        for k, v in self.__attributes.items():
            if v is None or isinstance(v, (dict, list, tuple)):
                continue
            d.value(URIRef(OBP_VOCAB + k), Literal(str(v)))
        for ref in self.__obp_refs:
            d.value(URIRef(OBP_VOCAB + "referencedItem"), URIRef(ref))


class OBPResourceNode(OBPResource):
    """A generic OBP entity (Part, PartVersion, IndividualPartView,
    External*GeometricModel, NextAssemblyViewUsage, ...) — one class
    serves the whole -3001 inventory; rdf_type is emitted per instance
    (``obp:<Class>``) in to_rdf."""

    @classmethod
    def from_obp_node(cls, node) -> "OBPResourceNode":
        """Build from a stepper.bom.OBPNode."""
        r = cls(identifier=node.step_ref.lstrip("#"),
                title=node.name or node.obp_class,
                obp_class=node.obp_class,
                step_ref=node.step_ref,
                attributes=node.attributes,
                obp_refs=list(node.obp_refs))
        about = node.step_ref.lstrip("#")
        r.about = about
        return r

    def to_rdf(self, graph, base_url=None, attributes=None):
        identifier = self.identifier
        base_url = self._obp_url(base_url, identifier)
        d = Describer(graph, base=base_url)
        d.about(base_url)
        d.rdftype(URIRef(OSLC_CORE + "Resource"))
        if self.title:
            d.value(DCTERMS.title, Literal(self.title))
        if self.identifier:
            d.value(DCTERMS.identifier, Literal(self.identifier))
        self._obp_rdf(d, graph)
        return graph

    def _obp_url(self, base_url, identifier):
        if identifier and identifier not in (base_url or "").split("/"):
            return (base_url or "").rstrip("/") + "/" + identifier
        return base_url


# -- the UUID identity vocabulary (v12 -400) ---------------------------------

UUID_ROLE_VOCAB = UUID_VOCAB + "role/"


class UuidRelationshipResource(BaseResource):
    """`uuid_relationship` (ISO/TS 10303-400 v12): uuid_1 + uuid_2 + role.

    The standards-track form of a Vee link: uuid_1 = the SysML side's
    stable id (sysmlpy interchange @id, `sysml:…`), uuid_2 = the STEP
    side's instance uuid (Hash_based_v5_uuid_attribute output or the
    provenance ref), role = realizes|specifies|traces.
    """

    rdf_type = URIRef(UUID_VOCAB + "UuidRelationship")

    def __init__(self, about=None, identifier=None,
                 uuid_1=None, uuid_2=None, role=None,
                 service_provider=None, relation=None):
        super().__init__(about, None, None, None, identifier, None, None,
                         None, None, None, None, None, None, None, None,
                         service_provider, relation)
        self.__uuid_1 = uuid_1 if uuid_1 is not None else ""
        self.__uuid_2 = uuid_2 if uuid_2 is not None else ""
        self.__role = role if role is not None else "realizes"

    @property
    def uuid_1(self):
        return self.__uuid_1

    @uuid_1.setter
    def uuid_1(self, value):
        self.__uuid_1 = value or ""

    @property
    def uuid_2(self):
        return self.__uuid_2

    @uuid_2.setter
    def uuid_2(self, value):
        self.__uuid_2 = value or ""

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        self.__role = value or "realizes"

    def to_rdf(self, graph, base_url=None, attributes=None):
        identifier = self.identifier
        base_url = self._self_url(base_url, identifier)
        d = Describer(graph, base=base_url)
        d.about(base_url)
        d.rdftype(self.rdf_type)
        if self.identifier:
            d.value(DCTERMS.identifier, Literal(self.identifier))
        if self.__uuid_1:
            d.value(URIRef(UUID_VOCAB + "uuid1"), Literal(self.__uuid_1))
        if self.__uuid_2:
            d.value(URIRef(UUID_VOCAB + "uuid2"), Literal(self.__uuid_2))
        # role is a RESOURCE (role/realizes), not a literal — Describer.value
        # casts everything to Literal, so add the triple directly.
        graph.add((URIRef(base_url), URIRef(UUID_VOCAB + "role"),
                   URIRef(UUID_ROLE_VOCAB + self.__role)))
        return graph

    def _self_url(self, base_url, identifier):
        if identifier and identifier not in (base_url or "").split("/"):
            return (base_url or "").rstrip("/") + "/" + identifier
        return base_url

    @classmethod
    def from_vee_link(cls, link) -> "UuidRelationshipResource":
        """Adapt a P3 VeeLink into the -400 vocabulary.

        uuid_1 = SysML stable id, uuid_2 = STEP uuid (a Hash_based_v5
        value when the STEP side carries real uuid attributes, else the
        provenance ref — '#4374'), identifier = the link's join key.
        """
        # fragment-free identifier ('#' cannot appear in a URL path)
        step_key = link.step_ref.lstrip("#") or "none"
        identifier = f"{link.sysml_id}__{step_key}__{link.kind}"
        return cls(identifier=identifier,
                   uuid_1=link.sysml_id,
                   uuid_2=link.step_ref,
                   role=link.kind)