import logging

from rdflib import RDF, BNode, Literal, URIRef
from rdflib.namespace import DCTERMS, XSD

from pyoslc.resources.models import BaseResource
from pyoslc.vocabularies.am import OSLC_AM
from pyoslc.vocabularies.core import OSLC
from pyoslc.vocabularies.sysml import OSLC_SYSML

logger = logging.getLogger(__name__)

SYSML_NS = str(OSLC_SYSML)


class SysMLElement(BaseResource):

    def __init__(self, about=None, types=None, properties=None,
                 description=None, identifier=None, short_title=None,
                 title=None, contributor=None, creator=None, subject=None,
                 created=None, modified=None, type=None,
                 discussed_by=None, instance_shape=None,
                 service_provider=None, relation=None,
                 element_id=None, alias_ids=None,
                 declared_name=None, declared_short_name=None,
                 name=None, short_name=None, qualified_name=None,
                 is_implied_included=None, is_library_element=None,
                 owner=None, owning_namespace=None,
                 owning_membership=None, owning_relationship=None,
                 owned_element=None, owned_relationship=None,
                 owned_annotation=None,
                 documentation=None, textual_representation=None):

        super().__init__(
            about, types, properties, description, identifier,
            short_title, title, contributor, creator, subject,
            created, modified, type, discussed_by, instance_shape,
            service_provider, relation,
        )

        self.__element_id = element_id if element_id is not None else ''
        self.__alias_ids = alias_ids if alias_ids is not None else []
        self.__declared_name = declared_name if declared_name is not None else ''
        self.__declared_short_name = declared_short_name if declared_short_name is not None else ''
        self.__name = name if name is not None else ''
        self.__short_name = short_name if short_name is not None else ''
        self.__qualified_name = qualified_name if qualified_name is not None else ''
        self.__is_implied_included = is_implied_included if is_implied_included is not None else False
        self.__is_library_element = is_library_element if is_library_element is not None else False
        self.__owner = owner if owner is not None else None
        self.__owning_namespace = owning_namespace if owning_namespace is not None else None
        self.__owning_membership = owning_membership if owning_membership is not None else None
        self.__owning_relationship = owning_relationship if owning_relationship is not None else None
        self.__owned_element = owned_element if owned_element is not None else []
        self.__owned_relationship = owned_relationship if owned_relationship is not None else []
        self.__owned_annotation = owned_annotation if owned_annotation is not None else []
        self.__documentation = documentation if documentation is not None else []
        self.__textual_representation = textual_representation if textual_representation is not None else []

    @property
    def element_id(self):
        return self.__element_id

    @element_id.setter
    def element_id(self, value):
        self.__element_id = value

    @property
    def alias_ids(self):
        return self.__alias_ids

    @alias_ids.setter
    def alias_ids(self, value):
        self.__alias_ids = value

    def add_alias_id(self, value):
        self.__alias_ids.append(value)

    @property
    def declared_name(self):
        return self.__declared_name

    @declared_name.setter
    def declared_name(self, value):
        self.__declared_name = value

    @property
    def declared_short_name(self):
        return self.__declared_short_name

    @declared_short_name.setter
    def declared_short_name(self, value):
        self.__declared_short_name = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def short_name(self):
        return self.__short_name

    @short_name.setter
    def short_name(self, value):
        self.__short_name = value

    @property
    def qualified_name(self):
        return self.__qualified_name

    @qualified_name.setter
    def qualified_name(self, value):
        self.__qualified_name = value

    @property
    def is_implied_included(self):
        return self.__is_implied_included

    @is_implied_included.setter
    def is_implied_included(self, value):
        self.__is_implied_included = value

    @property
    def is_library_element(self):
        return self.__is_library_element

    @is_library_element.setter
    def is_library_element(self, value):
        self.__is_library_element = value

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value

    @property
    def owning_namespace(self):
        return self.__owning_namespace

    @owning_namespace.setter
    def owning_namespace(self, value):
        self.__owning_namespace = value

    @property
    def owning_membership(self):
        return self.__owning_membership

    @owning_membership.setter
    def owning_membership(self, value):
        self.__owning_membership = value

    @property
    def owning_relationship(self):
        return self.__owning_relationship

    @owning_relationship.setter
    def owning_relationship(self, value):
        self.__owning_relationship = value

    @property
    def owned_element(self):
        return self.__owned_element

    @owned_element.setter
    def owned_element(self, value):
        self.__owned_element = value

    def add_owned_element(self, value):
        self.__owned_element.append(value)

    @property
    def owned_relationship(self):
        return self.__owned_relationship

    @owned_relationship.setter
    def owned_relationship(self, value):
        self.__owned_relationship = value

    def add_owned_relationship(self, value):
        self.__owned_relationship.append(value)

    @property
    def owned_annotation(self):
        return self.__owned_annotation

    @owned_annotation.setter
    def owned_annotation(self, value):
        self.__owned_annotation = value

    @property
    def documentation(self):
        return self.__documentation

    @documentation.setter
    def documentation(self, value):
        self.__documentation = value

    @property
    def textual_representation(self):
        return self.__textual_representation

    @textual_representation.setter
    def textual_representation(self, value):
        self.__textual_representation = value

    @staticmethod
    def get_absolute_url(base_url, identifier):
        return base_url + "/" + identifier

    def _add_element_properties_rdf(self, d, graph):
        if self.__element_id:
            d.value(OSLC_SYSML.elementId, Literal(self.__element_id))

        for alias in self.__alias_ids:
            d.value(OSLC_SYSML.aliasIds, Literal(alias))

        if self.__declared_name:
            d.value(OSLC_SYSML.declaredName, Literal(self.__declared_name))

        if self.__declared_short_name:
            d.value(OSLC_SYSML.declaredShortName, Literal(self.__declared_short_name))

        if self.__name:
            d.value(OSLC_SYSML.name, Literal(self.__name))

        if self.__short_name:
            d.value(OSLC_SYSML.shortName, Literal(self.__short_name))

        if self.__qualified_name:
            d.value(OSLC_SYSML.qualifiedName, Literal(self.__qualified_name))

        d.value(OSLC_SYSML.isImpliedIncluded,
                Literal(self.__is_implied_included, datatype=XSD.boolean))
        d.value(OSLC_SYSML.isLibraryElement,
                Literal(self.__is_library_element, datatype=XSD.boolean))

        if self.__owner:
            d.value(OSLC_SYSML.owner, URIRef(self.__owner))

        if self.__owning_namespace:
            d.value(OSLC_SYSML.owningNamespace, URIRef(self.__owning_namespace))

        if self.__owning_membership:
            d.value(OSLC_SYSML.owningMembership, URIRef(self.__owning_membership))

        if self.__owning_relationship:
            d.value(OSLC_SYSML.owningRelationship, URIRef(self.__owning_relationship))

        for elem in self.__owned_element:
            d.value(OSLC_SYSML.ownedElement, URIRef(elem))

        for rel in self.__owned_relationship:
            d.value(OSLC_SYSML.ownedRelationship, URIRef(rel))

        for ann in self.__owned_annotation:
            d.value(OSLC_SYSML.ownedAnnotation, URIRef(ann))

        for doc in self.__documentation:
            d.value(OSLC_SYSML.documentation, URIRef(doc))

        for tr in self.__textual_representation:
            d.value(OSLC_SYSML.textualRepresentation, URIRef(tr))

    def _add_base_properties_rdf(self, d, graph, base_url):
        if self.identifier:
            d.value(DCTERMS.identifier, Literal(self.identifier))

        if self.title:
            d.value(DCTERMS.title, Literal(self.title))

        if self.description:
            d.value(DCTERMS.description, Literal(self.description))

        if self.created:
            d.value(DCTERMS.created, Literal(str(self.created)))

        if self.modified:
            d.value(DCTERMS.modified, Literal(str(self.modified)))

        for c in self.creator:
            d.value(DCTERMS.creator, Literal(c))

        for c in self.contributor:
            d.value(DCTERMS.contributor, Literal(c))

        if self.instance_shape:
            d.value(OSLC.instanceShape, URIRef(self.instance_shape))

        for sp in self.service_provider:
            d.value(OSLC.serviceProvider, URIRef(sp))

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind('oslc_sysml', OSLC_SYSML)
        graph.bind('oslc_am', OSLC_AM)
        graph.bind('oslc', OSLC)

        from rdflib.extras.describer import Describer

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        d = Describer(graph, base=base_url)
        d.about(base_url)
        d.rdftype(OSLC_AM.Resource)
        d.rdftype(OSLC_SYSML.Element)

        self._add_base_properties_rdf(d, graph, base_url)
        self._add_element_properties_rdf(d, graph)

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Element):
            setattr(self, '_AbstractResource__about', str(r))

            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, DCTERMS.title):
                self.title = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, DCTERMS.description):
                self.description = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, DCTERMS.created):
                self.created = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, DCTERMS.modified):
                self.modified = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.elementId):
                self.element_id = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.aliasIds):
                self.add_alias_id(o.value if isinstance(o, Literal) else str(o))

            for o in g.objects(r, OSLC_SYSML.declaredName):
                self.declared_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.declaredShortName):
                self.declared_short_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.name):
                self.name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.shortName):
                self.short_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.qualifiedName):
                self.qualified_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.isImpliedIncluded):
                self.is_implied_included = o.value if isinstance(o, Literal) else False

            for o in g.objects(r, OSLC_SYSML.isLibraryElement):
                self.is_library_element = o.value if isinstance(o, Literal) else False

            for o in g.objects(r, OSLC_SYSML.owner):
                self.owner = str(o)

            for o in g.objects(r, OSLC_SYSML.owningNamespace):
                self.owning_namespace = str(o)

            for o in g.objects(r, OSLC_SYSML.owningMembership):
                self.owning_membership = str(o)

            for o in g.objects(r, OSLC_SYSML.owningRelationship):
                self.owning_relationship = str(o)

            for o in g.objects(r, OSLC_SYSML.ownedElement):
                self.add_owned_element(str(o))

            for o in g.objects(r, OSLC_SYSML.ownedRelationship):
                self.add_owned_relationship(str(o))

            for o in g.objects(r, OSLC.instanceShape):
                self.instance_shape = str(o)

            for o in g.objects(r, OSLC.serviceProvider):
                self.add_service_provider(str(o))

    def from_json(self, data, attributes=None):
        if 'identifier' in data:
            self.identifier = data['identifier']
        if 'title' in data:
            self.title = data['title']
        if 'description' in data:
            self.description = data['description']
        if 'element_id' in data:
            self.element_id = data['element_id']
        if 'declared_name' in data:
            self.declared_name = data['declared_name']
        if 'declared_short_name' in data:
            self.declared_short_name = data['declared_short_name']
        if 'name' in data:
            self.name = data['name']
        if 'short_name' in data:
            self.short_name = data['short_name']
        if 'qualified_name' in data:
            self.qualified_name = data['qualified_name']
        if 'is_implied_included' in data:
            self.is_implied_included = data['is_implied_included']
        if 'is_library_element' in data:
            self.is_library_element = data['is_library_element']
        if 'alias_ids' in data:
            self.alias_ids = data['alias_ids']
        if 'owned_element' in data:
            self.owned_element = data['owned_element']
        if 'owned_relationship' in data:
            self.owned_relationship = data['owned_relationship']

    def to_mapped_object(self, attributes=None):
        result = {
            'identifier': self.identifier,
            'title': self.title,
            'description': self.description,
            'element_id': self.element_id,
            'declared_name': self.declared_name,
            'declared_short_name': self.declared_short_name,
            'name': self.name,
            'short_name': self.short_name,
            'qualified_name': self.qualified_name,
            'is_implied_included': self.is_implied_included,
            'is_library_element': self.is_library_element,
            'alias_ids': self.alias_ids,
        }
        return {k: v for k, v in result.items() if v}

    def _add_element_properties_rdf_direct(self, graph, subject_uri):
        eid = self.element_id
        if eid:
            graph.add((subject_uri, OSLC_SYSML.elementId, Literal(eid)))

        for alias in self.alias_ids:
            graph.add((subject_uri, OSLC_SYSML.aliasIds, Literal(alias)))

        if self.declared_name:
            graph.add((subject_uri, OSLC_SYSML.declaredName, Literal(self.declared_name)))
        if self.declared_short_name:
            graph.add((subject_uri, OSLC_SYSML.declaredShortName,
                       Literal(self.declared_short_name)))
        if self.name:
            graph.add((subject_uri, OSLC_SYSML.name, Literal(self.name)))
        if self.short_name:
            graph.add((subject_uri, OSLC_SYSML.shortName, Literal(self.short_name)))
        if self.qualified_name:
            graph.add((subject_uri, OSLC_SYSML.qualifiedName, Literal(self.qualified_name)))

        graph.add((subject_uri, OSLC_SYSML.isImpliedIncluded,
                   Literal(self.is_implied_included, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isLibraryElement,
                   Literal(self.is_library_element, datatype=XSD.boolean)))

        if self.owner:
            graph.add((subject_uri, OSLC_SYSML.owner, URIRef(self.owner)))
        if self.owning_namespace:
            graph.add((subject_uri, OSLC_SYSML.owningNamespace,
                       URIRef(self.owning_namespace)))
        if self.owning_membership:
            graph.add((subject_uri, OSLC_SYSML.owningMembership,
                       URIRef(self.owning_membership)))
        if self.owning_relationship:
            graph.add((subject_uri, OSLC_SYSML.owningRelationship,
                       URIRef(self.owning_relationship)))

        for elem in self.owned_element:
            graph.add((subject_uri, OSLC_SYSML.ownedElement, URIRef(elem)))
        for rel in self.owned_relationship:
            graph.add((subject_uri, OSLC_SYSML.ownedRelationship, URIRef(rel)))
        for ann in self.owned_annotation:
            graph.add((subject_uri, OSLC_SYSML.ownedAnnotation, URIRef(ann)))
        for doc in self.documentation:
            graph.add((subject_uri, OSLC_SYSML.documentation, URIRef(doc)))
        for tr in self.textual_representation:
            graph.add((subject_uri, OSLC_SYSML.textualRepresentation, URIRef(tr)))


class SysMLRelationship(SysMLElement):

    def __init__(self, about=None, types=None, properties=None,
                 description=None, identifier=None, short_title=None,
                 title=None, contributor=None, creator=None, subject=None,
                 created=None, modified=None, type=None,
                 discussed_by=None, instance_shape=None,
                 service_provider=None, relation=None,
                 element_id=None, alias_ids=None,
                 declared_name=None, declared_short_name=None,
                 name=None, short_name=None, qualified_name=None,
                 is_implied_included=None, is_library_element=None,
                 owner=None, owning_namespace=None,
                 owning_membership=None, owning_relationship=None,
                 owned_element=None, owned_relationship=None,
                 owned_annotation=None,
                 documentation=None, textual_representation=None,
                 source=None, target=None,
                 is_implied=None,
                 related_element=None,
                 owned_related_element=None,
                 owning_related_element=None):

        super().__init__(
            about, types, properties, description, identifier,
            short_title, title, contributor, creator, subject,
            created, modified, type, discussed_by, instance_shape,
            service_provider, relation,
            element_id, alias_ids, declared_name, declared_short_name,
            name, short_name, qualified_name,
            is_implied_included, is_library_element,
            owner, owning_namespace, owning_membership,
            owning_relationship, owned_element, owned_relationship,
            owned_annotation, documentation, textual_representation,
        )

        self.__source = source if source is not None else []
        self.__target = target if target is not None else []
        self.__is_implied = is_implied if is_implied is not None else False
        self.__related_element = related_element if related_element is not None else []
        self.__owned_related_element = owned_related_element if owned_related_element is not None else []
        self.__owning_related_element = owning_related_element if owning_related_element is not None else None

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        self.__source = value

    def add_source(self, value):
        self.__source.append(value)

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        self.__target = value

    def add_target(self, value):
        self.__target.append(value)

    @property
    def is_implied(self):
        return self.__is_implied

    @is_implied.setter
    def is_implied(self, value):
        self.__is_implied = value

    @property
    def related_element(self):
        return self.__related_element

    @related_element.setter
    def related_element(self, value):
        self.__related_element = value

    def add_related_element(self, value):
        self.__related_element.append(value)

    @property
    def owned_related_element(self):
        return self.__owned_related_element

    @owned_related_element.setter
    def owned_related_element(self, value):
        self.__owned_related_element = value

    def add_owned_related_element(self, value):
        self.__owned_related_element.append(value)

    @property
    def owning_related_element(self):
        return self.__owning_related_element

    @owning_related_element.setter
    def owning_related_element(self, value):
        self.__owning_related_element = value

    @staticmethod
    def _emit_reified_ordered(graph, subject_uri, predicate, values):
        for idx, val in enumerate(values, start=1):
            stmt = BNode()
            graph.add((stmt, RDF.type, RDF.Statement))
            graph.add((stmt, RDF.subject, subject_uri))
            graph.add((stmt, RDF.predicate, predicate))
            graph.add((stmt, RDF.object, URIRef(val)))
            graph.add((stmt, OSLC_SYSML.order, Literal(idx, datatype=XSD.integer)))

    @staticmethod
    def _read_reified_ordered(graph, subject_uri, predicate):
        ordered = []
        for stmt in graph.subjects(RDF.type, RDF.Statement):
            s = list(graph.objects(stmt, RDF.subject))
            p = list(graph.objects(stmt, RDF.predicate))
            o = list(graph.objects(stmt, RDF.object))
            order = list(graph.objects(stmt, OSLC_SYSML.order))
            if (s and p and o and order
                    and str(s[0]) == str(subject_uri)
                    and str(p[0]) == str(predicate)):
                ordered.append((
                    order[0].value if isinstance(order[0], Literal) else int(str(order[0])),
                    str(o[0]),
                ))
        ordered.sort(key=lambda x: x[0])
        return [v for _, v in ordered]

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind('oslc_sysml', OSLC_SYSML)
        graph.bind('oslc_am', OSLC_AM)
        graph.bind('oslc', OSLC)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)

        graph.add((subject_uri, RDF.type, OSLC_AM.Resource))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Element))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Relationship))

        if self.identifier:
            graph.add((subject_uri, DCTERMS.identifier, Literal(self.identifier)))
        if self.title:
            graph.add((subject_uri, DCTERMS.title, Literal(self.title)))
        if self.description:
            graph.add((subject_uri, DCTERMS.description, Literal(self.description)))
        if self.created:
            graph.add((subject_uri, DCTERMS.created, Literal(str(self.created))))
        if self.modified:
            graph.add((subject_uri, DCTERMS.modified, Literal(str(self.modified))))

        for c in self.creator:
            graph.add((subject_uri, DCTERMS.creator, Literal(c)))
        for c in self.contributor:
            graph.add((subject_uri, DCTERMS.contributor, Literal(c)))

        if self.instance_shape:
            graph.add((subject_uri, OSLC.instanceShape, URIRef(self.instance_shape)))
        for sp in self.service_provider:
            graph.add((subject_uri, OSLC.serviceProvider, URIRef(sp)))

        self._add_element_properties_rdf_direct(graph, subject_uri)

        for src in self.__source:
            graph.add((subject_uri, OSLC_SYSML.source, URIRef(src)))
        for tgt in self.__target:
            graph.add((subject_uri, OSLC_SYSML.target, URIRef(tgt)))

        self._emit_reified_ordered(graph, subject_uri, OSLC_SYSML.source, self.__source)
        self._emit_reified_ordered(graph, subject_uri, OSLC_SYSML.target, self.__target)

        graph.add((subject_uri, OSLC_SYSML.isImplied,
                   Literal(self.__is_implied, datatype=XSD.boolean)))

        for re in self.__related_element:
            graph.add((subject_uri, OSLC_SYSML.relatedElement, URIRef(re)))
        for ore in self.__owned_related_element:
            graph.add((subject_uri, OSLC_SYSML.ownedRelatedElement, URIRef(ore)))
        if self.__owning_related_element:
            graph.add((subject_uri, OSLC_SYSML.owningRelatedElement,
                       URIRef(self.__owning_related_element)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Relationship):
            setattr(self, '_AbstractResource__about', str(r))

            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.created):
                self.created = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.modified):
                self.modified = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.elementId):
                self.element_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.aliasIds):
                self.add_alias_id(o.value if isinstance(o, Literal) else str(o))
            for o in g.objects(r, OSLC_SYSML.declaredName):
                self.declared_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.declaredShortName):
                self.declared_short_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.name):
                self.name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.shortName):
                self.short_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.qualifiedName):
                self.qualified_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.isImpliedIncluded):
                self.is_implied_included = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isLibraryElement):
                self.is_library_element = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isImplied):
                self.is_implied = o.value if isinstance(o, Literal) else False

            for o in g.objects(r, OSLC_SYSML.owner):
                self.owner = str(o)
            for o in g.objects(r, OSLC_SYSML.owningNamespace):
                self.owning_namespace = str(o)
            for o in g.objects(r, OSLC_SYSML.owningMembership):
                self.owning_membership = str(o)
            for o in g.objects(r, OSLC_SYSML.owningRelationship):
                self.owning_relationship = str(o)

            for o in g.objects(r, OSLC_SYSML.ownedElement):
                self.add_owned_element(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedRelationship):
                self.add_owned_relationship(str(o))

            self.source = self._read_reified_ordered(g, r, OSLC_SYSML.source)
            if not self.source:
                self.source = [str(o) for o in g.objects(r, OSLC_SYSML.source)]

            self.target = self._read_reified_ordered(g, r, OSLC_SYSML.target)
            if not self.target:
                self.target = [str(o) for o in g.objects(r, OSLC_SYSML.target)]

            for o in g.objects(r, OSLC_SYSML.relatedElement):
                self.add_related_element(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedRelatedElement):
                self.add_owned_related_element(str(o))
            for o in g.objects(r, OSLC_SYSML.owningRelatedElement):
                self.owning_related_element = str(o)

            for o in g.objects(r, OSLC.instanceShape):
                self.instance_shape = str(o)
            for o in g.objects(r, OSLC.serviceProvider):
                self.add_service_provider(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'source' in data:
            self.source = data['source'] if isinstance(data['source'], list) else [data['source']]
        if 'target' in data:
            self.target = data['target'] if isinstance(data['target'], list) else [data['target']]
        if 'is_implied' in data:
            self.is_implied = data['is_implied']
        if 'related_element' in data:
            vals = data['related_element']
            self.related_element = vals if isinstance(vals, list) else [vals]
        if 'owned_related_element' in data:
            vals = data['owned_related_element']
            self.owned_related_element = vals if isinstance(vals, list) else [vals]
        if 'owning_related_element' in data:
            self.owning_related_element = data['owning_related_element']

    def to_mapped_object(self, attributes=None):
        result = super().to_mapped_object(attributes)
        result.update({
            'source': self.source,
            'target': self.target,
            'is_implied': self.is_implied,
            'related_element': self.related_element,
            'owned_related_element': self.owned_related_element,
            'owning_related_element': self.owning_related_element,
        })
        return {k: v for k, v in result.items() if v or v is False}


class SysMLNamespace(SysMLElement):

    def __init__(self, about=None, types=None, properties=None,
                 description=None, identifier=None, short_title=None,
                 title=None, contributor=None, creator=None, subject=None,
                 created=None, modified=None, type=None,
                 discussed_by=None, instance_shape=None,
                 service_provider=None, relation=None,
                 element_id=None, alias_ids=None,
                 declared_name=None, declared_short_name=None,
                 name=None, short_name=None, qualified_name=None,
                 is_implied_included=None, is_library_element=None,
                 owner=None, owning_namespace=None,
                 owning_membership=None, owning_relationship=None,
                 owned_element=None, owned_relationship=None,
                 owned_annotation=None,
                 documentation=None, textual_representation=None,
                 member=None, membership=None,
                 owned_member=None, owned_membership=None,
                 imported_membership=None, owned_import=None):

        super().__init__(
            about, types, properties, description, identifier,
            short_title, title, contributor, creator, subject,
            created, modified, type, discussed_by, instance_shape,
            service_provider, relation,
            element_id, alias_ids, declared_name, declared_short_name,
            name, short_name, qualified_name,
            is_implied_included, is_library_element,
            owner, owning_namespace, owning_membership,
            owning_relationship, owned_element, owned_relationship,
            owned_annotation, documentation, textual_representation,
        )

        self.__member = member if member is not None else []
        self.__membership = membership if membership is not None else []
        self.__owned_member = owned_member if owned_member is not None else []
        self.__owned_membership = owned_membership if owned_membership is not None else []
        self.__imported_membership = imported_membership if imported_membership is not None else []
        self.__owned_import = owned_import if owned_import is not None else []

    @property
    def member(self):
        return self.__member

    @member.setter
    def member(self, value):
        self.__member = value

    def add_member(self, value):
        self.__member.append(value)

    @property
    def membership(self):
        return self.__membership

    @membership.setter
    def membership(self, value):
        self.__membership = value

    @property
    def owned_member(self):
        return self.__owned_member

    @owned_member.setter
    def owned_member(self, value):
        self.__owned_member = value

    def add_owned_member(self, value):
        self.__owned_member.append(value)

    @property
    def owned_membership(self):
        return self.__owned_membership

    @owned_membership.setter
    def owned_membership(self, value):
        self.__owned_membership = value

    @property
    def imported_membership(self):
        return self.__imported_membership

    @imported_membership.setter
    def imported_membership(self, value):
        self.__imported_membership = value

    @property
    def owned_import(self):
        return self.__owned_import

    @owned_import.setter
    def owned_import(self, value):
        self.__owned_import = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind('oslc_sysml', OSLC_SYSML)
        graph.bind('oslc_am', OSLC_AM)
        graph.bind('oslc', OSLC)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)

        graph.add((subject_uri, RDF.type, OSLC_AM.Resource))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Element))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Namespace))

        if self.identifier:
            graph.add((subject_uri, DCTERMS.identifier, Literal(self.identifier)))
        if self.title:
            graph.add((subject_uri, DCTERMS.title, Literal(self.title)))
        if self.description:
            graph.add((subject_uri, DCTERMS.description, Literal(self.description)))

        self._add_element_properties_rdf_direct(graph, subject_uri)

        for m in self.__member:
            graph.add((subject_uri, OSLC_SYSML.member, URIRef(m)))
        for m in self.__membership:
            graph.add((subject_uri, OSLC_SYSML.membership, URIRef(m)))
        for m in self.__owned_member:
            graph.add((subject_uri, OSLC_SYSML.ownedMember, URIRef(m)))
        for m in self.__owned_membership:
            graph.add((subject_uri, OSLC_SYSML.ownedMembership, URIRef(m)))
        for m in self.__imported_membership:
            graph.add((subject_uri, OSLC_SYSML.importedMembership, URIRef(m)))
        for m in self.__owned_import:
            graph.add((subject_uri, OSLC_SYSML.ownedImport, URIRef(m)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Namespace):
            setattr(self, '_AbstractResource__about', str(r))

            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.elementId):
                self.element_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.declaredName):
                self.declared_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.name):
                self.name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.qualifiedName):
                self.qualified_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.member):
                self.add_member(str(o))
            for o in g.objects(r, OSLC_SYSML.membership):
                self.membership.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedMember):
                self.add_owned_member(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedMembership):
                self.owned_membership.append(str(o))
            for o in g.objects(r, OSLC_SYSML.importedMembership):
                self.imported_membership.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedImport):
                self.owned_import.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'member' in data:
            self.member = data['member'] if isinstance(data['member'], list) else [data['member']]
        if 'owned_member' in data:
            vals = data['owned_member']
            self.owned_member = vals if isinstance(vals, list) else [vals]


