from rdflib.namespace import XSD

from pyoslc.resources.models import Property, ResourceShape
from pyoslc.vocabularies.core import OSLC

OSLC_NS = str(OSLC)
XSD_NS = str(XSD)
SYSML_NS = 'https://www.omg.org/spec/sysml/vocabulary#'
AM_NS = 'http://open-services.net/ns/am#'
DCTERMS_NS = 'http://purl.org/dc/terms/'


def build_requirement_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
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


def build_sysml_element_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = ResourceShape(
        about=shape_uri,
        title='SysML Element Resource Shape',
        describes=SYSML_NS + 'Element',
    )

    shape.add_shape_property(Property(
        property_definition=DCTERMS_NS + 'identifier',
        name='identifier',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Exactly-one',
        title='Identifier',
        read_only=True,
    ))

    shape.add_shape_property(Property(
        property_definition=DCTERMS_NS + 'title',
        name='title',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Exactly-one',
        title='Title',
    ))

    shape.add_shape_property(Property(
        property_definition=DCTERMS_NS + 'description',
        name='description',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Description',
    ))

    shape.add_shape_property(Property(
        property_definition=DCTERMS_NS + 'created',
        name='created',
        value_type=XSD_NS + 'dateTime',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Created',
    ))

    shape.add_shape_property(Property(
        property_definition=DCTERMS_NS + 'modified',
        name='modified',
        value_type=XSD_NS + 'dateTime',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Modified',
    ))

    shape.add_shape_property(Property(
        property_definition=DCTERMS_NS + 'creator',
        name='creator',
        value_type=OSLC_NS + 'AnyResource',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Creator',
    ))

    shape.add_shape_property(Property(
        property_definition=DCTERMS_NS + 'contributor',
        name='contributor',
        value_type=OSLC_NS + 'AnyResource',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Contributor',
    ))

    shape.add_shape_property(Property(
        property_definition=OSLC_NS + 'serviceProvider',
        name='serviceProvider',
        value_type=OSLC_NS + 'Resource',
        range=OSLC_NS + 'ServiceProvider',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Reference',
        title='Service Provider',
    ))

    shape.add_shape_property(Property(
        property_definition=OSLC_NS + 'instanceShape',
        name='instanceShape',
        value_type=OSLC_NS + 'Resource',
        range=OSLC_NS + 'ResourceShape',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Reference',
        title='Instance Shape',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'elementId',
        name='elementId',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Exactly-one',
        title='Element ID',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'aliasIds',
        name='aliasIds',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Alias IDs',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'declaredName',
        name='declaredName',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Declared Name',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'declaredShortName',
        name='declaredShortName',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Declared Short Name',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'name',
        name='name',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Name',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'shortName',
        name='shortName',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Short Name',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'qualifiedName',
        name='qualifiedName',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Qualified Name',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isImpliedIncluded',
        name='isImpliedIncluded',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Implied Included',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isLibraryElement',
        name='isLibraryElement',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Library Element',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'owner',
        name='owner',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owner',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'owningNamespace',
        name='owningNamespace',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Namespace',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owning Namespace',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'owningMembership',
        name='owningMembership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'OwningMembership',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owning Membership',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'owningRelationship',
        name='owningRelationship',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Relationship',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owning Relationship',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedElement',
        name='ownedElement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Element',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedRelationship',
        name='ownedRelationship',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Relationship',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Relationship',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedAnnotation',
        name='ownedAnnotation',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Annotation',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Annotation',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'documentation',
        name='documentation',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Documentation',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Documentation',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))

    return shape


