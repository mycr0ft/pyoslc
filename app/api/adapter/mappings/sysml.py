sysml_element_map = {
    'Element_id': {'attribute': '_SysMLElement__element_id', 'oslc_property': 'OSLC_SYSML.elementId'},
    'Identifier': {'attribute': '_BaseResource__identifier', 'oslc_property': 'DCTERMS.identifier'},
    'Title': {'attribute': '_BaseResource__title', 'oslc_property': 'DCTERMS.title'},
    'Description': {'attribute': '_BaseResource__description', 'oslc_property': 'DCTERMS.description'},
    'Declared_name': {'attribute': '_SysMLElement__declared_name', 'oslc_property': 'OSLC_SYSML.declaredName'},
    'Name': {'attribute': '_SysMLElement__name', 'oslc_property': 'OSLC_SYSML.name'},
    'Qualified_name': {'attribute': '_SysMLElement__qualified_name', 'oslc_property': 'OSLC_SYSML.qualifiedName'},
}

sysml_relationship_map = {
    **sysml_element_map,
    'Source': {'attribute': '_SysMLRelationship__source', 'oslc_property': 'OSLC_SYSML.source'},
    'Target': {'attribute': '_SysMLRelationship__target', 'oslc_property': 'OSLC_SYSML.target'},
    'Is_implied': {'attribute': '_SysMLRelationship__is_implied', 'oslc_property': 'OSLC_SYSML.isImplied'},
}