class SysMLType(SysMLNamespace):

    def __init__(self, about=None, types=None, properties=None,
                 description=None, identifier=None, short_title=None,
                 title=None, contributor=None, creator=None, subject=None,
                 created=None, modified=None, type=None,
                 discussed_by=None, instance_shape=None,
                 service_provider=None, relation=None,
                 element_id=None, alias_ids=None,
                 declared_name=None, declared_short_name=None,
                 name=None, short_name=None, qualified_name=None,
                 is_implied_included=None, is_library_element=None,
                 owner=None, owning_namespace=None,
                 owning_membership=None, owning_relationship=None,
                 owned_element=None, owned_relationship=None,
                 owned_annotation=None,
                 documentation=None, textual_representation=None,
                 member=None, membership=None,
                 owned_member=None, owned_membership=None,
                 imported_membership=None, owned_import=None,
                 is_abstract=None, is_conjugated=None, is_sufficient=None,
                 multiplicity=None, feature=None, directed_feature=None,
                 end_feature=None, owned_feature=None, owned_end_feature=None,
                 owned_feature_membership=None, feature_membership=None,
                 inherited_feature=None, inherited_membership=None,
                 input=None, output=None,
                 owned_specialization=None, owned_conjugator=None,
                 owned_differencing=None, owned_disjoining=None,
                 owned_intersecting=None, owned_unioning=None):

        super().__init__(
            about, types, properties, description, identifier,
            short_title, title, contributor, creator, subject,
            created, modified, type, discussed_by, instance_shape,
            service_provider, relation,
            element_id, alias_ids, declared_name, declared_short_name,
            name, short_name, qualified_name,
            is_implied_included, is_library_element,
            owner, owning_namespace, owning_membership,
            owning_relationship, owned_element, owned_relationship,
            owned_annotation, documentation, textual_representation,
            member, membership, owned_member, owned_membership,
            imported_membership, owned_import,
        )

        self.__is_abstract = is_abstract if is_abstract is not None else False
        self.__is_conjugated = is_conjugated if is_conjugated is not None else False
        self.__is_sufficient = is_sufficient if is_sufficient is not None else False
        self.__multiplicity = multiplicity if multiplicity is not None else None
        self.__feature = feature if feature is not None else []
        self.__directed_feature = directed_feature if directed_feature is not None else []
        self.__end_feature = end_feature if end_feature is not None else []
        self.__owned_feature = owned_feature if owned_feature is not None else []
        self.__owned_end_feature = owned_end_feature if owned_end_feature is not None else []
        self.__owned_feature_membership = owned_feature_membership if owned_feature_membership is not None else []
        self.__feature_membership = feature_membership if feature_membership is not None else []
        self.__inherited_feature = inherited_feature if inherited_feature is not None else []
        self.__inherited_membership = inherited_membership if inherited_membership is not None else []
        self.__input = input if input is not None else []
        self.__output = output if output is not None else []
        self.__owned_specialization = owned_specialization if owned_specialization is not None else []
        self.__owned_conjugator = owned_conjugator if owned_conjugator is not None else None
        self.__owned_differencing = owned_differencing if owned_differencing is not None else []
        self.__owned_disjoining = owned_disjoining if owned_disjoining is not None else []
        self.__owned_intersecting = owned_intersecting if owned_intersecting is not None else []
        self.__owned_unioning = owned_unioning if owned_unioning is not None else []

    @property
    def is_abstract(self):
        return self.__is_abstract

    @is_abstract.setter
    def is_abstract(self, value):
        self.__is_abstract = value

    @property
    def is_conjugated(self):
        return self.__is_conjugated

    @is_conjugated.setter
    def is_conjugated(self, value):
        self.__is_conjugated = value

    @property
    def is_sufficient(self):
        return self.__is_sufficient

    @is_sufficient.setter
    def is_sufficient(self, value):
        self.__is_sufficient = value

    @property
    def multiplicity(self):
        return self.__multiplicity

    @multiplicity.setter
    def multiplicity(self, value):
        self.__multiplicity = value

    @property
    def feature(self):
        return self.__feature

    @feature.setter
    def feature(self, value):
        self.__feature = value

    @property
    def directed_feature(self):
        return self.__directed_feature

    @directed_feature.setter
    def directed_feature(self, value):
        self.__directed_feature = value

    @property
    def end_feature(self):
        return self.__end_feature

    @end_feature.setter
    def end_feature(self, value):
        self.__end_feature = value

    @property
    def owned_feature(self):
        return self.__owned_feature

    @owned_feature.setter
    def owned_feature(self, value):
        self.__owned_feature = value

    @property
    def owned_end_feature(self):
        return self.__owned_end_feature

    @owned_end_feature.setter
    def owned_end_feature(self, value):
        self.__owned_end_feature = value

    @property
    def owned_feature_membership(self):
        return self.__owned_feature_membership

    @owned_feature_membership.setter
    def owned_feature_membership(self, value):
        self.__owned_feature_membership = value

    @property
    def feature_membership(self):
        return self.__feature_membership

    @feature_membership.setter
    def feature_membership(self, value):
        self.__feature_membership = value

    @property
    def inherited_feature(self):
        return self.__inherited_feature

    @inherited_feature.setter
    def inherited_feature(self, value):
        self.__inherited_feature = value

    @property
    def inherited_membership(self):
        return self.__inherited_membership

    @inherited_membership.setter
    def inherited_membership(self, value):
        self.__inherited_membership = value

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        self.__input = value

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    @property
    def owned_specialization(self):
        return self.__owned_specialization

    @owned_specialization.setter
    def owned_specialization(self, value):
        self.__owned_specialization = value

    @property
    def owned_conjugator(self):
        return self.__owned_conjugator

    @owned_conjugator.setter
    def owned_conjugator(self, value):
        self.__owned_conjugator = value

    @property
    def owned_differencing(self):
        return self.__owned_differencing

    @owned_differencing.setter
    def owned_differencing(self, value):
        self.__owned_differencing = value

    @property
    def owned_disjoining(self):
        return self.__owned_disjoining

    @owned_disjoining.setter
    def owned_disjoining(self, value):
        self.__owned_disjoining = value

    @property
    def owned_intersecting(self):
        return self.__owned_intersecting

    @owned_intersecting.setter
    def owned_intersecting(self, value):
        self.__owned_intersecting = value

    @property
    def owned_unioning(self):
        return self.__owned_unioning

    @owned_unioning.setter
    def owned_unioning(self, value):
        self.__owned_unioning = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind('oslc_sysml', OSLC_SYSML)
        graph.bind('oslc_am', OSLC_AM)
        graph.bind('oslc', OSLC)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)

        graph.add((subject_uri, RDF.type, OSLC_AM.Resource))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Element))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Namespace))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Type))

        if self.identifier:
            graph.add((subject_uri, DCTERMS.identifier, Literal(self.identifier)))
        if self.title:
            graph.add((subject_uri, DCTERMS.title, Literal(self.title)))
        if self.description:
            graph.add((subject_uri, DCTERMS.description, Literal(self.description)))

        self._add_element_properties_rdf_direct(graph, subject_uri)

        graph.add((subject_uri, OSLC_SYSML.isAbstract,
                   Literal(self.__is_abstract, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isConjugated,
                   Literal(self.__is_conjugated, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isSufficient,
                   Literal(self.__is_sufficient, datatype=XSD.boolean)))

        if self.__multiplicity:
            graph.add((subject_uri, OSLC_SYSML.multiplicity, URIRef(self.__multiplicity)))

        for f in self.__feature:
            graph.add((subject_uri, OSLC_SYSML.feature, URIRef(f)))
        for f in self.__directed_feature:
            graph.add((subject_uri, OSLC_SYSML.directedFeature, URIRef(f)))
        for f in self.__end_feature:
            graph.add((subject_uri, OSLC_SYSML.endFeature, URIRef(f)))
        for f in self.__owned_feature:
            graph.add((subject_uri, OSLC_SYSML.ownedFeature, URIRef(f)))
        for f in self.__owned_end_feature:
            graph.add((subject_uri, OSLC_SYSML.ownedEndFeature, URIRef(f)))
        for f in self.__owned_feature_membership:
            graph.add((subject_uri, OSLC_SYSML.ownedFeatureMembership, URIRef(f)))
        for f in self.__feature_membership:
            graph.add((subject_uri, OSLC_SYSML.featureMembership, URIRef(f)))
        for f in self.__inherited_feature:
            graph.add((subject_uri, OSLC_SYSML.inheritedFeature, URIRef(f)))
        for f in self.__inherited_membership:
            graph.add((subject_uri, OSLC_SYSML.inheritedMembership, URIRef(f)))
        for f in self.__input:
            graph.add((subject_uri, OSLC_SYSML.input, URIRef(f)))
        for f in self.__output:
            graph.add((subject_uri, OSLC_SYSML.output, URIRef(f)))
        for f in self.__owned_specialization:
            graph.add((subject_uri, OSLC_SYSML.ownedSpecialization, URIRef(f)))
        if self.__owned_conjugator:
            graph.add((subject_uri, OSLC_SYSML.ownedConjugator, URIRef(self.__owned_conjugator)))
        for f in self.__owned_differencing:
            graph.add((subject_uri, OSLC_SYSML.ownedDifferencing, URIRef(f)))
        for f in self.__owned_disjoining:
            graph.add((subject_uri, OSLC_SYSML.ownedDisjoining, URIRef(f)))
        for f in self.__owned_intersecting:
            graph.add((subject_uri, OSLC_SYSML.ownedIntersecting, URIRef(f)))
        for f in self.__owned_unioning:
            graph.add((subject_uri, OSLC_SYSML.ownedUnioning, URIRef(f)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Type):
            setattr(self, '_AbstractResource__about', str(r))

            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.elementId):
                self.element_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.declaredName):
                self.declared_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.name):
                self.name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.qualifiedName):
                self.qualified_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.isAbstract):
                self.is_abstract = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isConjugated):
                self.is_conjugated = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isSufficient):
                self.is_sufficient = o.value if isinstance(o, Literal) else False

            for o in g.objects(r, OSLC_SYSML.multiplicity):
                self.multiplicity = str(o)

            for o in g.objects(r, OSLC_SYSML.feature):
                self.feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.directedFeature):
                self.directed_feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedFeature):
                self.owned_feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedSpecialization):
                self.owned_specialization.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_abstract' in data:
            self.is_abstract = data['is_abstract']
        if 'is_conjugated' in data:
            self.is_conjugated = data['is_conjugated']
        if 'is_sufficient' in data:
            self.is_sufficient = data['is_sufficient']
        if 'multiplicity' in data:
            self.multiplicity = data['multiplicity']
        if 'feature' in data:
            self.feature = data['feature'] if isinstance(data['feature'], list) else [data['feature']]
        if 'owned_feature' in data:
            vals = data['owned_feature']
            self.owned_feature = vals if isinstance(vals, list) else [vals]