def _add_requirement_definition_properties(shape):
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'reqId',
        name='reqId',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Exactly-one',
        title='Requirement ID',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'text',
        name='text',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Text',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'assumedConstraint',
        name='assumedConstraint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConstraintUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Assumed Constraint',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'requiredConstraint',
        name='requiredConstraint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConstraintUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Required Constraint',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'framedConcern',
        name='framedConcern',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConcernUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Framed Concern',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'referencedConcern',
        name='referencedConcern',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConcernUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Referenced Concern',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedStakeholderParameter',
        name='ownedStakeholderParameter',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'StakeholderMembership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Stakeholder Parameter',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedSubjectParameter',
        name='ownedSubjectParameter',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'SubjectMembership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Subject Parameter',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedActorParameter',
        name='ownedActorParameter',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActorMembership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Actor Parameter',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedObjectiveRequirement',
        name='ownedObjectiveRequirement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RequirementUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owned Objective Requirement',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'stakeholderParameter',
        name='stakeholderParameter',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Stakeholder Parameter',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'subjectParameter',
        name='subjectParameter',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Subject Parameter',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'actorParameter',
        name='actorParameter',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Actor Parameter',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'referencedRendering',
        name='referencedRendering',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RenderingUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Referenced Rendering',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewpointStakeholder',
        name='viewpointStakeholder',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Viewpoint Stakeholder',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedConcern',
        name='ownedConcern',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConcernUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Concern',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedViewpoint',
        name='ownedViewpoint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewpointUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Viewpoint',
    ))


def _add_requirement_usage_properties(shape):
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'reqId',
        name='reqId',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Exactly-one',
        title='Requirement ID',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'text',
        name='text',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-many',
        title='Text',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'assumedConstraint',
        name='assumedConstraint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConstraintUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Assumed Constraint',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'requiredConstraint',
        name='requiredConstraint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConstraintUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Required Constraint',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'framedConcern',
        name='framedConcern',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConcernUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Framed Concern',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'referencedConcern',
        name='referencedConcern',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConcernUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Referenced Concern',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'referencedRendering',
        name='referencedRendering',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RenderingUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Referenced Rendering',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'satisfiedRequirement',
        name='satisfiedRequirement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RequirementUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Satisfied Requirement',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'satisfiedViewpoint',
        name='satisfiedViewpoint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewpointUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Satisfied Viewpoint',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'verifiedRequirement',
        name='verifiedRequirement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RequirementUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Verified Requirement',
    ))


def build_sysml_requirement_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML RequirementDefinition Resource Shape'
    shape.describes = SYSML_NS + 'RequirementDefinition'

    _add_requirement_definition_properties(shape)

    return shape


def build_sysml_requirement_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML RequirementUsage Resource Shape'
    shape.describes = SYSML_NS + 'RequirementUsage'

    _add_requirement_usage_properties(shape)

    return shape


def build_sysml_concern_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_requirement_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ConcernDefinition Resource Shape'
    shape.describes = SYSML_NS + 'ConcernDefinition'

    return shape


def build_sysml_concern_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_requirement_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ConcernUsage Resource Shape'
    shape.describes = SYSML_NS + 'ConcernUsage'

    return shape


def build_sysml_relationship_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = ResourceShape(
        about=shape_uri,
        title='SysML Relationship Resource Shape',
        describes=SYSML_NS + 'Relationship',
    )

    element_shape = build_sysml_element_shape(base_uri)
    for prop in element_shape.shape_properties:
        shape.add_shape_property(prop)

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'source',
        name='source',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Source',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'target',
        name='target',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Target',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isImplied',
        name='isImplied',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Implied',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'relatedElement',
        name='relatedElement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Related Element',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedRelatedElement',
        name='ownedRelatedElement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Related Element',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'owningRelatedElement',
        name='owningRelatedElement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owning Related Element',
    ))

    return shape


def _add_namespace_properties(shape):
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'member',
        name='member',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Member',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'membership',
        name='membership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Membership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Membership',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedMember',
        name='ownedMember',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Member',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedMembership',
        name='ownedMembership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'OwningMembership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Membership',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'importedMembership',
        name='importedMembership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Membership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Imported Membership',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedImport',
        name='ownedImport',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Import',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Import',
    ))


