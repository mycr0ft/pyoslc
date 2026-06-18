import logging

from rdflib import BNode, Graph, Literal, RDF, URIRef
from rdflib.namespace import SH, XSD

from pyoslc.vocabularies.core import OSLC

logger = logging.getLogger(__name__)

OSLC_NS = str(OSLC)


_OCCURS_MAP = {
    OSLC_NS + 'Exactly-one': (1, 1),
    OSLC_NS + 'Zero-or-one': (0, 1),
    OSLC_NS + 'Zero-or-many': (0, None),
    OSLC_NS + 'One-or-many': (1, None),
}


def _map_value_type(value_type_uri):
    if not value_type_uri:
        return None
    vt = str(value_type_uri)
    if vt.startswith('http://www.w3.org/2001/XMLSchema#'):
        return URIRef(vt)
    if vt == OSLC_NS + 'Resource':
        return None
    return URIRef(vt)


def _map_occurs(occurs_uri):
    if not occurs_uri:
        return None, None
    return _OCCURS_MAP.get(str(occurs_uri), (None, None))


def oslc_shape_to_shacl(oslc_graph, shacl_graph=None):
    if shacl_graph is None:
        shacl_graph = Graph()
    shacl_graph.bind('sh', SH)
    shacl_graph.bind('xsd', XSD)

    for shape_subj in oslc_graph.subjects(RDF.type, OSLC.ResourceShape):
        node_shape = BNode()
        shacl_graph.add((node_shape, RDF.type, SH.NodeShape))

        describes = oslc_graph.value(shape_subj, OSLC.describes)
        if describes:
            shacl_graph.add((node_shape, SH.targetClass, describes))

        title = oslc_graph.value(shape_subj, OSLC.title)
        if title:
            shacl_graph.add((node_shape, SH.name, title))

        for prop_subj in oslc_graph.objects(shape_subj, OSLC.property):
            prop_shape = BNode()
            shacl_graph.add((prop_shape, RDF.type, SH.PropertyShape))

            prop_def = oslc_graph.value(prop_subj, OSLC.propertyDefinition)
            if prop_def:
                shacl_graph.add((prop_shape, SH.path, prop_def))

            p_name = oslc_graph.value(prop_subj, OSLC.name)
            if p_name:
                shacl_graph.add((prop_shape, SH.name, Literal(p_name)))

            p_title = oslc_graph.value(prop_subj, OSLC.title)
            if p_title and not p_name:
                shacl_graph.add((prop_shape, SH.name, p_title))

            p_value_type = oslc_graph.value(prop_subj, OSLC.valueType)
            datatype = _map_value_type(p_value_type)
            if datatype:
                shacl_graph.add((prop_shape, SH.datatype, datatype))
            elif p_value_type and str(p_value_type) == OSLC_NS + 'Resource':
                shacl_graph.add((prop_shape, SH.nodeKind, SH.IRI))

            p_range = oslc_graph.value(prop_subj, OSLC.range)
            if p_range:
                shacl_graph.add((prop_shape, URIRef(SH + 'class'), p_range))

            p_occurs = oslc_graph.value(prop_subj, OSLC.occurs)
            min_c, max_c = _map_occurs(p_occurs)
            if min_c is not None:
                shacl_graph.add((prop_shape, SH.minCount, Literal(min_c)))
            if max_c is not None:
                shacl_graph.add((prop_shape, SH.maxCount, Literal(max_c)))

            p_read_only = oslc_graph.value(prop_subj, OSLC.readOnly)
            if p_read_only and str(p_read_only) == 'true':
                pass

            p_value_shape = oslc_graph.value(prop_subj, OSLC.valueShape)
            if p_value_shape:
                shacl_graph.add((prop_shape, SH.node, p_value_shape))

            shacl_graph.add((node_shape, SH.property, prop_shape))

    return shacl_graph


def validate_resource(resource_graph, shape_graph, **kwargs):
    import pyshacl

    return pyshacl.validate(
        data_graph=resource_graph,
        shacl_graph=shape_graph,
        **kwargs,
    )