class SysMLPackage(SysMLNamespace):

    def __init__(self, about=None, types=None, properties=None,
                 description=None, identifier=None, short_title=None,
                 title=None, contributor=None, creator=None, subject=None,
                 created=None, modified=None, type=None,
                 discussed_by=None, instance_shape=None,
                 service_provider=None, relation=None,
                 element_id=None, alias_ids=None,
                 declared_name=None, declared_short_name=None,
                 name=None, short_name=None, qualified_name=None,
                 is_implied_included=None, is_library_element=None,
                 owner=None, owning_namespace=None,
                 owning_membership=None, owning_relationship=None,
                 owned_element=None, owned_relationship=None,
                 owned_annotation=None,
                 documentation=None, textual_representation=None,
                 member=None, membership=None,
                 owned_member=None, owned_membership=None,
                 imported_membership=None, owned_import=None,
                 filter_condition=None):

        super().__init__(
            about, types, properties, description, identifier,
            short_title, title, contributor, creator, subject,
            created, modified, type, discussed_by, instance_shape,
            service_provider, relation,
            element_id, alias_ids, declared_name, declared_short_name,
            name, short_name, qualified_name,
            is_implied_included, is_library_element,
            owner, owning_namespace, owning_membership,
            owning_relationship, owned_element, owned_relationship,
            owned_annotation, documentation, textual_representation,
            member, membership, owned_member, owned_membership,
            imported_membership, owned_import,
        )

        self.__filter_condition = filter_condition if filter_condition is not None else []

    @property
    def filter_condition(self):
        return self.__filter_condition

    @filter_condition.setter
    def filter_condition(self, value):
        self.__filter_condition = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind('oslc_sysml', OSLC_SYSML)
        graph.bind('oslc_am', OSLC_AM)
        graph.bind('oslc', OSLC)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)

        graph.add((subject_uri, RDF.type, OSLC_AM.Resource))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Element))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Namespace))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Package))

        if self.identifier:
            graph.add((subject_uri, DCTERMS.identifier, Literal(self.identifier)))
        if self.title:
            graph.add((subject_uri, DCTERMS.title, Literal(self.title)))
        if self.description:
            graph.add((subject_uri, DCTERMS.description, Literal(self.description)))

        self._add_element_properties_rdf_direct(graph, subject_uri)

        for m in self.member:
            graph.add((subject_uri, OSLC_SYSML.member, URIRef(m)))
        for m in self.owned_member:
            graph.add((subject_uri, OSLC_SYSML.ownedMember, URIRef(m)))

        for fc in self.__filter_condition:
            graph.add((subject_uri, OSLC_SYSML.filterCondition, URIRef(fc)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Package):
            setattr(self, '_AbstractResource__about', str(r))

            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.elementId):
                self.element_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.declaredName):
                self.declared_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.name):
                self.name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.qualifiedName):
                self.qualified_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.member):
                self.add_member(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedMember):
                self.add_owned_member(str(o))
            for o in g.objects(r, OSLC_SYSML.filterCondition):
                self.filter_condition.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'filter_condition' in data:
            vals = data['filter_condition']
            self.filter_condition = vals if isinstance(vals, list) else [vals]


class SysMLDefinition(SysMLType):

    def __init__(self, about=None, types=None, properties=None,
                 description=None, identifier=None, short_title=None,
                 title=None, contributor=None, creator=None, subject=None,
                 created=None, modified=None, type=None,
                 discussed_by=None, instance_shape=None,
                 service_provider=None, relation=None,
                 element_id=None, alias_ids=None,
                 declared_name=None, declared_short_name=None,
                 name=None, short_name=None, qualified_name=None,
                 is_implied_included=None, is_library_element=None,
                 owner=None, owning_namespace=None,
                 owning_membership=None, owning_relationship=None,
                 owned_element=None, owned_relationship=None,
                 owned_annotation=None,
                 documentation=None, textual_representation=None,
                 member=None, membership=None,
                 owned_member=None, owned_membership=None,
                 imported_membership=None, owned_import=None,
                 is_abstract=None, is_conjugated=None, is_sufficient=None,
                 multiplicity=None, feature=None, directed_feature=None,
                 end_feature=None, owned_feature=None, owned_end_feature=None,
                 owned_feature_membership=None, feature_membership=None,
                 inherited_feature=None, inherited_membership=None,
                 input=None, output=None,
                 owned_specialization=None, owned_conjugator=None,
                 owned_differencing=None, owned_disjoining=None,
                 owned_intersecting=None, owned_unioning=None,
                 is_variation=None,
                 owned_action=None, owned_allocation=None,
                 owned_analysis_case=None, owned_attribute=None,
                 owned_calculation=None, owned_case=None,
                 owned_concern=None, owned_connection=None,
                 owned_constraint=None, owned_enumeration=None,
                 owned_flow=None, owned_interface=None,
                 owned_item=None, owned_metadata=None,
                 owned_occurrence=None, owned_part=None,
                 owned_port=None, owned_reference=None,
                 owned_rendering=None, owned_requirement=None,
                 owned_state=None, owned_transition=None,
                 owned_usage=None, owned_use_case=None,
                 owned_verification_case=None, owned_view=None,
                 owned_viewpoint=None, owned_subclassification=None,
                 variant=None, variant_membership=None):

        super().__init__(
            about, types, properties, description, identifier,
            short_title, title, contributor, creator, subject,
            created, modified, type, discussed_by, instance_shape,
            service_provider, relation,
            element_id, alias_ids, declared_name, declared_short_name,
            name, short_name, qualified_name,
            is_implied_included, is_library_element,
            owner, owning_namespace, owning_membership,
            owning_relationship, owned_element, owned_relationship,
            owned_annotation, documentation, textual_representation,
            member, membership, owned_member, owned_membership,
            imported_membership, owned_import,
            is_abstract, is_conjugated, is_sufficient,
            multiplicity, feature, directed_feature,
            end_feature, owned_feature, owned_end_feature,
            owned_feature_membership, feature_membership,
            inherited_feature, inherited_membership,
            input, output,
            owned_specialization, owned_conjugator,
            owned_differencing, owned_disjoining,
            owned_intersecting, owned_unioning,
        )

        self.__is_variation = is_variation if is_variation is not None else False
        self.__owned_action = owned_action if owned_action is not None else []
        self.__owned_allocation = owned_allocation if owned_allocation is not None else []
        self.__owned_analysis_case = owned_analysis_case if owned_analysis_case is not None else []
        self.__owned_attribute = owned_attribute if owned_attribute is not None else []
        self.__owned_calculation = owned_calculation if owned_calculation is not None else []
        self.__owned_case = owned_case if owned_case is not None else []
        self.__owned_concern = owned_concern if owned_concern is not None else []
        self.__owned_connection = owned_connection if owned_connection is not None else []
        self.__owned_constraint = owned_constraint if owned_constraint is not None else []
        self.__owned_enumeration = owned_enumeration if owned_enumeration is not None else []
        self.__owned_flow = owned_flow if owned_flow is not None else []
        self.__owned_interface = owned_interface if owned_interface is not None else []
        self.__owned_item = owned_item if owned_item is not None else []
        self.__owned_metadata = owned_metadata if owned_metadata is not None else []
        self.__owned_occurrence = owned_occurrence if owned_occurrence is not None else []
        self.__owned_part = owned_part if owned_part is not None else []
        self.__owned_port = owned_port if owned_port is not None else []
        self.__owned_reference = owned_reference if owned_reference is not None else []
        self.__owned_rendering = owned_rendering if owned_rendering is not None else []
        self.__owned_requirement = owned_requirement if owned_requirement is not None else []
        self.__owned_state = owned_state if owned_state is not None else []
        self.__owned_transition = owned_transition if owned_transition is not None else []
        self.__owned_usage = owned_usage if owned_usage is not None else []
        self.__owned_use_case = owned_use_case if owned_use_case is not None else []
        self.__owned_verification_case = owned_verification_case if owned_verification_case is not None else []
        self.__owned_view = owned_view if owned_view is not None else []
        self.__owned_viewpoint = owned_viewpoint if owned_viewpoint is not None else []
        self.__owned_subclassification = owned_subclassification if owned_subclassification is not None else []
        self.__variant = variant if variant is not None else []
        self.__variant_membership = variant_membership if variant_membership is not None else []

    @property
    def is_variation(self):
        return self.__is_variation

    @is_variation.setter
    def is_variation(self, value):
        self.__is_variation = value

    @property
    def owned_action(self):
        return self.__owned_action

    @owned_action.setter
    def owned_action(self, value):
        self.__owned_action = value

    @property
    def owned_part(self):
        return self.__owned_part

    @owned_part.setter
    def owned_part(self, value):
        self.__owned_part = value

    @property
    def owned_port(self):
        return self.__owned_port

    @owned_port.setter
    def owned_port(self, value):
        self.__owned_port = value

    @property
    def owned_requirement(self):
        return self.__owned_requirement

    @owned_requirement.setter
    def owned_requirement(self, value):
        self.__owned_requirement = value

    @property
    def owned_attribute(self):
        return self.__owned_attribute

    @owned_attribute.setter
    def owned_attribute(self, value):
        self.__owned_attribute = value

    @property
    def owned_usage(self):
        return self.__owned_usage

    @owned_usage.setter
    def owned_usage(self, value):
        self.__owned_usage = value

    @property
    def variant(self):
        return self.__variant

    @variant.setter
    def variant(self, value):
        self.__variant = value

    @property
    def variant_membership(self):
        return self.__variant_membership

    @variant_membership.setter
    def variant_membership(self, value):
        self.__variant_membership = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind('oslc_sysml', OSLC_SYSML)
        graph.bind('oslc_am', OSLC_AM)
        graph.bind('oslc', OSLC)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)

        graph.add((subject_uri, RDF.type, OSLC_AM.Resource))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Element))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Namespace))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Type))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Definition))

        if self.identifier:
            graph.add((subject_uri, DCTERMS.identifier, Literal(self.identifier)))
        if self.title:
            graph.add((subject_uri, DCTERMS.title, Literal(self.title)))
        if self.description:
            graph.add((subject_uri, DCTERMS.description, Literal(self.description)))

        self._add_element_properties_rdf_direct(graph, subject_uri)

        graph.add((subject_uri, OSLC_SYSML.isAbstract,
                   Literal(self.is_abstract, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isConjugated,
                   Literal(self.is_conjugated, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isSufficient,
                   Literal(self.is_sufficient, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isVariation,
                   Literal(self.__is_variation, datatype=XSD.boolean)))

        if self.multiplicity:
            graph.add((subject_uri, OSLC_SYSML.multiplicity, URIRef(self.multiplicity)))

        for f in self.feature:
            graph.add((subject_uri, OSLC_SYSML.feature, URIRef(f)))
        for f in self.directed_feature:
            graph.add((subject_uri, OSLC_SYSML.directedFeature, URIRef(f)))
        for f in self.owned_feature:
            graph.add((subject_uri, OSLC_SYSML.ownedFeature, URIRef(f)))
        for f in self.owned_specialization:
            graph.add((subject_uri, OSLC_SYSML.ownedSpecialization, URIRef(f)))

        for u in self.__owned_action:
            graph.add((subject_uri, OSLC_SYSML.ownedAction, URIRef(u)))
        for u in self.__owned_part:
            graph.add((subject_uri, OSLC_SYSML.ownedPart, URIRef(u)))
        for u in self.__owned_port:
            graph.add((subject_uri, OSLC_SYSML.ownedPort, URIRef(u)))
        for u in self.__owned_requirement:
            graph.add((subject_uri, OSLC_SYSML.ownedRequirement, URIRef(u)))
        for u in self.__owned_attribute:
            graph.add((subject_uri, OSLC_SYSML.ownedAttribute, URIRef(u)))
        for u in self.__owned_usage:
            graph.add((subject_uri, OSLC_SYSML.ownedUsage, URIRef(u)))
        for u in self.__variant:
            graph.add((subject_uri, OSLC_SYSML.variant, URIRef(u)))
        for u in self.__variant_membership:
            graph.add((subject_uri, OSLC_SYSML.variantMembership, URIRef(u)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Definition):
            setattr(self, '_AbstractResource__about', str(r))

            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.elementId):
                self.element_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.declaredName):
                self.declared_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.name):
                self.name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.qualifiedName):
                self.qualified_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.isAbstract):
                self.is_abstract = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isConjugated):
                self.is_conjugated = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isSufficient):
                self.is_sufficient = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isVariation):
                self.is_variation = o.value if isinstance(o, Literal) else False

            for o in g.objects(r, OSLC_SYSML.multiplicity):
                self.multiplicity = str(o)

            for o in g.objects(r, OSLC_SYSML.feature):
                self.feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.directedFeature):
                self.directed_feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedFeature):
                self.owned_feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedSpecialization):
                self.owned_specialization.append(str(o))

            for o in g.objects(r, OSLC_SYSML.ownedAction):
                self.owned_action.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedPart):
                self.owned_part.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedPort):
                self.owned_port.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedRequirement):
                self.owned_requirement.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedAttribute):
                self.owned_attribute.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedUsage):
                self.owned_usage.append(str(o))
            for o in g.objects(r, OSLC_SYSML.variant):
                self.variant.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_variation' in data:
            self.is_variation = data['is_variation']
        if 'owned_action' in data:
            vals = data['owned_action']
            self.owned_action = vals if isinstance(vals, list) else [vals]
        if 'owned_part' in data:
            vals = data['owned_part']
            self.owned_part = vals if isinstance(vals, list) else [vals]
        if 'owned_port' in data:
            vals = data['owned_port']
            self.owned_port = vals if isinstance(vals, list) else [vals]
        if 'owned_requirement' in data:
            vals = data['owned_requirement']
            self.owned_requirement = vals if isinstance(vals, list) else [vals]
        if 'owned_attribute' in data:
            vals = data['owned_attribute']
            self.owned_attribute = vals if isinstance(vals, list) else [vals]
        if 'owned_usage' in data:
            vals = data['owned_usage']
            self.owned_usage = vals if isinstance(vals, list) else [vals]