def _add_type_properties(shape):
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isAbstract',
        name='isAbstract',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Abstract',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isConjugated',
        name='isConjugated',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Conjugated',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isSufficient',
        name='isSufficient',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Sufficient',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'multiplicity',
        name='multiplicity',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Multiplicity',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Multiplicity',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'feature',
        name='feature',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Feature',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'directedFeature',
        name='directedFeature',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Directed Feature',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'endFeature',
        name='endFeature',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='End Feature',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedFeature',
        name='ownedFeature',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Feature',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedEndFeature',
        name='ownedEndFeature',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned End Feature',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedFeatureMembership',
        name='ownedFeatureMembership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'FeatureMembership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Feature Membership',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'featureMembership',
        name='featureMembership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'FeatureMembership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Feature Membership',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'inheritedFeature',
        name='inheritedFeature',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Inherited Feature',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'inheritedMembership',
        name='inheritedMembership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Membership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Inherited Membership',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'input',
        name='input',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Input',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'output',
        name='output',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Output',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedSpecialization',
        name='ownedSpecialization',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Specialization',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Specialization',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedConjugator',
        name='ownedConjugator',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Conjugation',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owned Conjugator',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedDifferencing',
        name='ownedDifferencing',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Differencing',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Differencing',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedDisjoining',
        name='ownedDisjoining',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Disjoining',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Disjoining',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedIntersecting',
        name='ownedIntersecting',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Intersecting',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Intersecting',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedUnioning',
        name='ownedUnioning',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Unioning',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Unioning',
    ))


def build_sysml_namespace_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = ResourceShape(
        about=shape_uri,
        title='SysML Namespace Resource Shape',
        describes=SYSML_NS + 'Namespace',
    )

    element_shape = build_sysml_element_shape(base_uri)
    for prop in element_shape.shape_properties:
        shape.add_shape_property(prop)

    _add_namespace_properties(shape)

    return shape


def build_sysml_type_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = ResourceShape(
        about=shape_uri,
        title='SysML Type Resource Shape',
        describes=SYSML_NS + 'Type',
    )

    element_shape = build_sysml_element_shape(base_uri)
    for prop in element_shape.shape_properties:
        shape.add_shape_property(prop)

    _add_namespace_properties(shape)
    _add_type_properties(shape)

    return shape


def build_sysml_package_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = ResourceShape(
        about=shape_uri,
        title='SysML Package Resource Shape',
        describes=SYSML_NS + 'Package',
    )

    element_shape = build_sysml_element_shape(base_uri)
    for prop in element_shape.shape_properties:
        shape.add_shape_property(prop)

    _add_namespace_properties(shape)

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))

    return shape


def _add_action_definition_properties(shape):
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'action',
        name='action',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActionUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Action',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'behavior',
        name='behavior',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Behavior',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Behavior',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'step',
        name='step',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Step',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Step',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'parameter',
        name='parameter',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Feature',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Parameter',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedConstraint',
        name='ownedConstraint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConstraintUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Constraint',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedRequirement',
        name='ownedRequirement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RequirementUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Requirement',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedConcern',
        name='ownedConcern',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConcernUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Concern',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedRendering',
        name='ownedRendering',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RenderingUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Rendering',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedCalculation',
        name='ownedCalculation',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'CalculationUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Calculation',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedCase',
        name='ownedCase',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'CaseUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Case',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedAnalysisCase',
        name='ownedAnalysisCase',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'AnalysisCaseUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Analysis Case',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedVerificationCase',
        name='ownedVerificationCase',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'VerificationCaseUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Verification Case',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedUseCase',
        name='ownedUseCase',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'UseCaseUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Use Case',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedTransition',
        name='ownedTransition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'TransitionUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Transition',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedState',
        name='ownedState',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'StateUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned State',
    ))


def _add_action_usage_properties(shape):
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'actionDefinition',
        name='actionDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActionDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Action Definition',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'behavior',
        name='behavior',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Behavior',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Behavior',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedCalculation',
        name='nestedCalculation',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'CalculationUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Calculation',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedCase',
        name='nestedCase',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'CaseUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Case',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedConcern',
        name='nestedConcern',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConcernUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Concern',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedConstraint',
        name='nestedConstraint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConstraintUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Constraint',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedEnumeration',
        name='nestedEnumeration',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'EnumerationUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Enumeration',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedFlow',
        name='nestedFlow',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'FlowUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Flow',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedItem',
        name='nestedItem',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ItemUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Item',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedMetadata',
        name='nestedMetadata',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'MetadataUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Metadata',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedOccurrence',
        name='nestedOccurrence',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'OccurrenceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Occurrence',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedReference',
        name='nestedReference',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ReferenceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Reference',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedRendering',
        name='nestedRendering',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RenderingUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Rendering',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedRequirement',
        name='nestedRequirement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RequirementUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Requirement',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedState',
        name='nestedState',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'StateUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested State',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedTransition',
        name='nestedTransition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'TransitionUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Transition',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedUseCase',
        name='nestedUseCase',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'UseCaseUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Use Case',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedVerificationCase',
        name='nestedVerificationCase',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'VerificationCaseUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Verification Case',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedView',
        name='nestedView',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested View',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedViewpoint',
        name='nestedViewpoint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewpointUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Viewpoint',
    ))


