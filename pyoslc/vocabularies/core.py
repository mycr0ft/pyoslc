"""
    Vocabulary definition for the OSLC specification.

    Taken from:
    http://docs.oasis-open.org/oslc-core/oslc-core/v3.0/csprd03/part7-core-vocabulary/oslc-core-v3.0-csprd03-part7-core-vocabulary.html#rdfvocab
    http://docs.oasis-open.org/oslc-core/oslc-core/v3.0/csprd03/part7-core-vocabulary/oslc-core-v3.0-csprd03-part7-core-vocabulary.html#vocabulary-details

"""
from rdflib import URIRef
from rdflib.namespace import ClosedNamespace

OSLC = ClosedNamespace(
    uri=URIRef("http://open-services.net/ns/core#"),
    terms=[
        # RDFS Classes in this namespace (27 total, per OSLC Core v3.0 Part 7)
        "AllowedValues", "Any", "AttachmentContainer", "AttachmentDescriptor",
        "Cardinality", "Comment", "Compact", "CreationFactory", "Dialog",
        "Discussion", "Error", "ExtendedError", "ImpactType",
        "OAuthConfiguration", "PrefixDefinition", "Preview", "Property",
        "Publisher", "QueryCapability", "Representation", "ResourceShape",
        "ResourceShapeConstraints", "ResourceValueType", "ResponseInfo",
        "Service", "ServiceProvider", "ServiceProviderCatalog",

        # RDF Properties in this namespace (81 total, per OSLC Core v3.0 Part 7)
        "allowedValue", "allowedValues", "archived", "attachment", "attachmentSize",
        "authorizationURI", "cause", "comment", "creation", "creationDialog",
        "creationFactory", "default", "defaultValue", "describes", "details",
        "dialog", "discussedBy", "discussionAbout", "document", "domain", "error",
        "executes", "extendedError", "futureAction", "hidden", "hintHeight",
        "hintWidth", "icon", "iconAltLabel", "iconSrcSet", "iconTitle", "impactType",
        "initialHeight", "inReplyTo", "instanceShape", "inverseLabel",
        "isMemberProperty", "label", "largePreview", "maxSize", "message",
        "modifiedBy", "moreInfo", "name", "nextPage", "oauthAccessTokenURI",
        "oauthConfiguration", "oauthRequestTokenURI", "occurs", "order",
        "partOfDiscussion", "postBody", "prefix", "prefixBase", "prefixDefinition",
        "property", "propertyDefinition", "publisher", "queryable", "queryBase",
        "queryCapability", "range", "readOnly", "rel", "representation",
        "resourceShape", "resourceType", "results", "score", "selectionDialog",
        "service", "serviceProvider", "serviceProviderCatalog", "shortId",
        "shortTitle", "smallPreview", "statusCode", "totalCount", "usage",
        "valueShape", "valueType",
    ]
)