class SysMLUsage(SysMLType):

    def __init__(self, about=None, types=None, properties=None,
                 description=None, identifier=None, short_title=None,
                 title=None, contributor=None, creator=None, subject=None,
                 created=None, modified=None, type=None,
                 discussed_by=None, instance_shape=None,
                 service_provider=None, relation=None,
                 element_id=None, alias_ids=None,
                 declared_name=None, declared_short_name=None,
                 name=None, short_name=None, qualified_name=None,
                 is_implied_included=None, is_library_element=None,
                 owner=None, owning_namespace=None,
                 owning_membership=None, owning_relationship=None,
                 owned_element=None, owned_relationship=None,
                 owned_annotation=None,
                 documentation=None, textual_representation=None,
                 member=None, membership=None,
                 owned_member=None, owned_membership=None,
                 imported_membership=None, owned_import=None,
                 is_abstract=None, is_conjugated=None, is_sufficient=None,
                 multiplicity=None, feature=None, directed_feature=None,
                 end_feature=None, owned_feature=None, owned_end_feature=None,
                 owned_feature_membership=None, feature_membership=None,
                 inherited_feature=None, inherited_membership=None,
                 input=None, output=None,
                 owned_specialization=None, owned_conjugator=None,
                 owned_differencing=None, owned_disjoining=None,
                 owned_intersecting=None, owned_unioning=None,
                 is_reference=None, may_time_vary=None, portion_kind=None,
                 definition=None, owning_definition=None, owning_usage=None,
                 is_variation=None, variant=None, variant_membership=None,
                 nested_action=None, nested_allocation=None,
                 nested_analysis_case=None, nested_attribute=None,
                 nested_calculation=None, nested_case=None,
                 nested_concern=None, nested_connection=None,
                 nested_constraint=None, nested_enumeration=None,
                 nested_flow=None, nested_interface=None,
                 nested_item=None, nested_metadata=None,
                 nested_occurrence=None, nested_part=None,
                 nested_port=None, nested_reference=None,
                 nested_rendering=None, nested_requirement=None,
                 nested_state=None, nested_transition=None,
                 nested_usage=None, nested_use_case=None,
                 nested_verification_case=None, nested_view=None,
                 nested_viewpoint=None,
                 individual_definition=None):

        super().__init__(
            about, types, properties, description, identifier,
            short_title, title, contributor, creator, subject,
            created, modified, type, discussed_by, instance_shape,
            service_provider, relation,
            element_id, alias_ids, declared_name, declared_short_name,
            name, short_name, qualified_name,
            is_implied_included, is_library_element,
            owner, owning_namespace, owning_membership,
            owning_relationship, owned_element, owned_relationship,
            owned_annotation, documentation, textual_representation,
            member, membership, owned_member, owned_membership,
            imported_membership, owned_import,
            is_abstract, is_conjugated, is_sufficient,
            multiplicity, feature, directed_feature,
            end_feature, owned_feature, owned_end_feature,
            owned_feature_membership, feature_membership,
            inherited_feature, inherited_membership,
            input, output,
            owned_specialization, owned_conjugator,
            owned_differencing, owned_disjoining,
            owned_intersecting, owned_unioning,
        )

        self.__is_reference = is_reference if is_reference is not None else False
        self.__may_time_vary = may_time_vary if may_time_vary is not None else False
        self.__portion_kind = portion_kind if portion_kind is not None else None
        self.__definition = definition if definition is not None else []
        self.__owning_definition = owning_definition if owning_definition is not None else None
        self.__owning_usage = owning_usage if owning_usage is not None else None
        self.__is_variation = is_variation if is_variation is not None else False
        self.__variant = variant if variant is not None else []
        self.__variant_membership = variant_membership if variant_membership is not None else []
        self.__individual_definition = individual_definition if individual_definition is not None else None

        self.__nested_action = nested_action if nested_action is not None else []
        self.__nested_allocation = nested_allocation if nested_allocation is not None else []
        self.__nested_analysis_case = nested_analysis_case if nested_analysis_case is not None else []
        self.__nested_attribute = nested_attribute if nested_attribute is not None else []
        self.__nested_calculation = nested_calculation if nested_calculation is not None else []
        self.__nested_case = nested_case if nested_case is not None else []
        self.__nested_concern = nested_concern if nested_concern is not None else []
        self.__nested_connection = nested_connection if nested_connection is not None else []
        self.__nested_constraint = nested_constraint if nested_constraint is not None else []
        self.__nested_enumeration = nested_enumeration if nested_enumeration is not None else []
        self.__nested_flow = nested_flow if nested_flow is not None else []
        self.__nested_interface = nested_interface if nested_interface is not None else []
        self.__nested_item = nested_item if nested_item is not None else []
        self.__nested_metadata = nested_metadata if nested_metadata is not None else []
        self.__nested_occurrence = nested_occurrence if nested_occurrence is not None else []
        self.__nested_part = nested_part if nested_part is not None else []
        self.__nested_port = nested_port if nested_port is not None else []
        self.__nested_reference = nested_reference if nested_reference is not None else []
        self.__nested_rendering = nested_rendering if nested_rendering is not None else []
        self.__nested_requirement = nested_requirement if nested_requirement is not None else []
        self.__nested_state = nested_state if nested_state is not None else []
        self.__nested_transition = nested_transition if nested_transition is not None else []
        self.__nested_usage = nested_usage if nested_usage is not None else []
        self.__nested_use_case = nested_use_case if nested_use_case is not None else []
        self.__nested_verification_case = nested_verification_case if nested_verification_case is not None else []
        self.__nested_view = nested_view if nested_view is not None else []
        self.__nested_viewpoint = nested_viewpoint if nested_viewpoint is not None else []

    @property
    def is_reference(self):
        return self.__is_reference

    @is_reference.setter
    def is_reference(self, value):
        self.__is_reference = value

    @property
    def may_time_vary(self):
        return self.__may_time_vary

    @may_time_vary.setter
    def may_time_vary(self, value):
        self.__may_time_vary = value

    @property
    def portion_kind(self):
        return self.__portion_kind

    @portion_kind.setter
    def portion_kind(self, value):
        self.__portion_kind = value

    @property
    def definition(self):
        return self.__definition

    @definition.setter
    def definition(self, value):
        self.__definition = value

    @property
    def owning_definition(self):
        return self.__owning_definition

    @owning_definition.setter
    def owning_definition(self, value):
        self.__owning_definition = value

    @property
    def owning_usage(self):
        return self.__owning_usage

    @owning_usage.setter
    def owning_usage(self, value):
        self.__owning_usage = value

    @property
    def is_variation(self):
        return self.__is_variation

    @is_variation.setter
    def is_variation(self, value):
        self.__is_variation = value

    @property
    def variant(self):
        return self.__variant

    @variant.setter
    def variant(self, value):
        self.__variant = value

    @property
    def variant_membership(self):
        return self.__variant_membership

    @variant_membership.setter
    def variant_membership(self, value):
        self.__variant_membership = value

    @property
    def nested_part(self):
        return self.__nested_part

    @nested_part.setter
    def nested_part(self, value):
        self.__nested_part = value

    @property
    def nested_port(self):
        return self.__nested_port

    @nested_port.setter
    def nested_port(self, value):
        self.__nested_port = value

    @property
    def nested_requirement(self):
        return self.__nested_requirement

    @nested_requirement.setter
    def nested_requirement(self, value):
        self.__nested_requirement = value

    @property
    def nested_attribute(self):
        return self.__nested_attribute

    @nested_attribute.setter
    def nested_attribute(self, value):
        self.__nested_attribute = value

    @property
    def nested_action(self):
        return self.__nested_action

    @nested_action.setter
    def nested_action(self, value):
        self.__nested_action = value

    @property
    def nested_usage(self):
        return self.__nested_usage

    @nested_usage.setter
    def nested_usage(self, value):
        self.__nested_usage = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        graph.bind('oslc_sysml', OSLC_SYSML)
        graph.bind('oslc_am', OSLC_AM)
        graph.bind('oslc', OSLC)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)

        graph.add((subject_uri, RDF.type, OSLC_AM.Resource))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Element))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Namespace))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Type))
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Usage))

        if self.identifier:
            graph.add((subject_uri, DCTERMS.identifier, Literal(self.identifier)))
        if self.title:
            graph.add((subject_uri, DCTERMS.title, Literal(self.title)))
        if self.description:
            graph.add((subject_uri, DCTERMS.description, Literal(self.description)))

        self._add_element_properties_rdf_direct(graph, subject_uri)

        graph.add((subject_uri, OSLC_SYSML.isAbstract,
                   Literal(self.is_abstract, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isConjugated,
                   Literal(self.is_conjugated, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isSufficient,
                   Literal(self.is_sufficient, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isReference,
                   Literal(self.__is_reference, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.mayTimeVary,
                   Literal(self.__may_time_vary, datatype=XSD.boolean)))
        graph.add((subject_uri, OSLC_SYSML.isVariation,
                   Literal(self.__is_variation, datatype=XSD.boolean)))

        if self.__portion_kind:
            graph.add((subject_uri, OSLC_SYSML.portionKind, URIRef(self.__portion_kind)))

        if self.multiplicity:
            graph.add((subject_uri, OSLC_SYSML.multiplicity, URIRef(self.multiplicity)))

        for f in self.feature:
            graph.add((subject_uri, OSLC_SYSML.feature, URIRef(f)))
        for f in self.directed_feature:
            graph.add((subject_uri, OSLC_SYSML.directedFeature, URIRef(f)))
        for f in self.owned_feature:
            graph.add((subject_uri, OSLC_SYSML.ownedFeature, URIRef(f)))
        for f in self.owned_specialization:
            graph.add((subject_uri, OSLC_SYSML.ownedSpecialization, URIRef(f)))

        for d in self.__definition:
            graph.add((subject_uri, OSLC_SYSML.definition, URIRef(d)))
        if self.__owning_definition:
            graph.add((subject_uri, OSLC_SYSML.owningDefinition, URIRef(self.__owning_definition)))
        if self.__owning_usage:
            graph.add((subject_uri, OSLC_SYSML.owningUsage, URIRef(self.__owning_usage)))
        if self.__individual_definition:
            graph.add((subject_uri, OSLC_SYSML.individualDefinition, URIRef(self.__individual_definition)))

        for v in self.__variant:
            graph.add((subject_uri, OSLC_SYSML.variant, URIRef(v)))
        for v in self.__variant_membership:
            graph.add((subject_uri, OSLC_SYSML.variantMembership, URIRef(v)))

        for n in self.__nested_action:
            graph.add((subject_uri, OSLC_SYSML.nestedAction, URIRef(n)))
        for n in self.__nested_part:
            graph.add((subject_uri, OSLC_SYSML.nestedPart, URIRef(n)))
        for n in self.__nested_port:
            graph.add((subject_uri, OSLC_SYSML.nestedPort, URIRef(n)))
        for n in self.__nested_requirement:
            graph.add((subject_uri, OSLC_SYSML.nestedRequirement, URIRef(n)))
        for n in self.__nested_attribute:
            graph.add((subject_uri, OSLC_SYSML.nestedAttribute, URIRef(n)))
        for n in self.__nested_usage:
            graph.add((subject_uri, OSLC_SYSML.nestedUsage, URIRef(n)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Usage):
            setattr(self, '_AbstractResource__about', str(r))

            for o in g.objects(r, DCTERMS.identifier):
                self.identifier = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.title):
                self.title = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, DCTERMS.description):
                self.description = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.elementId):
                self.element_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.declaredName):
                self.declared_name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.name):
                self.name = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.qualifiedName):
                self.qualified_name = o.value if isinstance(o, Literal) else str(o)

            for o in g.objects(r, OSLC_SYSML.isAbstract):
                self.is_abstract = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isConjugated):
                self.is_conjugated = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isSufficient):
                self.is_sufficient = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isReference):
                self.is_reference = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.mayTimeVary):
                self.may_time_vary = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.isVariation):
                self.is_variation = o.value if isinstance(o, Literal) else False

            for o in g.objects(r, OSLC_SYSML.portionKind):
                self.portion_kind = str(o)
            for o in g.objects(r, OSLC_SYSML.multiplicity):
                self.multiplicity = str(o)

            for o in g.objects(r, OSLC_SYSML.feature):
                self.feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.directedFeature):
                self.directed_feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedFeature):
                self.owned_feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedSpecialization):
                self.owned_specialization.append(str(o))

            for o in g.objects(r, OSLC_SYSML.definition):
                self.definition.append(str(o))
            for o in g.objects(r, OSLC_SYSML.owningDefinition):
                self.owning_definition = str(o)
            for o in g.objects(r, OSLC_SYSML.owningUsage):
                self.owning_usage = str(o)

            for o in g.objects(r, OSLC_SYSML.variant):
                self.variant.append(str(o))

            for o in g.objects(r, OSLC_SYSML.nestedAction):
                self.nested_action.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedPart):
                self.nested_part.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedPort):
                self.nested_port.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedRequirement):
                self.nested_requirement.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedAttribute):
                self.nested_attribute.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedUsage):
                self.nested_usage.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_reference' in data:
            self.is_reference = data['is_reference']
        if 'may_time_vary' in data:
            self.may_time_vary = data['may_time_vary']
        if 'portion_kind' in data:
            self.portion_kind = data['portion_kind']
        if 'definition' in data:
            self.definition = data['definition'] if isinstance(data['definition'], list) else [data['definition']]
        if 'owning_definition' in data:
            self.owning_definition = data['owning_definition']
        if 'is_variation' in data:
            self.is_variation = data['is_variation']
        if 'nested_part' in data:
            self.nested_part = data['nested_part'] if isinstance(data['nested_part'], list) else [data['nested_part']]
        if 'nested_port' in data:
            self.nested_port = data['nested_port'] if isinstance(data['nested_port'], list) else [data['nested_port']]
        if 'nested_requirement' in data:
            vals = data['nested_requirement']
            self.nested_requirement = vals if isinstance(vals, list) else [vals]
        if 'nested_attribute' in data:
            vals = data['nested_attribute']
            self.nested_attribute = vals if isinstance(vals, list) else [vals]
        if 'nested_action' in data:
            vals = data['nested_action']
            self.nested_action = vals if isinstance(vals, list) else [vals]
        if 'nested_usage' in data:
            vals = data['nested_usage']
            self.nested_usage = vals if isinstance(vals, list) else [vals]


class SysMLItemDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        owned_occurrence = kwargs.pop('owned_occurrence', None)
        owned_item = kwargs.pop('owned_item', None)
        super().__init__(**kwargs)

        self.__owned_occurrence = owned_occurrence if owned_occurrence is not None else []
        self.__owned_item = owned_item if owned_item is not None else []

    @property
    def owned_occurrence(self):
        return self.__owned_occurrence

    @owned_occurrence.setter
    def owned_occurrence(self, value):
        self.__owned_occurrence = value

    @property
    def owned_item(self):
        return self.__owned_item

    @owned_item.setter
    def owned_item(self, value):
        self.__owned_item = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ItemDefinition))

        for u in self.__owned_occurrence:
            graph.add((subject_uri, OSLC_SYSML.ownedOccurrence, URIRef(u)))
        for u in self.__owned_item:
            graph.add((subject_uri, OSLC_SYSML.ownedItem, URIRef(u)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ItemDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.ownedOccurrence):
                self.owned_occurrence.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedItem):
                self.owned_item.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'owned_occurrence' in data:
            vals = data['owned_occurrence']
            self.owned_occurrence = vals if isinstance(vals, list) else [vals]
        if 'owned_item' in data:
            vals = data['owned_item']
            self.owned_item = vals if isinstance(vals, list) else [vals]


class SysMLItemUsage(SysMLUsage):

    def __init__(self, **kwargs):
        occurrence_definition = kwargs.pop('occurrence_definition', None)
        super().__init__(**kwargs)

        self.__occurrence_definition = occurrence_definition if occurrence_definition is not None else None

    @property
    def occurrence_definition(self):
        return self.__occurrence_definition

    @occurrence_definition.setter
    def occurrence_definition(self, value):
        self.__occurrence_definition = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ItemUsage))

        if self.__occurrence_definition:
            graph.add((subject_uri, OSLC_SYSML.occurrenceDefinition,
                       URIRef(self.__occurrence_definition)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ItemUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.occurrenceDefinition):
                self.occurrence_definition = str(o)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'occurrence_definition' in data:
            self.occurrence_definition = data['occurrence_definition']


class SysMLPartDefinition(SysMLItemDefinition):

    def __init__(self, **kwargs):
        owned_connection = kwargs.pop('owned_connection', None)
        owned_interface = kwargs.pop('owned_interface', None)
        super().__init__(**kwargs)

        self.__owned_connection = owned_connection if owned_connection is not None else []
        self.__owned_interface = owned_interface if owned_interface is not None else []

    @property
    def owned_connection(self):
        return self.__owned_connection

    @owned_connection.setter
    def owned_connection(self, value):
        self.__owned_connection = value

    @property
    def owned_interface(self):
        return self.__owned_interface

    @owned_interface.setter
    def owned_interface(self, value):
        self.__owned_interface = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.PartDefinition))

        for u in self.__owned_connection:
            graph.add((subject_uri, OSLC_SYSML.ownedConnection, URIRef(u)))
        for u in self.__owned_interface:
            graph.add((subject_uri, OSLC_SYSML.ownedInterface, URIRef(u)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.PartDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.ownedConnection):
                self.owned_connection.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedInterface):
                self.owned_interface.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'owned_connection' in data:
            vals = data['owned_connection']
            self.owned_connection = vals if isinstance(vals, list) else [vals]
        if 'owned_interface' in data:
            vals = data['owned_interface']
            self.owned_interface = vals if isinstance(vals, list) else [vals]


class SysMLPartUsage(SysMLItemUsage):

    def __init__(self, **kwargs):
        nested_item = kwargs.pop('nested_item', None)
        nested_connection = kwargs.pop('nested_connection', None)
        nested_interface = kwargs.pop('nested_interface', None)
        super().__init__(**kwargs)

        self.__nested_item = nested_item if nested_item is not None else []
        self.__nested_connection = nested_connection if nested_connection is not None else []
        self.__nested_interface = nested_interface if nested_interface is not None else []

    @property
    def nested_item(self):
        return self.__nested_item

    @nested_item.setter
    def nested_item(self, value):
        self.__nested_item = value

    @property
    def nested_connection(self):
        return self.__nested_connection

    @nested_connection.setter
    def nested_connection(self, value):
        self.__nested_connection = value

    @property
    def nested_interface(self):
        return self.__nested_interface

    @nested_interface.setter
    def nested_interface(self, value):
        self.__nested_interface = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.PartUsage))

        for n in self.__nested_item:
            graph.add((subject_uri, OSLC_SYSML.nestedItem, URIRef(n)))
        for n in self.__nested_connection:
            graph.add((subject_uri, OSLC_SYSML.nestedConnection, URIRef(n)))
        for n in self.__nested_interface:
            graph.add((subject_uri, OSLC_SYSML.nestedInterface, URIRef(n)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.PartUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.nestedItem):
                self.nested_item.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedConnection):
                self.nested_connection.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedInterface):
                self.nested_interface.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'nested_item' in data:
            vals = data['nested_item']
            self.nested_item = vals if isinstance(vals, list) else [vals]
        if 'nested_connection' in data:
            vals = data['nested_connection']
            self.nested_connection = vals if isinstance(vals, list) else [vals]
        if 'nested_interface' in data:
            vals = data['nested_interface']
            self.nested_interface = vals if isinstance(vals, list) else [vals]


class SysMLPortDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        conjugated_port_definition = kwargs.pop('conjugated_port_definition', None)
        super().__init__(**kwargs)

        self.__conjugated_port_definition = conjugated_port_definition

    @property
    def conjugated_port_definition(self):
        return self.__conjugated_port_definition

    @conjugated_port_definition.setter
    def conjugated_port_definition(self, value):
        self.__conjugated_port_definition = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.PortDefinition))

        if self.__conjugated_port_definition:
            graph.add((subject_uri, OSLC_SYSML.conjugatedPortDefinition,
                       URIRef(self.__conjugated_port_definition)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.PortDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.conjugatedPortDefinition):
                self.conjugated_port_definition = str(o)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'conjugated_port_definition' in data:
            self.conjugated_port_definition = data['conjugated_port_definition']


class SysMLPortUsage(SysMLUsage):

    def __init__(self, **kwargs):
        conjugated_port_definition = kwargs.pop('conjugated_port_definition', None)
        nested_connection = kwargs.pop('nested_connection', None)
        nested_interface = kwargs.pop('nested_interface', None)
        super().__init__(**kwargs)

        self.__conjugated_port_definition = conjugated_port_definition
        self.__nested_connection = nested_connection if nested_connection is not None else []
        self.__nested_interface = nested_interface if nested_interface is not None else []

    @property
    def conjugated_port_definition(self):
        return self.__conjugated_port_definition

    @conjugated_port_definition.setter
    def conjugated_port_definition(self, value):
        self.__conjugated_port_definition = value

    @property
    def nested_connection(self):
        return self.__nested_connection

    @nested_connection.setter
    def nested_connection(self, value):
        self.__nested_connection = value

    @property
    def nested_interface(self):
        return self.__nested_interface

    @nested_interface.setter
    def nested_interface(self, value):
        self.__nested_interface = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.PortUsage))

        if self.__conjugated_port_definition:
            graph.add((subject_uri, OSLC_SYSML.conjugatedPortDefinition,
                       URIRef(self.__conjugated_port_definition)))
        for n in self.__nested_connection:
            graph.add((subject_uri, OSLC_SYSML.nestedConnection, URIRef(n)))
        for n in self.__nested_interface:
            graph.add((subject_uri, OSLC_SYSML.nestedInterface, URIRef(n)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.PortUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.conjugatedPortDefinition):
                self.conjugated_port_definition = str(o)
            for o in g.objects(r, OSLC_SYSML.nestedConnection):
                self.nested_connection.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedInterface):
                self.nested_interface.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'conjugated_port_definition' in data:
            self.conjugated_port_definition = data['conjugated_port_definition']
        if 'nested_connection' in data:
            vals = data['nested_connection']
            self.nested_connection = vals if isinstance(vals, list) else [vals]
        if 'nested_interface' in data:
            vals = data['nested_interface']
            self.nested_interface = vals if isinstance(vals, list) else [vals]


class SysMLRequirementDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        req_id = kwargs.pop('req_id', None)
        text = kwargs.pop('text', None)
        assumed_constraint = kwargs.pop('assumed_constraint', None)
        required_constraint = kwargs.pop('required_constraint', None)
        framed_concern = kwargs.pop('framed_concern', None)
        referenced_concern = kwargs.pop('referenced_concern', None)
        owned_stakeholder_parameter = kwargs.pop('owned_stakeholder_parameter', None)
        owned_subject_parameter = kwargs.pop('owned_subject_parameter', None)
        owned_actor_parameter = kwargs.pop('owned_actor_parameter', None)
        owned_objective_requirement = kwargs.pop('owned_objective_requirement', None)
        stakeholder_parameter = kwargs.pop('stakeholder_parameter', None)
        subject_parameter = kwargs.pop('subject_parameter', None)
        actor_parameter = kwargs.pop('actor_parameter', None)
        referenced_rendering = kwargs.pop('referenced_rendering', None)
        viewpoint_stakeholder = kwargs.pop('viewpoint_stakeholder', None)
        owned_concern = kwargs.pop('owned_concern', None)
        owned_viewpoint = kwargs.pop('owned_viewpoint', None)
        super().__init__(**kwargs)

        self.__req_id = req_id if req_id is not None else ''
        self.__text = text if text is not None else []
        self.__assumed_constraint = assumed_constraint if assumed_constraint is not None else []
        self.__required_constraint = required_constraint if required_constraint is not None else []
        self.__framed_concern = framed_concern if framed_concern is not None else []
        self.__referenced_concern = referenced_concern if referenced_concern is not None else []
        self.__owned_stakeholder_parameter = (
            owned_stakeholder_parameter if owned_stakeholder_parameter is not None else [])
        self.__owned_subject_parameter = (
            owned_subject_parameter if owned_subject_parameter is not None else [])
        self.__owned_actor_parameter = (
            owned_actor_parameter if owned_actor_parameter is not None else [])
        self.__owned_objective_requirement = owned_objective_requirement
        self.__stakeholder_parameter = (
            stakeholder_parameter if stakeholder_parameter is not None else [])
        self.__subject_parameter = subject_parameter if subject_parameter is not None else []
        self.__actor_parameter = actor_parameter if actor_parameter is not None else []
        self.__referenced_rendering = referenced_rendering
        self.__viewpoint_stakeholder = (
            viewpoint_stakeholder if viewpoint_stakeholder is not None else [])
        self.__owned_concern = owned_concern if owned_concern is not None else []
        self.__owned_viewpoint = owned_viewpoint if owned_viewpoint is not None else []

    @property
    def req_id(self):
        return self.__req_id

    @req_id.setter
    def req_id(self, value):
        self.__req_id = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def assumed_constraint(self):
        return self.__assumed_constraint

    @assumed_constraint.setter
    def assumed_constraint(self, value):
        self.__assumed_constraint = value

    @property
    def required_constraint(self):
        return self.__required_constraint

    @required_constraint.setter
    def required_constraint(self, value):
        self.__required_constraint = value

    @property
    def framed_concern(self):
        return self.__framed_concern

    @framed_concern.setter
    def framed_concern(self, value):
        self.__framed_concern = value

    @property
    def referenced_concern(self):
        return self.__referenced_concern

    @referenced_concern.setter
    def referenced_concern(self, value):
        self.__referenced_concern = value

    @property
    def owned_stakeholder_parameter(self):
        return self.__owned_stakeholder_parameter

    @owned_stakeholder_parameter.setter
    def owned_stakeholder_parameter(self, value):
        self.__owned_stakeholder_parameter = value

    @property
    def owned_subject_parameter(self):
        return self.__owned_subject_parameter

    @owned_subject_parameter.setter
    def owned_subject_parameter(self, value):
        self.__owned_subject_parameter = value

    @property
    def owned_actor_parameter(self):
        return self.__owned_actor_parameter

    @owned_actor_parameter.setter
    def owned_actor_parameter(self, value):
        self.__owned_actor_parameter = value

    @property
    def owned_objective_requirement(self):
        return self.__owned_objective_requirement

    @owned_objective_requirement.setter
    def owned_objective_requirement(self, value):
        self.__owned_objective_requirement = value

    @property
    def stakeholder_parameter(self):
        return self.__stakeholder_parameter

    @stakeholder_parameter.setter
    def stakeholder_parameter(self, value):
        self.__stakeholder_parameter = value

    @property
    def subject_parameter(self):
        return self.__subject_parameter

    @subject_parameter.setter
    def subject_parameter(self, value):
        self.__subject_parameter = value

    @property
    def actor_parameter(self):
        return self.__actor_parameter

    @actor_parameter.setter
    def actor_parameter(self, value):
        self.__actor_parameter = value

    @property
    def referenced_rendering(self):
        return self.__referenced_rendering

    @referenced_rendering.setter
    def referenced_rendering(self, value):
        self.__referenced_rendering = value

    @property
    def viewpoint_stakeholder(self):
        return self.__viewpoint_stakeholder

    @viewpoint_stakeholder.setter
    def viewpoint_stakeholder(self, value):
        self.__viewpoint_stakeholder = value

    @property
    def owned_concern(self):
        return self.__owned_concern

    @owned_concern.setter
    def owned_concern(self, value):
        self.__owned_concern = value

    @property
    def owned_viewpoint(self):
        return self.__owned_viewpoint

    @owned_viewpoint.setter
    def owned_viewpoint(self, value):
        self.__owned_viewpoint = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.RequirementDefinition))

        if self.__req_id:
            graph.add((subject_uri, OSLC_SYSML.reqId, Literal(self.__req_id)))
        for t in self.__text:
            graph.add((subject_uri, OSLC_SYSML.text, Literal(t)))
        for c in self.__assumed_constraint:
            graph.add((subject_uri, OSLC_SYSML.assumedConstraint, URIRef(c)))
        for c in self.__required_constraint:
            graph.add((subject_uri, OSLC_SYSML.requiredConstraint, URIRef(c)))
        for c in self.__framed_concern:
            graph.add((subject_uri, OSLC_SYSML.framedConcern, URIRef(c)))
        for c in self.__referenced_concern:
            graph.add((subject_uri, OSLC_SYSML.referencedConcern, URIRef(c)))
        for p in self.__owned_stakeholder_parameter:
            graph.add((subject_uri, OSLC_SYSML.ownedStakeholderParameter, URIRef(p)))
        for p in self.__owned_subject_parameter:
            graph.add((subject_uri, OSLC_SYSML.ownedSubjectParameter, URIRef(p)))
        for p in self.__owned_actor_parameter:
            graph.add((subject_uri, OSLC_SYSML.ownedActorParameter, URIRef(p)))
        if self.__owned_objective_requirement:
            graph.add((subject_uri, OSLC_SYSML.ownedObjectiveRequirement,
                       URIRef(self.__owned_objective_requirement)))
        for p in self.__stakeholder_parameter:
            graph.add((subject_uri, OSLC_SYSML.stakeholderParameter, URIRef(p)))
        for p in self.__subject_parameter:
            graph.add((subject_uri, OSLC_SYSML.subjectParameter, URIRef(p)))
        for p in self.__actor_parameter:
            graph.add((subject_uri, OSLC_SYSML.actorParameter, URIRef(p)))
        if self.__referenced_rendering:
            graph.add((subject_uri, OSLC_SYSML.referencedRendering,
                       URIRef(self.__referenced_rendering)))
        for v in self.__viewpoint_stakeholder:
            graph.add((subject_uri, OSLC_SYSML.viewpointStakeholder, URIRef(v)))
        for c in self.__owned_concern:
            graph.add((subject_uri, OSLC_SYSML.ownedConcern, URIRef(c)))
        for v in self.__owned_viewpoint:
            graph.add((subject_uri, OSLC_SYSML.ownedViewpoint, URIRef(v)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.RequirementDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.reqId):
                self.req_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.text):
                self.text.append(o.value if isinstance(o, Literal) else str(o))
            for o in g.objects(r, OSLC_SYSML.assumedConstraint):
                self.assumed_constraint.append(str(o))
            for o in g.objects(r, OSLC_SYSML.requiredConstraint):
                self.required_constraint.append(str(o))
            for o in g.objects(r, OSLC_SYSML.framedConcern):
                self.framed_concern.append(str(o))
            for o in g.objects(r, OSLC_SYSML.referencedConcern):
                self.referenced_concern.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedStakeholderParameter):
                self.owned_stakeholder_parameter.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedSubjectParameter):
                self.owned_subject_parameter.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedActorParameter):
                self.owned_actor_parameter.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedObjectiveRequirement):
                self.owned_objective_requirement = str(o)
            for o in g.objects(r, OSLC_SYSML.stakeholderParameter):
                self.stakeholder_parameter.append(str(o))
            for o in g.objects(r, OSLC_SYSML.subjectParameter):
                self.subject_parameter.append(str(o))
            for o in g.objects(r, OSLC_SYSML.actorParameter):
                self.actor_parameter.append(str(o))
            for o in g.objects(r, OSLC_SYSML.referencedRendering):
                self.referenced_rendering = str(o)
            for o in g.objects(r, OSLC_SYSML.viewpointStakeholder):
                self.viewpoint_stakeholder.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedConcern):
                self.owned_concern.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedViewpoint):
                self.owned_viewpoint.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'req_id' in data:
            self.req_id = data['req_id']
        if 'text' in data:
            self.text = data['text'] if isinstance(data['text'], list) else [data['text']]
        if 'assumed_constraint' in data:
            vals = data['assumed_constraint']
            self.assumed_constraint = vals if isinstance(vals, list) else [vals]
        if 'required_constraint' in data:
            vals = data['required_constraint']
            self.required_constraint = vals if isinstance(vals, list) else [vals]
        if 'framed_concern' in data:
            vals = data['framed_concern']
            self.framed_concern = vals if isinstance(vals, list) else [vals]
        if 'referenced_concern' in data:
            vals = data['referenced_concern']
            self.referenced_concern = vals if isinstance(vals, list) else [vals]
        if 'owned_concern' in data:
            vals = data['owned_concern']
            self.owned_concern = vals if isinstance(vals, list) else [vals]
        if 'owned_viewpoint' in data:
            vals = data['owned_viewpoint']
            self.owned_viewpoint = vals if isinstance(vals, list) else [vals]
        if 'owned_objective_requirement' in data:
            self.owned_objective_requirement = data['owned_objective_requirement']
        if 'referenced_rendering' in data:
            self.referenced_rendering = data['referenced_rendering']