def build_sysml_action_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ActionDefinition Resource Shape'
    shape.describes = SYSML_NS + 'ActionDefinition'

    _add_action_definition_properties(shape)

    return shape


def build_sysml_action_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ActionUsage Resource Shape'
    shape.describes = SYSML_NS + 'ActionUsage'

    _add_action_usage_properties(shape)

    return shape


def build_sysml_state_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_action_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML StateDefinition Resource Shape'
    shape.describes = SYSML_NS + 'StateDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'state',
        name='state',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'StateUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='State',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'entryAction',
        name='entryAction',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActionUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Entry Action',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'doAction',
        name='doAction',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActionUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Do Action',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'exitAction',
        name='exitAction',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActionUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Exit Action',
    ))

    return shape


def build_sysml_state_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_action_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML StateUsage Resource Shape'
    shape.describes = SYSML_NS + 'StateUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'stateDefinition',
        name='stateDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'StateDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='State Definition',
    ))

    return shape


def build_sysml_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = ResourceShape(
        about=shape_uri,
        title='SysML Definition Resource Shape',
        describes=SYSML_NS + 'Definition',
    )

    element_shape = build_sysml_element_shape(base_uri)
    for prop in element_shape.shape_properties:
        shape.add_shape_property(prop)

    _add_namespace_properties(shape)
    _add_type_properties(shape)

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isVariation',
        name='isVariation',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Variation',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedAction',
        name='ownedAction',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActionUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Action',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedPart',
        name='ownedPart',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Part',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedPort',
        name='ownedPort',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PortUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Port',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedRequirement',
        name='ownedRequirement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RequirementUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Requirement',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedAttribute',
        name='ownedAttribute',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'AttributeUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Attribute',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedUsage',
        name='ownedUsage',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Usage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Usage',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'variant',
        name='variant',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Usage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Variant',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))

    return shape


def build_sysml_constraint_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ConstraintDefinition Resource Shape'
    shape.describes = SYSML_NS + 'ConstraintDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isNegated',
        name='isNegated',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Negated',
    ))

    return shape


def build_sysml_constraint_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ConstraintUsage Resource Shape'
    shape.describes = SYSML_NS + 'ConstraintUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isNegated',
        name='isNegated',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Negated',
    ))

    return shape


def build_sysml_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = ResourceShape(
        about=shape_uri,
        title='SysML Usage Resource Shape',
        describes=SYSML_NS + 'Usage',
    )

    element_shape = build_sysml_element_shape(base_uri)
    for prop in element_shape.shape_properties:
        shape.add_shape_property(prop)

    _add_namespace_properties(shape)
    _add_type_properties(shape)

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isReference',
        name='isReference',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Reference',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'mayTimeVary',
        name='mayTimeVary',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='May Time Vary',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'portionKind',
        name='portionKind',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PortionKind',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Portion Kind',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'definition',
        name='definition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Classifier',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Definition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'owningDefinition',
        name='owningDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Definition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owning Definition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'owningUsage',
        name='owningUsage',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Usage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Owning Usage',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isVariation',
        name='isVariation',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Variation',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'individualDefinition',
        name='individualDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'OccurrenceDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Individual Definition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'variant',
        name='variant',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Usage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Variant',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'variantMembership',
        name='variantMembership',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'VariantMembership',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Variant Membership',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedAction',
        name='nestedAction',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ActionUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Action',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedPart',
        name='nestedPart',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Part',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedPort',
        name='nestedPort',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PortUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Port',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedRequirement',
        name='nestedRequirement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RequirementUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Requirement',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedAttribute',
        name='nestedAttribute',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'AttributeUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Attribute',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))

    return shape


