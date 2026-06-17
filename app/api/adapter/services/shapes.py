from rdflib.namespace import XSD

from pyoslc.resources.models import Property, ResourceShape
from pyoslc.vocabularies.core import OSLC

OSLC_NS = str(OSLC)
XSD_NS = str(XSD)


def build_requirement_shape(base_uri):
    shape_uri = base_uri.rstrip('/') + '/resourceShapes/requirement'
    shape = ResourceShape(
        about=shape_uri,
        title='Requirement Resource Shape',
        describes='http://open-services.net/ns/rm#Requirement',
    )

    shape.add_shape_property(Property(
        property_definition='http://purl.org/dc/terms/identifier',
        name='identifier',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Exactly-one',
        title='Identifier',
        read_only=True,
    ))

    shape.add_shape_property(Property(
        property_definition='http://purl.org/dc/terms/title',
        name='title',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Exactly-one',
        title='Title',
    ))

    shape.add_shape_property(Property(
        property_definition='http://purl.org/dc/terms/description',
        name='description',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Description',
    ))

    shape.add_shape_property(Property(
        property_definition='http://purl.org/dc/terms/creator',
        name='creator',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Creator',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/core#shortTitle',
        name='shortTitle',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Short Title',
    ))

    shape.add_shape_property(Property(
        property_definition='http://purl.org/dc/terms/subject',
        name='subject',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Subject',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#elaboratedBy',
        name='elaboratedBy',
        value_type=OSLC_NS + 'Resource',
        range='http://open-services.net/ns/rm#TestCase',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Reference',
        title='Elaborated By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#specifiedBy',
        name='specifiedBy',
        value_type=OSLC_NS + 'Resource',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Reference',
        title='Specified By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#constrainedBy',
        name='constrainedBy',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Constrained By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#satisfiedBy',
        name='satisfiedBy',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Satisfied By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#trackedBy',
        name='trackedBy',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Tracked By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#validatedBy',
        name='validatedBy',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Validated By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#affectedBy',
        name='affectedBy',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Affected By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#decomposedBy',
        name='decomposedBy',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Decomposed By',
    ))

    shape.add_shape_property(Property(
        property_definition='http://open-services.net/ns/rm#puid',
        name='puid',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='PUID',
    ))

    return shape