class SysMLRequirementUsage(SysMLUsage):

    def __init__(self, **kwargs):
        req_id = kwargs.pop('req_id', None)
        text = kwargs.pop('text', None)
        assumed_constraint = kwargs.pop('assumed_constraint', None)
        required_constraint = kwargs.pop('required_constraint', None)
        framed_concern = kwargs.pop('framed_concern', None)
        referenced_concern = kwargs.pop('referenced_concern', None)
        referenced_rendering = kwargs.pop('referenced_rendering', None)
        satisfied_requirement = kwargs.pop('satisfied_requirement', None)
        satisfied_viewpoint = kwargs.pop('satisfied_viewpoint', None)
        verified_requirement = kwargs.pop('verified_requirement', None)
        super().__init__(**kwargs)

        self.__req_id = req_id if req_id is not None else ''
        self.__text = text if text is not None else []
        self.__assumed_constraint = assumed_constraint if assumed_constraint is not None else []
        self.__required_constraint = required_constraint if required_constraint is not None else []
        self.__framed_concern = framed_concern if framed_concern is not None else []
        self.__referenced_concern = referenced_concern if referenced_concern is not None else []
        self.__referenced_rendering = referenced_rendering
        self.__satisfied_requirement = (
            satisfied_requirement if satisfied_requirement is not None else [])
        self.__satisfied_viewpoint = (
            satisfied_viewpoint if satisfied_viewpoint is not None else [])
        self.__verified_requirement = (
            verified_requirement if verified_requirement is not None else [])

    @property
    def req_id(self):
        return self.__req_id

    @req_id.setter
    def req_id(self, value):
        self.__req_id = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def assumed_constraint(self):
        return self.__assumed_constraint

    @assumed_constraint.setter
    def assumed_constraint(self, value):
        self.__assumed_constraint = value

    @property
    def required_constraint(self):
        return self.__required_constraint

    @required_constraint.setter
    def required_constraint(self, value):
        self.__required_constraint = value

    @property
    def framed_concern(self):
        return self.__framed_concern

    @framed_concern.setter
    def framed_concern(self, value):
        self.__framed_concern = value

    @property
    def referenced_concern(self):
        return self.__referenced_concern

    @referenced_concern.setter
    def referenced_concern(self, value):
        self.__referenced_concern = value

    @property
    def referenced_rendering(self):
        return self.__referenced_rendering

    @referenced_rendering.setter
    def referenced_rendering(self, value):
        self.__referenced_rendering = value

    @property
    def satisfied_requirement(self):
        return self.__satisfied_requirement

    @satisfied_requirement.setter
    def satisfied_requirement(self, value):
        self.__satisfied_requirement = value

    @property
    def satisfied_viewpoint(self):
        return self.__satisfied_viewpoint

    @satisfied_viewpoint.setter
    def satisfied_viewpoint(self, value):
        self.__satisfied_viewpoint = value

    @property
    def verified_requirement(self):
        return self.__verified_requirement

    @verified_requirement.setter
    def verified_requirement(self, value):
        self.__verified_requirement = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.RequirementUsage))

        if self.__req_id:
            graph.add((subject_uri, OSLC_SYSML.reqId, Literal(self.__req_id)))
        for t in self.__text:
            graph.add((subject_uri, OSLC_SYSML.text, Literal(t)))
        for c in self.__assumed_constraint:
            graph.add((subject_uri, OSLC_SYSML.assumedConstraint, URIRef(c)))
        for c in self.__required_constraint:
            graph.add((subject_uri, OSLC_SYSML.requiredConstraint, URIRef(c)))
        for c in self.__framed_concern:
            graph.add((subject_uri, OSLC_SYSML.framedConcern, URIRef(c)))
        for c in self.__referenced_concern:
            graph.add((subject_uri, OSLC_SYSML.referencedConcern, URIRef(c)))
        if self.__referenced_rendering:
            graph.add((subject_uri, OSLC_SYSML.referencedRendering,
                       URIRef(self.__referenced_rendering)))
        for s in self.__satisfied_requirement:
            graph.add((subject_uri, OSLC_SYSML.satisfiedRequirement, URIRef(s)))
        for s in self.__satisfied_viewpoint:
            graph.add((subject_uri, OSLC_SYSML.satisfiedViewpoint, URIRef(s)))
        for v in self.__verified_requirement:
            graph.add((subject_uri, OSLC_SYSML.verifiedRequirement, URIRef(v)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.RequirementUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.reqId):
                self.req_id = o.value if isinstance(o, Literal) else str(o)
            for o in g.objects(r, OSLC_SYSML.text):
                self.text.append(o.value if isinstance(o, Literal) else str(o))
            for o in g.objects(r, OSLC_SYSML.assumedConstraint):
                self.assumed_constraint.append(str(o))
            for o in g.objects(r, OSLC_SYSML.requiredConstraint):
                self.required_constraint.append(str(o))
            for o in g.objects(r, OSLC_SYSML.framedConcern):
                self.framed_concern.append(str(o))
            for o in g.objects(r, OSLC_SYSML.referencedConcern):
                self.referenced_concern.append(str(o))
            for o in g.objects(r, OSLC_SYSML.referencedRendering):
                self.referenced_rendering = str(o)
            for o in g.objects(r, OSLC_SYSML.satisfiedRequirement):
                self.satisfied_requirement.append(str(o))
            for o in g.objects(r, OSLC_SYSML.satisfiedViewpoint):
                self.satisfied_viewpoint.append(str(o))
            for o in g.objects(r, OSLC_SYSML.verifiedRequirement):
                self.verified_requirement.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'req_id' in data:
            self.req_id = data['req_id']
        if 'text' in data:
            self.text = data['text'] if isinstance(data['text'], list) else [data['text']]
        if 'assumed_constraint' in data:
            vals = data['assumed_constraint']
            self.assumed_constraint = vals if isinstance(vals, list) else [vals]
        if 'required_constraint' in data:
            vals = data['required_constraint']
            self.required_constraint = vals if isinstance(vals, list) else [vals]
        if 'framed_concern' in data:
            vals = data['framed_concern']
            self.framed_concern = vals if isinstance(vals, list) else [vals]
        if 'referenced_concern' in data:
            vals = data['referenced_concern']
            self.referenced_concern = vals if isinstance(vals, list) else [vals]
        if 'referenced_rendering' in data:
            self.referenced_rendering = data['referenced_rendering']
        if 'satisfied_requirement' in data:
            vals = data['satisfied_requirement']
            self.satisfied_requirement = vals if isinstance(vals, list) else [vals]
        if 'satisfied_viewpoint' in data:
            vals = data['satisfied_viewpoint']
            self.satisfied_viewpoint = vals if isinstance(vals, list) else [vals]
        if 'verified_requirement' in data:
            vals = data['verified_requirement']
            self.verified_requirement = vals if isinstance(vals, list) else [vals]


class SysMLConcernDefinition(SysMLRequirementDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConcernDefinition))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConcernDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLConcernUsage(SysMLRequirementUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConcernUsage))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConcernUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLActionDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        action = kwargs.pop('action', None)
        behavior = kwargs.pop('behavior', None)
        step = kwargs.pop('step', None)
        parameter = kwargs.pop('parameter', None)
        owned_constraint = kwargs.pop('owned_constraint', None)
        owned_requirement = kwargs.pop('owned_requirement', None)
        owned_concern = kwargs.pop('owned_concern', None)
        owned_rendering = kwargs.pop('owned_rendering', None)
        owned_calculation = kwargs.pop('owned_calculation', None)
        owned_case = kwargs.pop('owned_case', None)
        owned_analysis_case = kwargs.pop('owned_analysis_case', None)
        owned_verification_case = kwargs.pop('owned_verification_case', None)
        owned_use_case = kwargs.pop('owned_use_case', None)
        owned_transition = kwargs.pop('owned_transition', None)
        owned_state = kwargs.pop('owned_state', None)
        super().__init__(**kwargs)

        self.__action = action if action is not None else []
        self.__behavior = behavior if behavior is not None else []
        self.__step = step if step is not None else []
        self.__parameter = parameter if parameter is not None else []
        self.__owned_constraint = owned_constraint if owned_constraint is not None else []
        self.__owned_requirement = owned_requirement if owned_requirement is not None else []
        self.__owned_concern = owned_concern if owned_concern is not None else []
        self.__owned_rendering = owned_rendering if owned_rendering is not None else []
        self.__owned_calculation = owned_calculation if owned_calculation is not None else []
        self.__owned_case = owned_case if owned_case is not None else []
        self.__owned_analysis_case = owned_analysis_case if owned_analysis_case is not None else []
        self.__owned_verification_case = (
            owned_verification_case if owned_verification_case is not None else [])
        self.__owned_use_case = owned_use_case if owned_use_case is not None else []
        self.__owned_transition = owned_transition if owned_transition is not None else []
        self.__owned_state = owned_state if owned_state is not None else []

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        self.__action = value

    @property
    def behavior(self):
        return self.__behavior

    @behavior.setter
    def behavior(self, value):
        self.__behavior = value

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, value):
        self.__step = value

    @property
    def parameter(self):
        return self.__parameter

    @parameter.setter
    def parameter(self, value):
        self.__parameter = value

    @property
    def owned_constraint(self):
        return self.__owned_constraint

    @owned_constraint.setter
    def owned_constraint(self, value):
        self.__owned_constraint = value

    @property
    def owned_requirement(self):
        return self.__owned_requirement

    @owned_requirement.setter
    def owned_requirement(self, value):
        self.__owned_requirement = value

    @property
    def owned_concern(self):
        return self.__owned_concern

    @owned_concern.setter
    def owned_concern(self, value):
        self.__owned_concern = value

    @property
    def owned_rendering(self):
        return self.__owned_rendering

    @owned_rendering.setter
    def owned_rendering(self, value):
        self.__owned_rendering = value

    @property
    def owned_calculation(self):
        return self.__owned_calculation

    @owned_calculation.setter
    def owned_calculation(self, value):
        self.__owned_calculation = value

    @property
    def owned_case(self):
        return self.__owned_case

    @owned_case.setter
    def owned_case(self, value):
        self.__owned_case = value

    @property
    def owned_analysis_case(self):
        return self.__owned_analysis_case

    @owned_analysis_case.setter
    def owned_analysis_case(self, value):
        self.__owned_analysis_case = value

    @property
    def owned_verification_case(self):
        return self.__owned_verification_case

    @owned_verification_case.setter
    def owned_verification_case(self, value):
        self.__owned_verification_case = value

    @property
    def owned_use_case(self):
        return self.__owned_use_case

    @owned_use_case.setter
    def owned_use_case(self, value):
        self.__owned_use_case = value

    @property
    def owned_transition(self):
        return self.__owned_transition

    @owned_transition.setter
    def owned_transition(self, value):
        self.__owned_transition = value

    @property
    def owned_state(self):
        return self.__owned_state

    @owned_state.setter
    def owned_state(self, value):
        self.__owned_state = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ActionDefinition))

        for a in self.__action:
            graph.add((subject_uri, OSLC_SYSML.action, URIRef(a)))
        for b in self.__behavior:
            graph.add((subject_uri, OSLC_SYSML.behavior, URIRef(b)))
        for s in self.__step:
            graph.add((subject_uri, OSLC_SYSML.step, URIRef(s)))
        for p in self.__parameter:
            graph.add((subject_uri, OSLC_SYSML.parameter, URIRef(p)))
        for c in self.__owned_constraint:
            graph.add((subject_uri, OSLC_SYSML.ownedConstraint, URIRef(c)))
        for r in self.__owned_requirement:
            graph.add((subject_uri, OSLC_SYSML.ownedRequirement, URIRef(r)))
        for c in self.__owned_concern:
            graph.add((subject_uri, OSLC_SYSML.ownedConcern, URIRef(c)))
        for r in self.__owned_rendering:
            graph.add((subject_uri, OSLC_SYSML.ownedRendering, URIRef(r)))
        for c in self.__owned_calculation:
            graph.add((subject_uri, OSLC_SYSML.ownedCalculation, URIRef(c)))
        for c in self.__owned_case:
            graph.add((subject_uri, OSLC_SYSML.ownedCase, URIRef(c)))
        for a in self.__owned_analysis_case:
            graph.add((subject_uri, OSLC_SYSML.ownedAnalysisCase, URIRef(a)))
        for v in self.__owned_verification_case:
            graph.add((subject_uri, OSLC_SYSML.ownedVerificationCase, URIRef(v)))
        for u in self.__owned_use_case:
            graph.add((subject_uri, OSLC_SYSML.ownedUseCase, URIRef(u)))
        for t in self.__owned_transition:
            graph.add((subject_uri, OSLC_SYSML.ownedTransition, URIRef(t)))
        for s in self.__owned_state:
            graph.add((subject_uri, OSLC_SYSML.ownedState, URIRef(s)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ActionDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.action):
                self.action.append(str(o))
            for o in g.objects(r, OSLC_SYSML.behavior):
                self.behavior.append(str(o))
            for o in g.objects(r, OSLC_SYSML.step):
                self.step.append(str(o))
            for o in g.objects(r, OSLC_SYSML.parameter):
                self.parameter.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedConstraint):
                self.owned_constraint.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedRequirement):
                self.owned_requirement.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedConcern):
                self.owned_concern.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedRendering):
                self.owned_rendering.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedCalculation):
                self.owned_calculation.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedCase):
                self.owned_case.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedAnalysisCase):
                self.owned_analysis_case.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedVerificationCase):
                self.owned_verification_case.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedUseCase):
                self.owned_use_case.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedTransition):
                self.owned_transition.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedState):
                self.owned_state.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'action' in data:
            vals = data['action']
            self.action = vals if isinstance(vals, list) else [vals]
        if 'behavior' in data:
            vals = data['behavior']
            self.behavior = vals if isinstance(vals, list) else [vals]
        if 'step' in data:
            vals = data['step']
            self.step = vals if isinstance(vals, list) else [vals]
        if 'parameter' in data:
            vals = data['parameter']
            self.parameter = vals if isinstance(vals, list) else [vals]
        if 'owned_constraint' in data:
            vals = data['owned_constraint']
            self.owned_constraint = vals if isinstance(vals, list) else [vals]
        if 'owned_requirement' in data:
            vals = data['owned_requirement']
            self.owned_requirement = vals if isinstance(vals, list) else [vals]
        if 'owned_concern' in data:
            vals = data['owned_concern']
            self.owned_concern = vals if isinstance(vals, list) else [vals]
        if 'owned_rendering' in data:
            vals = data['owned_rendering']
            self.owned_rendering = vals if isinstance(vals, list) else [vals]
        if 'owned_calculation' in data:
            vals = data['owned_calculation']
            self.owned_calculation = vals if isinstance(vals, list) else [vals]
        if 'owned_case' in data:
            vals = data['owned_case']
            self.owned_case = vals if isinstance(vals, list) else [vals]
        if 'owned_analysis_case' in data:
            vals = data['owned_analysis_case']
            self.owned_analysis_case = vals if isinstance(vals, list) else [vals]
        if 'owned_verification_case' in data:
            vals = data['owned_verification_case']
            self.owned_verification_case = vals if isinstance(vals, list) else [vals]
        if 'owned_use_case' in data:
            vals = data['owned_use_case']
            self.owned_use_case = vals if isinstance(vals, list) else [vals]
        if 'owned_transition' in data:
            vals = data['owned_transition']
            self.owned_transition = vals if isinstance(vals, list) else [vals]
        if 'owned_state' in data:
            vals = data['owned_state']
            self.owned_state = vals if isinstance(vals, list) else [vals]


class SysMLActionUsage(SysMLUsage):

    def __init__(self, **kwargs):
        action_definition = kwargs.pop('action_definition', None)
        behavior = kwargs.pop('behavior', None)
        nested_calculation = kwargs.pop('nested_calculation', None)
        nested_case = kwargs.pop('nested_case', None)
        nested_concern = kwargs.pop('nested_concern', None)
        nested_constraint = kwargs.pop('nested_constraint', None)
        nested_enumeration = kwargs.pop('nested_enumeration', None)
        nested_flow = kwargs.pop('nested_flow', None)
        nested_interface = kwargs.pop('nested_interface', None)
        nested_item = kwargs.pop('nested_item', None)
        nested_metadata = kwargs.pop('nested_metadata', None)
        nested_occurrence = kwargs.pop('nested_occurrence', None)
        nested_reference = kwargs.pop('nested_reference', None)
        nested_rendering = kwargs.pop('nested_rendering', None)
        nested_requirement = kwargs.pop('nested_requirement', None)
        nested_state = kwargs.pop('nested_state', None)
        nested_transition = kwargs.pop('nested_transition', None)
        nested_use_case = kwargs.pop('nested_use_case', None)
        nested_verification_case = kwargs.pop('nested_verification_case', None)
        nested_view = kwargs.pop('nested_view', None)
        nested_viewpoint = kwargs.pop('nested_viewpoint', None)
        super().__init__(**kwargs)

        self.__action_definition = action_definition
        self.__behavior = behavior if behavior is not None else []
        self.__nested_calculation = nested_calculation if nested_calculation is not None else []
        self.__nested_case = nested_case if nested_case is not None else []
        self.__nested_concern = nested_concern if nested_concern is not None else []
        self.__nested_constraint = nested_constraint if nested_constraint is not None else []
        self.__nested_enumeration = nested_enumeration if nested_enumeration is not None else []
        self.__nested_flow = nested_flow if nested_flow is not None else []
        self.__nested_interface = nested_interface if nested_interface is not None else []
        self.__nested_item = nested_item if nested_item is not None else []
        self.__nested_metadata = nested_metadata if nested_metadata is not None else []
        self.__nested_occurrence = nested_occurrence if nested_occurrence is not None else []
        self.__nested_reference = nested_reference if nested_reference is not None else []
        self.__nested_rendering = nested_rendering if nested_rendering is not None else []
        self.__nested_requirement = nested_requirement if nested_requirement is not None else []
        self.__nested_state = nested_state if nested_state is not None else []
        self.__nested_transition = nested_transition if nested_transition is not None else []
        self.__nested_use_case = nested_use_case if nested_use_case is not None else []
        self.__nested_verification_case = (
            nested_verification_case if nested_verification_case is not None else [])
        self.__nested_view = nested_view if nested_view is not None else []
        self.__nested_viewpoint = nested_viewpoint if nested_viewpoint is not None else []

    @property
    def action_definition(self):
        return self.__action_definition

    @action_definition.setter
    def action_definition(self, value):
        self.__action_definition = value

    @property
    def behavior(self):
        return self.__behavior

    @behavior.setter
    def behavior(self, value):
        self.__behavior = value

    @property
    def nested_calculation(self):
        return self.__nested_calculation

    @nested_calculation.setter
    def nested_calculation(self, value):
        self.__nested_calculation = value

    @property
    def nested_case(self):
        return self.__nested_case

    @nested_case.setter
    def nested_case(self, value):
        self.__nested_case = value

    @property
    def nested_concern(self):
        return self.__nested_concern

    @nested_concern.setter
    def nested_concern(self, value):
        self.__nested_concern = value

    @property
    def nested_constraint(self):
        return self.__nested_constraint

    @nested_constraint.setter
    def nested_constraint(self, value):
        self.__nested_constraint = value

    @property
    def nested_enumeration(self):
        return self.__nested_enumeration

    @nested_enumeration.setter
    def nested_enumeration(self, value):
        self.__nested_enumeration = value

    @property
    def nested_flow(self):
        return self.__nested_flow

    @nested_flow.setter
    def nested_flow(self, value):
        self.__nested_flow = value

    @property
    def nested_interface(self):
        return self.__nested_interface

    @nested_interface.setter
    def nested_interface(self, value):
        self.__nested_interface = value

    @property
    def nested_item(self):
        return self.__nested_item

    @nested_item.setter
    def nested_item(self, value):
        self.__nested_item = value

    @property
    def nested_metadata(self):
        return self.__nested_metadata

    @nested_metadata.setter
    def nested_metadata(self, value):
        self.__nested_metadata = value

    @property
    def nested_occurrence(self):
        return self.__nested_occurrence

    @nested_occurrence.setter
    def nested_occurrence(self, value):
        self.__nested_occurrence = value

    @property
    def nested_reference(self):
        return self.__nested_reference

    @nested_reference.setter
    def nested_reference(self, value):
        self.__nested_reference = value

    @property
    def nested_rendering(self):
        return self.__nested_rendering

    @nested_rendering.setter
    def nested_rendering(self, value):
        self.__nested_rendering = value

    @property
    def nested_requirement(self):
        return self.__nested_requirement

    @nested_requirement.setter
    def nested_requirement(self, value):
        self.__nested_requirement = value

    @property
    def nested_state(self):
        return self.__nested_state

    @nested_state.setter
    def nested_state(self, value):
        self.__nested_state = value

    @property
    def nested_transition(self):
        return self.__nested_transition

    @nested_transition.setter
    def nested_transition(self, value):
        self.__nested_transition = value

    @property
    def nested_use_case(self):
        return self.__nested_use_case

    @nested_use_case.setter
    def nested_use_case(self, value):
        self.__nested_use_case = value

    @property
    def nested_verification_case(self):
        return self.__nested_verification_case

    @nested_verification_case.setter
    def nested_verification_case(self, value):
        self.__nested_verification_case = value

    @property
    def nested_view(self):
        return self.__nested_view

    @nested_view.setter
    def nested_view(self, value):
        self.__nested_view = value

    @property
    def nested_viewpoint(self):
        return self.__nested_viewpoint

    @nested_viewpoint.setter
    def nested_viewpoint(self, value):
        self.__nested_viewpoint = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ActionUsage))

        if self.__action_definition:
            graph.add((subject_uri, OSLC_SYSML.actionDefinition,
                       URIRef(self.__action_definition)))
        for b in self.__behavior:
            graph.add((subject_uri, OSLC_SYSML.behavior, URIRef(b)))
        for n in self.__nested_calculation:
            graph.add((subject_uri, OSLC_SYSML.nestedCalculation, URIRef(n)))
        for n in self.__nested_case:
            graph.add((subject_uri, OSLC_SYSML.nestedCase, URIRef(n)))
        for n in self.__nested_concern:
            graph.add((subject_uri, OSLC_SYSML.nestedConcern, URIRef(n)))
        for n in self.__nested_constraint:
            graph.add((subject_uri, OSLC_SYSML.nestedConstraint, URIRef(n)))
        for n in self.__nested_enumeration:
            graph.add((subject_uri, OSLC_SYSML.nestedEnumeration, URIRef(n)))
        for n in self.__nested_flow:
            graph.add((subject_uri, OSLC_SYSML.nestedFlow, URIRef(n)))
        for n in self.__nested_interface:
            graph.add((subject_uri, OSLC_SYSML.nestedInterface, URIRef(n)))
        for n in self.__nested_item:
            graph.add((subject_uri, OSLC_SYSML.nestedItem, URIRef(n)))
        for n in self.__nested_metadata:
            graph.add((subject_uri, OSLC_SYSML.nestedMetadata, URIRef(n)))
        for n in self.__nested_occurrence:
            graph.add((subject_uri, OSLC_SYSML.nestedOccurrence, URIRef(n)))
        for n in self.__nested_reference:
            graph.add((subject_uri, OSLC_SYSML.nestedReference, URIRef(n)))
        for n in self.__nested_rendering:
            graph.add((subject_uri, OSLC_SYSML.nestedRendering, URIRef(n)))
        for n in self.__nested_requirement:
            graph.add((subject_uri, OSLC_SYSML.nestedRequirement, URIRef(n)))
        for n in self.__nested_state:
            graph.add((subject_uri, OSLC_SYSML.nestedState, URIRef(n)))
        for n in self.__nested_transition:
            graph.add((subject_uri, OSLC_SYSML.nestedTransition, URIRef(n)))
        for n in self.__nested_use_case:
            graph.add((subject_uri, OSLC_SYSML.nestedUseCase, URIRef(n)))
        for n in self.__nested_verification_case:
            graph.add((subject_uri, OSLC_SYSML.nestedVerificationCase, URIRef(n)))
        for n in self.__nested_view:
            graph.add((subject_uri, OSLC_SYSML.nestedView, URIRef(n)))
        for n in self.__nested_viewpoint:
            graph.add((subject_uri, OSLC_SYSML.nestedViewpoint, URIRef(n)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ActionUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.actionDefinition):
                self.action_definition = str(o)
            for o in g.objects(r, OSLC_SYSML.behavior):
                self.behavior.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedCalculation):
                self.nested_calculation.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedCase):
                self.nested_case.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedConcern):
                self.nested_concern.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedConstraint):
                self.nested_constraint.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedEnumeration):
                self.nested_enumeration.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedFlow):
                self.nested_flow.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedInterface):
                self.nested_interface.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedItem):
                self.nested_item.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedMetadata):
                self.nested_metadata.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedOccurrence):
                self.nested_occurrence.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedReference):
                self.nested_reference.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedRendering):
                self.nested_rendering.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedRequirement):
                self.nested_requirement.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedState):
                self.nested_state.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedTransition):
                self.nested_transition.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedUseCase):
                self.nested_use_case.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedVerificationCase):
                self.nested_verification_case.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedView):
                self.nested_view.append(str(o))
            for o in g.objects(r, OSLC_SYSML.nestedViewpoint):
                self.nested_viewpoint.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'action_definition' in data:
            self.action_definition = data['action_definition']
        if 'behavior' in data:
            vals = data['behavior']
            self.behavior = vals if isinstance(vals, list) else [vals]
        if 'nested_calculation' in data:
            vals = data['nested_calculation']
            self.nested_calculation = vals if isinstance(vals, list) else [vals]
        if 'nested_case' in data:
            vals = data['nested_case']
            self.nested_case = vals if isinstance(vals, list) else [vals]
        if 'nested_concern' in data:
            vals = data['nested_concern']
            self.nested_concern = vals if isinstance(vals, list) else [vals]
        if 'nested_constraint' in data:
            vals = data['nested_constraint']
            self.nested_constraint = vals if isinstance(vals, list) else [vals]
        if 'nested_enumeration' in data:
            vals = data['nested_enumeration']
            self.nested_enumeration = vals if isinstance(vals, list) else [vals]
        if 'nested_flow' in data:
            vals = data['nested_flow']
            self.nested_flow = vals if isinstance(vals, list) else [vals]
        if 'nested_interface' in data:
            vals = data['nested_interface']
            self.nested_interface = vals if isinstance(vals, list) else [vals]
        if 'nested_item' in data:
            vals = data['nested_item']
            self.nested_item = vals if isinstance(vals, list) else [vals]
        if 'nested_metadata' in data:
            vals = data['nested_metadata']
            self.nested_metadata = vals if isinstance(vals, list) else [vals]
        if 'nested_occurrence' in data:
            vals = data['nested_occurrence']
            self.nested_occurrence = vals if isinstance(vals, list) else [vals]
        if 'nested_reference' in data:
            vals = data['nested_reference']
            self.nested_reference = vals if isinstance(vals, list) else [vals]
        if 'nested_rendering' in data:
            vals = data['nested_rendering']
            self.nested_rendering = vals if isinstance(vals, list) else [vals]
        if 'nested_requirement' in data:
            vals = data['nested_requirement']
            self.nested_requirement = vals if isinstance(vals, list) else [vals]
        if 'nested_state' in data:
            vals = data['nested_state']
            self.nested_state = vals if isinstance(vals, list) else [vals]
        if 'nested_transition' in data:
            vals = data['nested_transition']
            self.nested_transition = vals if isinstance(vals, list) else [vals]
        if 'nested_use_case' in data:
            vals = data['nested_use_case']
            self.nested_use_case = vals if isinstance(vals, list) else [vals]
        if 'nested_verification_case' in data:
            vals = data['nested_verification_case']
            self.nested_verification_case = vals if isinstance(vals, list) else [vals]
        if 'nested_view' in data:
            vals = data['nested_view']
            self.nested_view = vals if isinstance(vals, list) else [vals]
        if 'nested_viewpoint' in data:
            vals = data['nested_viewpoint']
            self.nested_viewpoint = vals if isinstance(vals, list) else [vals]