def build_sysml_view_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_part_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ViewDefinition Resource Shape'
    shape.describes = SYSML_NS + 'ViewDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewCondition',
        name='viewCondition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Expression',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='View Condition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewRendering',
        name='viewRendering',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RenderingUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='View Rendering',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))

    return shape


def _build_inherited_shape(base_uri, parent_shape_func, title, describes):
    shape_uri = base_uri.rstrip('/')
    shape = parent_shape_func(base_uri)
    shape.about = shape_uri
    shape.title = title
    shape.describes = describes
    return shape


# --- Phase 8: Feature ---

def build_sysml_feature_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_type_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML Feature Resource Shape'
    shape.describes = SYSML_NS + 'Feature'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isComposite',
        name='isComposite',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Composite',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isDerived',
        name='isDerived',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Derived',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isEnd',
        name='isEnd',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is End',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isOrdered',
        name='isOrdered',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Ordered',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isPortion',
        name='isPortion',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Portion',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isReadOnly',
        name='isReadOnly',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Read Only',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isUnique',
        name='isUnique',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Unique',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'direction',
        name='direction',
        value_type=XSD_NS + 'string',
        occurs=OSLC_NS + 'Zero-or-one',
        title='Direction',
    ))

    return shape


# --- Phase 8: Classifier ---

def build_sysml_classifier_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_type_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML Classifier Resource Shape'
    shape.describes = SYSML_NS + 'Classifier'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isVariation',
        name='isVariation',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Variation',
    ))

    return shape


# --- Phase 8: OccurrenceDefinition ---

def build_sysml_occurrence_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML OccurrenceDefinition Resource Shape'
    shape.describes = SYSML_NS + 'OccurrenceDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isSufficient',
        name='isSufficient',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Sufficient',
    ))

    return shape


# --- Phase 8: OccurrenceUsage ---

def build_sysml_occurrence_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML OccurrenceUsage Resource Shape'
    shape.describes = SYSML_NS + 'OccurrenceUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'isReference',
        name='isReference',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='Is Reference',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'mayTimeVary',
        name='mayTimeVary',
        value_type=XSD_NS + 'boolean',
        occurs=OSLC_NS + 'Exactly-one',
        title='May Time Vary',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'portionKind',
        name='portionKind',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PortionKind',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Portion Kind',
    ))
    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'definition',
        name='definition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Classifier',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Definition',
    ))

    return shape


# --- Phase 8 marker shapes (no new properties beyond inheritance) ---

def build_sysml_class_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_classifier_shape,
        'SysML Class Resource Shape', SYSML_NS + 'Class',
    )


def build_sysml_structure_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_class_shape,
        'SysML Structure Resource Shape', SYSML_NS + 'Structure',
    )


def build_sysml_data_type_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_classifier_shape,
        'SysML DataType Resource Shape', SYSML_NS + 'DataType',
    )


def build_sysml_behavior_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_structure_shape,
        'SysML Behavior Resource Shape', SYSML_NS + 'Behavior',
    )


def build_sysml_function_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_behavior_shape,
        'SysML Function Resource Shape', SYSML_NS + 'Function',
    )


def build_sysml_predicate_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_function_shape,
        'SysML Predicate Resource Shape', SYSML_NS + 'Predicate',
    )


def build_sysml_library_package_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_package_shape,
        'SysML LibraryPackage Resource Shape', SYSML_NS + 'LibraryPackage',
    )


def build_sysml_attribute_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, _build_on_definition_shape,
        'SysML AttributeDefinition Resource Shape', SYSML_NS + 'AttributeDefinition',
    )


def build_sysml_attribute_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, _build_on_usage_shape,
        'SysML AttributeUsage Resource Shape', SYSML_NS + 'AttributeUsage',
    )


def build_sysml_enumeration_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_attribute_definition_shape,
        'SysML EnumerationDefinition Resource Shape', SYSML_NS + 'EnumerationDefinition',
    )


def build_sysml_enumeration_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_attribute_usage_shape,
        'SysML EnumerationUsage Resource Shape', SYSML_NS + 'EnumerationUsage',
    )