class SysMLStateDefinition(SysMLActionDefinition):

    def __init__(self, **kwargs):
        state = kwargs.pop('state', None)
        entry_action = kwargs.pop('entry_action', None)
        do_action = kwargs.pop('do_action', None)
        exit_action = kwargs.pop('exit_action', None)
        super().__init__(**kwargs)

        self.__state = state if state is not None else []
        self.__entry_action = entry_action
        self.__do_action = do_action
        self.__exit_action = exit_action

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def entry_action(self):
        return self.__entry_action

    @entry_action.setter
    def entry_action(self, value):
        self.__entry_action = value

    @property
    def do_action(self):
        return self.__do_action

    @do_action.setter
    def do_action(self, value):
        self.__do_action = value

    @property
    def exit_action(self):
        return self.__exit_action

    @exit_action.setter
    def exit_action(self, value):
        self.__exit_action = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.StateDefinition))

        for s in self.__state:
            graph.add((subject_uri, OSLC_SYSML.state, URIRef(s)))
        if self.__entry_action:
            graph.add((subject_uri, OSLC_SYSML.entryAction, URIRef(self.__entry_action)))
        if self.__do_action:
            graph.add((subject_uri, OSLC_SYSML.doAction, URIRef(self.__do_action)))
        if self.__exit_action:
            graph.add((subject_uri, OSLC_SYSML.exitAction, URIRef(self.__exit_action)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.StateDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.state):
                self.state.append(str(o))
            for o in g.objects(r, OSLC_SYSML.entryAction):
                self.entry_action = str(o)
            for o in g.objects(r, OSLC_SYSML.doAction):
                self.do_action = str(o)
            for o in g.objects(r, OSLC_SYSML.exitAction):
                self.exit_action = str(o)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'state' in data:
            vals = data['state']
            self.state = vals if isinstance(vals, list) else [vals]
        if 'entry_action' in data:
            self.entry_action = data['entry_action']
        if 'do_action' in data:
            self.do_action = data['do_action']
        if 'exit_action' in data:
            self.exit_action = data['exit_action']


class SysMLStateUsage(SysMLActionUsage):

    def __init__(self, **kwargs):
        state_definition = kwargs.pop('state_definition', None)
        super().__init__(**kwargs)

        self.__state_definition = state_definition

    @property
    def state_definition(self):
        return self.__state_definition

    @state_definition.setter
    def state_definition(self, value):
        self.__state_definition = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.StateUsage))

        if self.__state_definition:
            graph.add((subject_uri, OSLC_SYSML.stateDefinition,
                       URIRef(self.__state_definition)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.StateUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.stateDefinition):
                self.state_definition = str(o)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'state_definition' in data:
            self.state_definition = data['state_definition']


class SysMLConstraintDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        is_negated = kwargs.pop('is_negated', None)
        super().__init__(**kwargs)

        self.__is_negated = is_negated if is_negated is not None else False

    @property
    def is_negated(self):
        return self.__is_negated

    @is_negated.setter
    def is_negated(self, value):
        self.__is_negated = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConstraintDefinition))
        graph.add((subject_uri, OSLC_SYSML.isNegated,
                   Literal(self.__is_negated, datatype=XSD.boolean)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConstraintDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.isNegated):
                self.is_negated = o.value if isinstance(o, Literal) else False

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_negated' in data:
            self.is_negated = data['is_negated']


class SysMLConstraintUsage(SysMLUsage):

    def __init__(self, **kwargs):
        is_negated = kwargs.pop('is_negated', None)
        constraint_definition = kwargs.pop('constraint_definition', None)
        super().__init__(**kwargs)

        self.__is_negated = is_negated if is_negated is not None else False
        self.__constraint_definition = constraint_definition

    @property
    def is_negated(self):
        return self.__is_negated

    @is_negated.setter
    def is_negated(self, value):
        self.__is_negated = value

    @property
    def constraint_definition(self):
        return self.__constraint_definition

    @constraint_definition.setter
    def constraint_definition(self, value):
        self.__constraint_definition = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConstraintUsage))
        graph.add((subject_uri, OSLC_SYSML.isNegated,
                   Literal(self.__is_negated, datatype=XSD.boolean)))

        if self.__constraint_definition:
            graph.add((subject_uri, OSLC_SYSML.definition,
                       URIRef(self.__constraint_definition)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConstraintUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.isNegated):
                self.is_negated = o.value if isinstance(o, Literal) else False
            for o in g.objects(r, OSLC_SYSML.definition):
                self.constraint_definition = str(o)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_negated' in data:
            self.is_negated = data['is_negated']
        if 'constraint_definition' in data:
            self.constraint_definition = data['constraint_definition']


class SysMLViewDefinition(SysMLPartDefinition):

    def __init__(self, **kwargs):
        view_condition = kwargs.pop('view_condition', None)
        view_rendering = kwargs.pop('view_rendering', None)
        exposed_element = kwargs.pop('exposed_element', None)
        super().__init__(**kwargs)

        self.__view_condition = view_condition
        self.__view_rendering = view_rendering
        self.__exposed_element = exposed_element if exposed_element is not None else []

    @property
    def view_condition(self):
        return self.__view_condition

    @view_condition.setter
    def view_condition(self, value):
        self.__view_condition = value

    @property
    def view_rendering(self):
        return self.__view_rendering

    @view_rendering.setter
    def view_rendering(self, value):
        self.__view_rendering = value

    @property
    def exposed_element(self):
        return self.__exposed_element

    @exposed_element.setter
    def exposed_element(self, value):
        self.__exposed_element = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ViewDefinition))

        if self.__view_condition:
            graph.add((subject_uri, OSLC_SYSML.viewCondition,
                       URIRef(self.__view_condition)))
        if self.__view_rendering:
            graph.add((subject_uri, OSLC_SYSML.viewRendering,
                       URIRef(self.__view_rendering)))
        for elem in self.__exposed_element:
            graph.add((subject_uri, OSLC_SYSML.exposedElement, URIRef(elem)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ViewDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.viewCondition):
                self.view_condition = str(o)
            for o in g.objects(r, OSLC_SYSML.viewRendering):
                self.view_rendering = str(o)
            for o in g.objects(r, OSLC_SYSML.exposedElement):
                self.exposed_element.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'view_condition' in data:
            self.view_condition = data['view_condition']
        if 'view_rendering' in data:
            self.view_rendering = data['view_rendering']
        if 'exposed_element' in data:
            vals = data['exposed_element']
            self.exposed_element = vals if isinstance(vals, list) else [vals]


class SysMLViewUsage(SysMLPartUsage):

    def __init__(self, **kwargs):
        view_definition = kwargs.pop('view_definition', None)
        view_condition = kwargs.pop('view_condition', None)
        view_rendering = kwargs.pop('view_rendering', None)
        exposed_element = kwargs.pop('exposed_element', None)
        satisfied_viewpoint = kwargs.pop('satisfied_viewpoint', None)
        super().__init__(**kwargs)

        self.__view_definition = view_definition
        self.__view_condition = view_condition
        self.__view_rendering = view_rendering
        self.__exposed_element = exposed_element if exposed_element is not None else []
        self.__satisfied_viewpoint = satisfied_viewpoint if satisfied_viewpoint is not None else []

    @property
    def view_definition(self):
        return self.__view_definition

    @view_definition.setter
    def view_definition(self, value):
        self.__view_definition = value

    @property
    def view_condition(self):
        return self.__view_condition

    @view_condition.setter
    def view_condition(self, value):
        self.__view_condition = value

    @property
    def view_rendering(self):
        return self.__view_rendering

    @view_rendering.setter
    def view_rendering(self, value):
        self.__view_rendering = value

    @property
    def exposed_element(self):
        return self.__exposed_element

    @exposed_element.setter
    def exposed_element(self, value):
        self.__exposed_element = value

    @property
    def satisfied_viewpoint(self):
        return self.__satisfied_viewpoint

    @satisfied_viewpoint.setter
    def satisfied_viewpoint(self, value):
        self.__satisfied_viewpoint = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ViewUsage))

        if self.__view_definition:
            graph.add((subject_uri, OSLC_SYSML.viewDefinition,
                       URIRef(self.__view_definition)))
        if self.__view_condition:
            graph.add((subject_uri, OSLC_SYSML.viewCondition,
                       URIRef(self.__view_condition)))
        if self.__view_rendering:
            graph.add((subject_uri, OSLC_SYSML.viewRendering,
                       URIRef(self.__view_rendering)))
        for elem in self.__exposed_element:
            graph.add((subject_uri, OSLC_SYSML.exposedElement, URIRef(elem)))
        for vp in self.__satisfied_viewpoint:
            graph.add((subject_uri, OSLC_SYSML.satisfiedViewpoint, URIRef(vp)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ViewUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.viewDefinition):
                self.view_definition = str(o)
            for o in g.objects(r, OSLC_SYSML.viewCondition):
                self.view_condition = str(o)
            for o in g.objects(r, OSLC_SYSML.viewRendering):
                self.view_rendering = str(o)
            for o in g.objects(r, OSLC_SYSML.exposedElement):
                self.exposed_element.append(str(o))
            for o in g.objects(r, OSLC_SYSML.satisfiedViewpoint):
                self.satisfied_viewpoint.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'view_definition' in data:
            self.view_definition = data['view_definition']
        if 'view_condition' in data:
            self.view_condition = data['view_condition']
        if 'view_rendering' in data:
            self.view_rendering = data['view_rendering']
        if 'exposed_element' in data:
            vals = data['exposed_element']
            self.exposed_element = vals if isinstance(vals, list) else [vals]
        if 'satisfied_viewpoint' in data:
            vals = data['satisfied_viewpoint']
            self.satisfied_viewpoint = vals if isinstance(vals, list) else [vals]


class SysMLViewpointDefinition(SysMLRequirementDefinition):

    def __init__(self, **kwargs):
        viewpoint_stakeholder = kwargs.pop('viewpoint_stakeholder', None)
        satisfied_viewpoint = kwargs.pop('satisfied_viewpoint', None)
        super().__init__(**kwargs)

        self.__viewpoint_stakeholder = viewpoint_stakeholder if viewpoint_stakeholder is not None else []
        self.__satisfied_viewpoint = satisfied_viewpoint if satisfied_viewpoint is not None else []

    @property
    def viewpoint_stakeholder(self):
        return self.__viewpoint_stakeholder

    @viewpoint_stakeholder.setter
    def viewpoint_stakeholder(self, value):
        self.__viewpoint_stakeholder = value

    @property
    def satisfied_viewpoint(self):
        return self.__satisfied_viewpoint

    @satisfied_viewpoint.setter
    def satisfied_viewpoint(self, value):
        self.__satisfied_viewpoint = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ViewpointDefinition))

        for sh in self.__viewpoint_stakeholder:
            graph.add((subject_uri, OSLC_SYSML.viewpointStakeholder, URIRef(sh)))
        for vp in self.__satisfied_viewpoint:
            graph.add((subject_uri, OSLC_SYSML.satisfiedViewpoint, URIRef(vp)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ViewpointDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.viewpointStakeholder):
                self.viewpoint_stakeholder.append(str(o))
            for o in g.objects(r, OSLC_SYSML.satisfiedViewpoint):
                self.satisfied_viewpoint.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'viewpoint_stakeholder' in data:
            vals = data['viewpoint_stakeholder']
            self.viewpoint_stakeholder = vals if isinstance(vals, list) else [vals]
        if 'satisfied_viewpoint' in data:
            vals = data['satisfied_viewpoint']
            self.satisfied_viewpoint = vals if isinstance(vals, list) else [vals]


class SysMLFeature(SysMLType):

    def __init__(self, **kwargs):
        is_abstract = kwargs.pop('is_abstract', None)
        is_composite = kwargs.pop('is_composite', None)
        is_derived = kwargs.pop('is_derived', None)
        is_end = kwargs.pop('is_end', None)
        is_ordered = kwargs.pop('is_ordered', None)
        is_portion = kwargs.pop('is_portion', None)
        is_read_only = kwargs.pop('is_read_only', None)
        is_unique = kwargs.pop('is_unique', None)
        direction = kwargs.pop('direction', None)
        super().__init__(**kwargs)
        self.__is_abstract = is_abstract
        self.__is_composite = is_composite
        self.__is_derived = is_derived
        self.__is_end = is_end
        self.__is_ordered = is_ordered
        self.__is_portion = is_portion
        self.__is_read_only = is_read_only
        self.__is_unique = is_unique
        self.__direction = direction

    @property
    def is_abstract(self):
        return self.__is_abstract

    @is_abstract.setter
    def is_abstract(self, value):
        self.__is_abstract = value

    @property
    def is_composite(self):
        return self.__is_composite

    @is_composite.setter
    def is_composite(self, value):
        self.__is_composite = value

    @property
    def is_derived(self):
        return self.__is_derived

    @is_derived.setter
    def is_derived(self, value):
        self.__is_derived = value

    @property
    def is_end(self):
        return self.__is_end

    @is_end.setter
    def is_end(self, value):
        self.__is_end = value

    @property
    def is_ordered(self):
        return self.__is_ordered

    @is_ordered.setter
    def is_ordered(self, value):
        self.__is_ordered = value

    @property
    def is_portion(self):
        return self.__is_portion

    @is_portion.setter
    def is_portion(self, value):
        self.__is_portion = value

    @property
    def is_read_only(self):
        return self.__is_read_only

    @is_read_only.setter
    def is_read_only(self, value):
        self.__is_read_only = value

    @property
    def is_unique(self):
        return self.__is_unique

    @is_unique.setter
    def is_unique(self, value):
        self.__is_unique = value

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Feature))

        if self.__is_abstract is not None:
            graph.add((subject_uri, OSLC_SYSML.isAbstract,
                       Literal(self.__is_abstract, datatype=XSD.boolean)))
        if self.__is_composite is not None:
            graph.add((subject_uri, OSLC_SYSML.isComposite,
                       Literal(self.__is_composite, datatype=XSD.boolean)))
        if self.__is_derived is not None:
            graph.add((subject_uri, OSLC_SYSML.isDerived,
                       Literal(self.__is_derived, datatype=XSD.boolean)))
        if self.__is_end is not None:
            graph.add((subject_uri, OSLC_SYSML.isEnd,
                       Literal(self.__is_end, datatype=XSD.boolean)))
        if self.__is_ordered is not None:
            graph.add((subject_uri, OSLC_SYSML.isOrdered,
                       Literal(self.__is_ordered, datatype=XSD.boolean)))
        if self.__is_portion is not None:
            graph.add((subject_uri, OSLC_SYSML.isPortion,
                       Literal(self.__is_portion, datatype=XSD.boolean)))
        if self.__is_read_only is not None:
            graph.add((subject_uri, OSLC_SYSML.isReadOnly,
                       Literal(self.__is_read_only, datatype=XSD.boolean)))
        if self.__is_unique is not None:
            graph.add((subject_uri, OSLC_SYSML.isUnique,
                       Literal(self.__is_unique, datatype=XSD.boolean)))
        if self.__direction:
            graph.add((subject_uri, OSLC_SYSML.direction,
                       OSLC_SYSML[self.__direction]))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Feature):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.isAbstract):
                self.is_abstract = o.value
            for o in g.objects(r, OSLC_SYSML.isComposite):
                self.is_composite = o.value
            for o in g.objects(r, OSLC_SYSML.isDerived):
                self.is_derived = o.value
            for o in g.objects(r, OSLC_SYSML.isEnd):
                self.is_end = o.value
            for o in g.objects(r, OSLC_SYSML.isOrdered):
                self.is_ordered = o.value
            for o in g.objects(r, OSLC_SYSML.isPortion):
                self.is_portion = o.value
            for o in g.objects(r, OSLC_SYSML.isReadOnly):
                self.is_read_only = o.value
            for o in g.objects(r, OSLC_SYSML.isUnique):
                self.is_unique = o.value
            for o in g.objects(r, OSLC_SYSML.direction):
                self.direction = str(o).split('#')[-1]

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_abstract' in data:
            self.is_abstract = data['is_abstract']
        if 'is_composite' in data:
            self.is_composite = data['is_composite']
        if 'is_derived' in data:
            self.is_derived = data['is_derived']
        if 'is_end' in data:
            self.is_end = data['is_end']
        if 'is_ordered' in data:
            self.is_ordered = data['is_ordered']
        if 'is_portion' in data:
            self.is_portion = data['is_portion']
        if 'is_read_only' in data:
            self.is_read_only = data['is_read_only']
        if 'is_unique' in data:
            self.is_unique = data['is_unique']
        if 'direction' in data:
            self.direction = data['direction']