def build_sysml_calculation_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_action_definition_shape,
        'SysML CalculationDefinition Resource Shape', SYSML_NS + 'CalculationDefinition',
    )


def build_sysml_calculation_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_action_usage_shape,
        'SysML CalculationUsage Resource Shape', SYSML_NS + 'CalculationUsage',
    )


def build_sysml_case_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_calculation_definition_shape,
        'SysML CaseDefinition Resource Shape', SYSML_NS + 'CaseDefinition',
    )


def build_sysml_case_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_calculation_usage_shape,
        'SysML CaseUsage Resource Shape', SYSML_NS + 'CaseUsage',
    )


def build_sysml_use_case_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_case_definition_shape,
        'SysML UseCaseDefinition Resource Shape', SYSML_NS + 'UseCaseDefinition',
    )


def build_sysml_use_case_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_case_usage_shape,
        'SysML UseCaseUsage Resource Shape', SYSML_NS + 'UseCaseUsage',
    )


def build_sysml_analysis_case_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_case_definition_shape,
        'SysML AnalysisCaseDefinition Resource Shape', SYSML_NS + 'AnalysisCaseDefinition',
    )


def build_sysml_analysis_case_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_case_usage_shape,
        'SysML AnalysisCaseUsage Resource Shape', SYSML_NS + 'AnalysisCaseUsage',
    )


def build_sysml_verification_case_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_case_definition_shape,
        'SysML VerificationCaseDefinition Resource Shape', SYSML_NS + 'VerificationCaseDefinition',
    )


def build_sysml_verification_case_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_case_usage_shape,
        'SysML VerificationCaseUsage Resource Shape', SYSML_NS + 'VerificationCaseUsage',
    )


def build_sysml_connection_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, _build_on_definition_shape,
        'SysML ConnectionDefinition Resource Shape', SYSML_NS + 'ConnectionDefinition',
    )


def build_sysml_connection_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, _build_on_usage_shape,
        'SysML ConnectionUsage Resource Shape', SYSML_NS + 'ConnectionUsage',
    )


def build_sysml_flow_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connection_definition_shape,
        'SysML FlowDefinition Resource Shape', SYSML_NS + 'FlowDefinition',
    )


def build_sysml_flow_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connection_usage_shape,
        'SysML FlowUsage Resource Shape', SYSML_NS + 'FlowUsage',
    )


def build_sysml_interface_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connection_definition_shape,
        'SysML InterfaceDefinition Resource Shape', SYSML_NS + 'InterfaceDefinition',
    )


def build_sysml_interface_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connection_usage_shape,
        'SysML InterfaceUsage Resource Shape', SYSML_NS + 'InterfaceUsage',
    )


def build_sysml_allocation_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connection_definition_shape,
        'SysML AllocationDefinition Resource Shape', SYSML_NS + 'AllocationDefinition',
    )


def build_sysml_allocation_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connection_usage_shape,
        'SysML AllocationUsage Resource Shape', SYSML_NS + 'AllocationUsage',
    )


def build_sysml_rendering_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_part_definition_shape,
        'SysML RenderingDefinition Resource Shape', SYSML_NS + 'RenderingDefinition',
    )


def build_sysml_rendering_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_part_usage_shape,
        'SysML RenderingUsage Resource Shape', SYSML_NS + 'RenderingUsage',
    )


def build_sysml_reference_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, _build_on_usage_shape,
        'SysML ReferenceUsage Resource Shape', SYSML_NS + 'ReferenceUsage',
    )


def build_sysml_conjugated_port_definition_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_port_definition_shape,
        'SysML ConjugatedPortDefinition Resource Shape', SYSML_NS + 'ConjugatedPortDefinition',
    )


def build_sysml_connector_as_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, _build_on_usage_shape,
        'SysML ConnectorAsUsage Resource Shape', SYSML_NS + 'ConnectorAsUsage',
    )


def build_sysml_succession_as_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connector_as_usage_shape,
        'SysML SuccessionAsUsage Resource Shape', SYSML_NS + 'SuccessionAsUsage',
    )


def build_sysml_binding_connector_as_usage_shape(base_uri):
    return _build_inherited_shape(
        base_uri, build_sysml_connector_as_usage_shape,
        'SysML BindingConnectorAsUsage Resource Shape', SYSML_NS + 'BindingConnectorAsUsage',
    )