class SysMLClassifier(SysMLType):

    def __init__(self, **kwargs):
        is_abstract = kwargs.pop('is_abstract', None)
        is_conjugated = kwargs.pop('is_conjugated', None)
        is_sufficient = kwargs.pop('is_sufficient', None)
        is_variation = kwargs.pop('is_variation', None)
        multiplicity = kwargs.pop('multiplicity', None)
        owned_feature = kwargs.pop('owned_feature', None)
        feature = kwargs.pop('feature', None)
        owned_specialization = kwargs.pop('owned_specialization', None)
        owned_conjugator = kwargs.pop('owned_conjugator', None)
        owned_membership = kwargs.pop('owned_membership', None)
        owned_import = kwargs.pop('owned_import', None)
        super().__init__(**kwargs)
        self.__is_abstract = is_abstract
        self.__is_conjugated = is_conjugated
        self.__is_sufficient = is_sufficient
        self.__is_variation = is_variation
        self.__multiplicity = multiplicity
        self.__owned_feature = owned_feature if owned_feature is not None else []
        self.__feature = feature if feature is not None else []
        self.__owned_specialization = owned_specialization if owned_specialization is not None else []
        self.__owned_conjugator = owned_conjugator
        self.__owned_membership = owned_membership if owned_membership is not None else []
        self.__owned_import = owned_import if owned_import is not None else []

    @property
    def is_abstract(self):
        return self.__is_abstract

    @is_abstract.setter
    def is_abstract(self, value):
        self.__is_abstract = value

    @property
    def is_conjugated(self):
        return self.__is_conjugated

    @is_conjugated.setter
    def is_conjugated(self, value):
        self.__is_conjugated = value

    @property
    def is_sufficient(self):
        return self.__is_sufficient

    @is_sufficient.setter
    def is_sufficient(self, value):
        self.__is_sufficient = value

    @property
    def is_variation(self):
        return self.__is_variation

    @is_variation.setter
    def is_variation(self, value):
        self.__is_variation = value

    @property
    def multiplicity(self):
        return self.__multiplicity

    @multiplicity.setter
    def multiplicity(self, value):
        self.__multiplicity = value

    @property
    def owned_feature(self):
        return self.__owned_feature

    @owned_feature.setter
    def owned_feature(self, value):
        self.__owned_feature = value

    @property
    def feature(self):
        return self.__feature

    @feature.setter
    def feature(self, value):
        self.__feature = value

    @property
    def owned_specialization(self):
        return self.__owned_specialization

    @owned_specialization.setter
    def owned_specialization(self, value):
        self.__owned_specialization = value

    @property
    def owned_conjugator(self):
        return self.__owned_conjugator

    @owned_conjugator.setter
    def owned_conjugator(self, value):
        self.__owned_conjugator = value

    @property
    def owned_membership(self):
        return self.__owned_membership

    @owned_membership.setter
    def owned_membership(self, value):
        self.__owned_membership = value

    @property
    def owned_import(self):
        return self.__owned_import

    @owned_import.setter
    def owned_import(self, value):
        self.__owned_import = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Classifier))

        if self.__is_abstract is not None:
            graph.add((subject_uri, OSLC_SYSML.isAbstract,
                       Literal(self.__is_abstract, datatype=XSD.boolean)))
        if self.__is_conjugated is not None:
            graph.add((subject_uri, OSLC_SYSML.isConjugated,
                       Literal(self.__is_conjugated, datatype=XSD.boolean)))
        if self.__is_sufficient is not None:
            graph.add((subject_uri, OSLC_SYSML.isSufficient,
                       Literal(self.__is_sufficient, datatype=XSD.boolean)))
        if self.__is_variation is not None:
            graph.add((subject_uri, OSLC_SYSML.isVariation,
                       Literal(self.__is_variation, datatype=XSD.boolean)))
        if self.__multiplicity:
            graph.add((subject_uri, OSLC_SYSML.multiplicity,
                       URIRef(self.__multiplicity)))
        for f in self.__feature:
            graph.add((subject_uri, OSLC_SYSML.feature, URIRef(f)))
        for f in self.__owned_feature:
            graph.add((subject_uri, OSLC_SYSML.ownedFeature, URIRef(f)))
        for s in self.__owned_specialization:
            graph.add((subject_uri, OSLC_SYSML.ownedSpecialization, URIRef(s)))
        if self.__owned_conjugator:
            graph.add((subject_uri, OSLC_SYSML.ownedConjugator,
                       URIRef(self.__owned_conjugator)))
        for m in self.__owned_membership:
            graph.add((subject_uri, OSLC_SYSML.ownedMembership, URIRef(m)))
        for i in self.__owned_import:
            graph.add((subject_uri, OSLC_SYSML.ownedImport, URIRef(i)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Classifier):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.isAbstract):
                self.is_abstract = o.value
            for o in g.objects(r, OSLC_SYSML.isConjugated):
                self.is_conjugated = o.value
            for o in g.objects(r, OSLC_SYSML.isSufficient):
                self.is_sufficient = o.value
            for o in g.objects(r, OSLC_SYSML.isVariation):
                self.is_variation = o.value
            for o in g.objects(r, OSLC_SYSML.multiplicity):
                self.multiplicity = str(o)
            for o in g.objects(r, OSLC_SYSML.feature):
                self.feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedFeature):
                self.owned_feature.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedSpecialization):
                self.owned_specialization.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedConjugator):
                self.owned_conjugator = str(o)
            for o in g.objects(r, OSLC_SYSML.ownedMembership):
                self.owned_membership.append(str(o))
            for o in g.objects(r, OSLC_SYSML.ownedImport):
                self.owned_import.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_abstract' in data:
            self.is_abstract = data['is_abstract']
        if 'is_conjugated' in data:
            self.is_conjugated = data['is_conjugated']
        if 'is_sufficient' in data:
            self.is_sufficient = data['is_sufficient']
        if 'is_variation' in data:
            self.is_variation = data['is_variation']
        if 'multiplicity' in data:
            self.multiplicity = data['multiplicity']
        if 'feature' in data:
            vals = data['feature']
            self.feature = vals if isinstance(vals, list) else [vals]
        if 'owned_feature' in data:
            vals = data['owned_feature']
            self.owned_feature = vals if isinstance(vals, list) else [vals]
        if 'owned_specialization' in data:
            vals = data['owned_specialization']
            self.owned_specialization = vals if isinstance(vals, list) else [vals]
        if 'owned_conjugator' in data:
            self.owned_conjugator = data['owned_conjugator']
        if 'owned_membership' in data:
            vals = data['owned_membership']
            self.owned_membership = vals if isinstance(vals, list) else [vals]
        if 'owned_import' in data:
            vals = data['owned_import']
            self.owned_import = vals if isinstance(vals, list) else [vals]


class SysMLClass(SysMLClassifier):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Class))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Class):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLStructure(SysMLClass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Structure))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Structure):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLDataType(SysMLClassifier):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.DataType))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.DataType):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLBehavior(SysMLStructure):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Behavior))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Behavior):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLFunction(SysMLBehavior):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Function))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Function):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLPredicate(SysMLFunction):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.Predicate))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.Predicate):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLOccurrenceDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        is_sufficient = kwargs.pop('is_sufficient', None)
        super().__init__(**kwargs)
        self.__is_sufficient = is_sufficient

    @property
    def is_sufficient(self):
        return self.__is_sufficient

    @is_sufficient.setter
    def is_sufficient(self, value):
        self.__is_sufficient = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.OccurrenceDefinition))

        if self.__is_sufficient is not None:
            graph.add((subject_uri, OSLC_SYSML.isSufficient,
                       Literal(self.__is_sufficient, datatype=XSD.boolean)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.OccurrenceDefinition):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.isSufficient):
                self.is_sufficient = o.value

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_sufficient' in data:
            self.is_sufficient = data['is_sufficient']


class SysMLOccurrenceUsage(SysMLUsage):

    def __init__(self, **kwargs):
        is_reference = kwargs.pop('is_reference', None)
        may_time_vary = kwargs.pop('may_time_vary', None)
        portion_kind = kwargs.pop('portion_kind', None)
        definition = kwargs.pop('definition', None)
        super().__init__(**kwargs)
        self.__is_reference = is_reference
        self.__may_time_vary = may_time_vary
        self.__portion_kind = portion_kind
        self.__definition = definition if definition is not None else []

    @property
    def is_reference(self):
        return self.__is_reference

    @is_reference.setter
    def is_reference(self, value):
        self.__is_reference = value

    @property
    def may_time_vary(self):
        return self.__may_time_vary

    @may_time_vary.setter
    def may_time_vary(self, value):
        self.__may_time_vary = value

    @property
    def portion_kind(self):
        return self.__portion_kind

    @portion_kind.setter
    def portion_kind(self, value):
        self.__portion_kind = value

    @property
    def definition(self):
        return self.__definition

    @definition.setter
    def definition(self, value):
        self.__definition = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.OccurrenceUsage))

        if self.__is_reference is not None:
            graph.add((subject_uri, OSLC_SYSML.isReference,
                       Literal(self.__is_reference, datatype=XSD.boolean)))
        if self.__may_time_vary is not None:
            graph.add((subject_uri, OSLC_SYSML.mayTimeVary,
                       Literal(self.__may_time_vary, datatype=XSD.boolean)))
        if self.__portion_kind:
            graph.add((subject_uri, OSLC_SYSML.portionKind,
                       OSLC_SYSML[self.__portion_kind]))
        for d in self.__definition:
            graph.add((subject_uri, OSLC_SYSML.definition, URIRef(d)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.OccurrenceUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.isReference):
                self.is_reference = o.value
            for o in g.objects(r, OSLC_SYSML.mayTimeVary):
                self.may_time_vary = o.value
            for o in g.objects(r, OSLC_SYSML.portionKind):
                self.portion_kind = str(o).split('#')[-1]
            for o in g.objects(r, OSLC_SYSML.definition):
                self.definition.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'is_reference' in data:
            self.is_reference = data['is_reference']
        if 'may_time_vary' in data:
            self.may_time_vary = data['may_time_vary']
        if 'portion_kind' in data:
            self.portion_kind = data['portion_kind']
        if 'definition' in data:
            vals = data['definition']
            self.definition = vals if isinstance(vals, list) else [vals]


class SysMLLibraryPackage(SysMLPackage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.LibraryPackage))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.LibraryPackage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLViewpointUsage(SysMLRequirementUsage):

    def __init__(self, **kwargs):
        viewpoint_definition = kwargs.pop('viewpoint_definition', None)
        viewpoint_stakeholder = kwargs.pop('viewpoint_stakeholder', None)
        satisfied_viewpoint = kwargs.pop('satisfied_viewpoint', None)
        super().__init__(**kwargs)

        self.__viewpoint_definition = viewpoint_definition
        self.__viewpoint_stakeholder = viewpoint_stakeholder if viewpoint_stakeholder is not None else []
        self.__satisfied_viewpoint = satisfied_viewpoint if satisfied_viewpoint is not None else []

    @property
    def viewpoint_definition(self):
        return self.__viewpoint_definition

    @viewpoint_definition.setter
    def viewpoint_definition(self, value):
        self.__viewpoint_definition = value

    @property
    def viewpoint_stakeholder(self):
        return self.__viewpoint_stakeholder

    @viewpoint_stakeholder.setter
    def viewpoint_stakeholder(self, value):
        self.__viewpoint_stakeholder = value

    @property
    def satisfied_viewpoint(self):
        return self.__satisfied_viewpoint

    @satisfied_viewpoint.setter
    def satisfied_viewpoint(self, value):
        self.__satisfied_viewpoint = value

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)

        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)

        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ViewpointUsage))

        if self.__viewpoint_definition:
            graph.add((subject_uri, OSLC_SYSML.viewpointDefinition,
                       URIRef(self.__viewpoint_definition)))
        for sh in self.__viewpoint_stakeholder:
            graph.add((subject_uri, OSLC_SYSML.viewpointStakeholder, URIRef(sh)))
        for vp in self.__satisfied_viewpoint:
            graph.add((subject_uri, OSLC_SYSML.satisfiedViewpoint, URIRef(vp)))

        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ViewpointUsage):
            super().from_rdf(g, attributes)
            for o in g.objects(r, OSLC_SYSML.viewpointDefinition):
                self.viewpoint_definition = str(o)
            for o in g.objects(r, OSLC_SYSML.viewpointStakeholder):
                self.viewpoint_stakeholder.append(str(o))
            for o in g.objects(r, OSLC_SYSML.satisfiedViewpoint):
                self.satisfied_viewpoint.append(str(o))

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
        if 'viewpoint_definition' in data:
            self.viewpoint_definition = data['viewpoint_definition']
        if 'viewpoint_stakeholder' in data:
            vals = data['viewpoint_stakeholder']
            self.viewpoint_stakeholder = vals if isinstance(vals, list) else [vals]
        if 'satisfied_viewpoint' in data:
            vals = data['satisfied_viewpoint']
            self.satisfied_viewpoint = vals if isinstance(vals, list) else [vals]


class SysMLAttributeDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.AttributeDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.AttributeDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLAttributeUsage(SysMLUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.AttributeUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.AttributeUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLEnumerationDefinition(SysMLAttributeDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.EnumerationDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.EnumerationDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLEnumerationUsage(SysMLAttributeUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.EnumerationUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.EnumerationUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLCalculationDefinition(SysMLActionDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.CalculationDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.CalculationDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLCalculationUsage(SysMLActionUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.CalculationUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.CalculationUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLCaseDefinition(SysMLCalculationDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.CaseDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.CaseDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLCaseUsage(SysMLCalculationUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.CaseUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.CaseUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLUseCaseDefinition(SysMLCaseDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.UseCaseDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.UseCaseDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLUseCaseUsage(SysMLCaseUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.UseCaseUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.UseCaseUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLAnalysisCaseDefinition(SysMLCaseDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.AnalysisCaseDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.AnalysisCaseDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLAnalysisCaseUsage(SysMLCaseUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.AnalysisCaseUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.AnalysisCaseUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLVerificationCaseDefinition(SysMLCaseDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.VerificationCaseDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.VerificationCaseDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLVerificationCaseUsage(SysMLCaseUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.VerificationCaseUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.VerificationCaseUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLConnectionDefinition(SysMLDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConnectionDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConnectionDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLConnectionUsage(SysMLUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConnectionUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConnectionUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLFlowDefinition(SysMLConnectionDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.FlowDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.FlowDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLFlowUsage(SysMLConnectionUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.FlowUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.FlowUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLInterfaceDefinition(SysMLConnectionDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.InterfaceDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.InterfaceDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLInterfaceUsage(SysMLConnectionUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.InterfaceUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.InterfaceUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLAllocationDefinition(SysMLConnectionDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.AllocationDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.AllocationDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLAllocationUsage(SysMLConnectionUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.AllocationUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.AllocationUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLRenderingDefinition(SysMLPartDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.RenderingDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.RenderingDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLRenderingUsage(SysMLPartUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.RenderingUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.RenderingUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLReferenceUsage(SysMLUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ReferenceUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ReferenceUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLConjugatedPortDefinition(SysMLPortDefinition):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConjugatedPortDefinition))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConjugatedPortDefinition):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLConnectorAsUsage(SysMLUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.ConnectorAsUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.ConnectorAsUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLSuccessionAsUsage(SysMLConnectorAsUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.SuccessionAsUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.SuccessionAsUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)


class SysMLBindingConnectorAsUsage(SysMLConnectorAsUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_rdf(self, graph, base_url=None, attributes=None):
        super().to_rdf(graph, base_url, attributes)
        identifier = self.identifier
        if isinstance(identifier, Literal):
            identifier = identifier.value
        if base_url and identifier and identifier not in base_url.split('/'):
            base_url = self.get_absolute_url(base_url, identifier)
        subject_uri = URIRef(base_url)
        graph.add((subject_uri, RDF.type, OSLC_SYSML.BindingConnectorAsUsage))
        return graph

    def from_rdf(self, g, attributes=None):
        for r in g.subjects(RDF.type, OSLC_SYSML.BindingConnectorAsUsage):
            super().from_rdf(g, attributes)

    def from_json(self, data, attributes=None):
        super().from_json(data, attributes)