def build_sysml_view_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_part_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ViewUsage Resource Shape'
    shape.describes = SYSML_NS + 'ViewUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewDefinition',
        name='viewDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='View Definition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewCondition',
        name='viewCondition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Expression',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='View Condition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewRendering',
        name='viewRendering',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'RenderingUsage',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='View Rendering',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'exposedElement',
        name='exposedElement',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'Element',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Exposed Element',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'satisfiedViewpoint',
        name='satisfiedViewpoint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewpointUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Satisfied Viewpoint',
    ))

    return shape


def build_sysml_viewpoint_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_requirement_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ViewpointDefinition Resource Shape'
    shape.describes = SYSML_NS + 'ViewpointDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewpointStakeholder',
        name='viewpointStakeholder',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Viewpoint Stakeholder',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'satisfiedViewpoint',
        name='satisfiedViewpoint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewpointUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Satisfied Viewpoint',
    ))

    return shape


def build_sysml_viewpoint_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_requirement_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ViewpointUsage Resource Shape'
    shape.describes = SYSML_NS + 'ViewpointUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewpointDefinition',
        name='viewpointDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewpointDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Viewpoint Definition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'viewpointStakeholder',
        name='viewpointStakeholder',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'PartUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Viewpoint Stakeholder',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'satisfiedViewpoint',
        name='satisfiedViewpoint',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ViewpointUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Satisfied Viewpoint',
    ))

    return shape


def _build_on_definition_shape(base_uri):
    shape = build_sysml_definition_shape(base_uri)
    return shape


def _build_on_usage_shape(base_uri):
    shape = build_sysml_usage_shape(base_uri)
    return shape


def build_sysml_item_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ItemDefinition Resource Shape'
    shape.describes = SYSML_NS + 'ItemDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedOccurrence',
        name='ownedOccurrence',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'OccurrenceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Occurrence',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedItem',
        name='ownedItem',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ItemUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Item',
    ))

    return shape


def build_sysml_item_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML ItemUsage Resource Shape'
    shape.describes = SYSML_NS + 'ItemUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'occurrenceDefinition',
        name='occurrenceDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'OccurrenceDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Occurrence Definition',
    ))

    return shape


def build_sysml_part_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_item_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML PartDefinition Resource Shape'
    shape.describes = SYSML_NS + 'PartDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedConnection',
        name='ownedConnection',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConnectorAsUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Connection',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'ownedInterface',
        name='ownedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Owned Interface',
    ))

    return shape


def build_sysml_part_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = build_sysml_item_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML PartUsage Resource Shape'
    shape.describes = SYSML_NS + 'PartUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedItem',
        name='nestedItem',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ItemUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Item',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedConnection',
        name='nestedConnection',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConnectorAsUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Connection',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))

    return shape


def build_sysml_port_definition_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_definition_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML PortDefinition Resource Shape'
    shape.describes = SYSML_NS + 'PortDefinition'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'conjugatedPortDefinition',
        name='conjugatedPortDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConjugatedPortDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Conjugated Port Definition',
    ))

    return shape


def build_sysml_port_usage_shape(base_uri):
    shape_uri = base_uri.rstrip('/')
    shape = _build_on_usage_shape(base_uri)
    shape.about = shape_uri
    shape.title = 'SysML PortUsage Resource Shape'
    shape.describes = SYSML_NS + 'PortUsage'

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'conjugatedPortDefinition',
        name='conjugatedPortDefinition',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConjugatedPortDefinition',
        occurs=OSLC_NS + 'Zero-or-one',
        representation=OSLC_NS + 'Either',
        title='Conjugated Port Definition',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedConnection',
        name='nestedConnection',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'ConnectorAsUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Connection',
    ))

    shape.add_shape_property(Property(
        property_definition=SYSML_NS + 'nestedInterface',
        name='nestedInterface',
        value_type=OSLC_NS + 'Resource',
        range=SYSML_NS + 'InterfaceUsage',
        occurs=OSLC_NS + 'Zero-or-many',
        representation=OSLC_NS + 'Either',
        title='Nested Interface',
    ))

    return shape
