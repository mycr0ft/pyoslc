from flask_restx import fields

from app.api.adapter import api

base_sysml_element = api.model('Base SysML Element', {
    'identifier': fields.String,
    'title': fields.String,
    'description': fields.String,
    'element_id': fields.String,
    'declared_name': fields.String,
    'declared_short_name': fields.String,
    'name': fields.String,
    'short_name': fields.String,
    'qualified_name': fields.String,
    'is_implied_included': fields.Boolean,
    'is_library_element': fields.Boolean,
    'alias_ids': fields.List(fields.String),
})

sysml_element = api.inherit('SysML Element', base_sysml_element, {
    'owned_element': fields.List(fields.String),
    'owned_relationship': fields.List(fields.String),
})

sysml_relationship = api.inherit('SysML Relationship', base_sysml_element, {
    'source': fields.List(fields.String),
    'target': fields.List(fields.String),
    'is_implied': fields.Boolean,
    'related_element': fields.List(fields.String),
    'owned_related_element': fields.List(fields.String),
    'owning_related_element': fields.String,
})

sysml_package = api.inherit('SysML Package', base_sysml_element, {
    'member': fields.List(fields.String),
    'owned_member': fields.List(fields.String),
    'filter_condition': fields.List(fields.String),
})

sysml_definition = api.inherit('SysML Definition', base_sysml_element, {
    'is_abstract': fields.Boolean,
    'is_conjugated': fields.Boolean,
    'is_sufficient': fields.Boolean,
    'is_variation': fields.Boolean,
    'multiplicity': fields.String,
    'feature': fields.List(fields.String),
    'owned_feature': fields.List(fields.String),
    'owned_specialization': fields.List(fields.String),
    'owned_action': fields.List(fields.String),
    'owned_part': fields.List(fields.String),
    'owned_port': fields.List(fields.String),
    'owned_requirement': fields.List(fields.String),
    'owned_attribute': fields.List(fields.String),
    'owned_usage': fields.List(fields.String),
    'variant': fields.List(fields.String),
})

sysml_usage = api.inherit('SysML Usage', base_sysml_element, {
    'is_abstract': fields.Boolean,
    'is_conjugated': fields.Boolean,
    'is_sufficient': fields.Boolean,
    'is_reference': fields.Boolean,
    'may_time_vary': fields.Boolean,
    'portion_kind': fields.String,
    'definition': fields.List(fields.String),
    'owning_definition': fields.String,
    'owning_usage': fields.String,
    'is_variation': fields.Boolean,
    'nested_action': fields.List(fields.String),
    'nested_part': fields.List(fields.String),
    'nested_port': fields.List(fields.String),
    'nested_requirement': fields.List(fields.String),
    'nested_attribute': fields.List(fields.String),
    'nested_usage': fields.List(fields.String),
})

sysml_item_definition = api.inherit('SysML ItemDefinition', sysml_definition, {
    'owned_occurrence': fields.List(fields.String),
    'owned_item': fields.List(fields.String),
})

sysml_item_usage = api.inherit('SysML ItemUsage', sysml_usage, {
    'occurrence_definition': fields.String,
})

sysml_part_definition = api.inherit('SysML PartDefinition', sysml_item_definition, {
    'owned_connection': fields.List(fields.String),
    'owned_interface': fields.List(fields.String),
})

sysml_part_usage = api.inherit('SysML PartUsage', sysml_item_usage, {
    'nested_item': fields.List(fields.String),
    'nested_connection': fields.List(fields.String),
    'nested_interface': fields.List(fields.String),
})

sysml_port_definition = api.inherit('SysML PortDefinition', sysml_definition, {
    'conjugated_port_definition': fields.String,
})

sysml_port_usage = api.inherit('SysML PortUsage', sysml_usage, {
    'conjugated_port_definition': fields.String,
    'nested_connection': fields.List(fields.String),
    'nested_interface': fields.List(fields.String),
})

_requirement_base_fields = {
    'req_id': fields.String,
    'text': fields.List(fields.String),
    'assumed_constraint': fields.List(fields.String),
    'required_constraint': fields.List(fields.String),
    'framed_concern': fields.List(fields.String),
    'referenced_concern': fields.List(fields.String),
    'referenced_rendering': fields.String,
}

sysml_requirement_definition = api.inherit('SysML RequirementDefinition', sysml_definition, {
    **_requirement_base_fields,
    'owned_stakeholder_parameter': fields.List(fields.String),
    'owned_subject_parameter': fields.List(fields.String),
    'owned_actor_parameter': fields.List(fields.String),
    'owned_objective_requirement': fields.String,
    'stakeholder_parameter': fields.List(fields.String),
    'subject_parameter': fields.List(fields.String),
    'actor_parameter': fields.List(fields.String),
    'viewpoint_stakeholder': fields.List(fields.String),
    'owned_concern': fields.List(fields.String),
    'owned_viewpoint': fields.List(fields.String),
})

sysml_requirement_usage = api.inherit('SysML RequirementUsage', sysml_usage, {
    **_requirement_base_fields,
    'satisfied_requirement': fields.List(fields.String),
    'satisfied_viewpoint': fields.List(fields.String),
    'verified_requirement': fields.List(fields.String),
})

sysml_concern_definition = api.inherit('SysML ConcernDefinition',
                                       sysml_requirement_definition, {})

sysml_concern_usage = api.inherit('SysML ConcernUsage',
                                  sysml_requirement_usage, {})

sysml_action_definition = api.inherit('SysML ActionDefinition', sysml_definition, {
    'action': fields.List(fields.String),
    'behavior': fields.List(fields.String),
    'step': fields.List(fields.String),
    'parameter': fields.List(fields.String),
    'owned_constraint': fields.List(fields.String),
    'owned_requirement': fields.List(fields.String),
    'owned_concern': fields.List(fields.String),
    'owned_rendering': fields.List(fields.String),
    'owned_calculation': fields.List(fields.String),
    'owned_case': fields.List(fields.String),
    'owned_analysis_case': fields.List(fields.String),
    'owned_verification_case': fields.List(fields.String),
    'owned_use_case': fields.List(fields.String),
    'owned_transition': fields.List(fields.String),
    'owned_state': fields.List(fields.String),
})

sysml_action_usage = api.inherit('SysML ActionUsage', sysml_usage, {
    'action_definition': fields.String,
    'behavior': fields.List(fields.String),
    'nested_calculation': fields.List(fields.String),
    'nested_case': fields.List(fields.String),
    'nested_concern': fields.List(fields.String),
    'nested_constraint': fields.List(fields.String),
    'nested_enumeration': fields.List(fields.String),
    'nested_flow': fields.List(fields.String),
    'nested_interface': fields.List(fields.String),
    'nested_item': fields.List(fields.String),
    'nested_metadata': fields.List(fields.String),
    'nested_occurrence': fields.List(fields.String),
    'nested_reference': fields.List(fields.String),
    'nested_rendering': fields.List(fields.String),
    'nested_requirement': fields.List(fields.String),
    'nested_state': fields.List(fields.String),
    'nested_transition': fields.List(fields.String),
    'nested_use_case': fields.List(fields.String),
    'nested_verification_case': fields.List(fields.String),
    'nested_view': fields.List(fields.String),
    'nested_viewpoint': fields.List(fields.String),
})

sysml_state_definition = api.inherit('SysML StateDefinition', sysml_action_definition, {
    'state': fields.List(fields.String),
    'entry_action': fields.String,
    'do_action': fields.String,
    'exit_action': fields.String,
})

sysml_state_usage = api.inherit('SysML StateUsage', sysml_action_usage, {
    'state_definition': fields.String,
})

sysml_constraint_definition = api.inherit('SysML ConstraintDefinition', sysml_definition, {
    'is_negated': fields.Boolean,
})

sysml_constraint_usage = api.inherit('SysML ConstraintUsage', sysml_usage, {
    'is_negated': fields.Boolean,
    'constraint_definition': fields.String,
})

sysml_view_definition = api.inherit('SysML ViewDefinition', sysml_part_definition, {
    'view_condition': fields.String,
    'view_rendering': fields.String,
    'exposed_element': fields.List(fields.String),
})

sysml_view_usage = api.inherit('SysML ViewUsage', sysml_part_usage, {
    'view_definition': fields.String,
    'view_condition': fields.String,
    'view_rendering': fields.String,
    'exposed_element': fields.List(fields.String),
    'satisfied_viewpoint': fields.List(fields.String),
})

sysml_viewpoint_definition = api.inherit('SysML ViewpointDefinition', sysml_requirement_definition, {
    'viewpoint_stakeholder': fields.List(fields.String),
    'satisfied_viewpoint': fields.List(fields.String),
})

sysml_viewpoint_usage = api.inherit('SysML ViewpointUsage', sysml_requirement_usage, {
    'viewpoint_definition': fields.String,
    'viewpoint_stakeholder': fields.List(fields.String),
    'satisfied_viewpoint': fields.List(fields.String),
})

# --- Phase 8 models ---

sysml_feature = api.inherit('SysML Feature', sysml_definition, {
    'is_composite': fields.Boolean,
    'is_derived': fields.Boolean,
    'is_end': fields.Boolean,
    'is_ordered': fields.Boolean,
    'is_portion': fields.Boolean,
    'is_read_only': fields.Boolean,
    'is_unique': fields.Boolean,
    'direction': fields.String,
})

sysml_classifier = api.inherit('SysML Classifier', sysml_definition, {
    'is_variation': fields.Boolean,
})

sysml_occurrence_definition = api.inherit('SysML OccurrenceDefinition', sysml_definition, {
    'is_sufficient': fields.Boolean,
})

sysml_occurrence_usage = api.inherit('SysML OccurrenceUsage', sysml_usage, {
    'is_reference': fields.Boolean,
    'may_time_vary': fields.Boolean,
    'portion_kind': fields.String,
    'definition': fields.List(fields.String),
})

sysml_class = api.inherit('SysML Class', sysml_classifier, {})

sysml_structure = api.inherit('SysML Structure', sysml_class, {})

sysml_data_type = api.inherit('SysML DataType', sysml_classifier, {})

sysml_behavior = api.inherit('SysML Behavior', sysml_structure, {})

sysml_function = api.inherit('SysML Function', sysml_behavior, {})

sysml_predicate = api.inherit('SysML Predicate', sysml_function, {})

sysml_library_package = api.inherit('SysML LibraryPackage', sysml_package, {})

sysml_attribute_definition = api.inherit('SysML AttributeDefinition', sysml_definition, {})

sysml_attribute_usage = api.inherit('SysML AttributeUsage', sysml_usage, {})

sysml_enumeration_definition = api.inherit('SysML EnumerationDefinition', sysml_attribute_definition, {})

sysml_enumeration_usage = api.inherit('SysML EnumerationUsage', sysml_attribute_usage, {})

sysml_calculation_definition = api.inherit('SysML CalculationDefinition', sysml_action_definition, {})

sysml_calculation_usage = api.inherit('SysML CalculationUsage', sysml_action_usage, {})

sysml_case_definition = api.inherit('SysML CaseDefinition', sysml_calculation_definition, {})

sysml_case_usage = api.inherit('SysML CaseUsage', sysml_calculation_usage, {})

sysml_use_case_definition = api.inherit('SysML UseCaseDefinition', sysml_case_definition, {})

sysml_use_case_usage = api.inherit('SysML UseCaseUsage', sysml_case_usage, {})

sysml_analysis_case_definition = api.inherit('SysML AnalysisCaseDefinition', sysml_case_definition, {})

sysml_analysis_case_usage = api.inherit('SysML AnalysisCaseUsage', sysml_case_usage, {})

sysml_verification_case_definition = api.inherit('SysML VerificationCaseDefinition', sysml_case_definition, {})

sysml_verification_case_usage = api.inherit('SysML VerificationCaseUsage', sysml_case_usage, {})

sysml_connection_definition = api.inherit('SysML ConnectionDefinition', sysml_definition, {})

sysml_connection_usage = api.inherit('SysML ConnectionUsage', sysml_usage, {})

sysml_flow_definition = api.inherit('SysML FlowDefinition', sysml_connection_definition, {})

sysml_flow_usage = api.inherit('SysML FlowUsage', sysml_connection_usage, {})

sysml_interface_definition = api.inherit('SysML InterfaceDefinition', sysml_connection_definition, {})

sysml_interface_usage = api.inherit('SysML InterfaceUsage', sysml_connection_usage, {})

sysml_allocation_definition = api.inherit('SysML AllocationDefinition', sysml_connection_definition, {})

sysml_allocation_usage = api.inherit('SysML AllocationUsage', sysml_connection_usage, {})

sysml_rendering_definition = api.inherit('SysML RenderingDefinition', sysml_part_definition, {})

sysml_rendering_usage = api.inherit('SysML RenderingUsage', sysml_part_usage, {})

sysml_reference_usage = api.inherit('SysML ReferenceUsage', sysml_usage, {})

sysml_conjugated_port_definition = api.inherit('SysML ConjugatedPortDefinition', sysml_port_definition, {})

sysml_connector_as_usage = api.inherit('SysML ConnectorAsUsage', sysml_usage, {})

sysml_succession_as_usage = api.inherit('SysML SuccessionAsUsage', sysml_connector_as_usage, {})

sysml_binding_connector_as_usage = api.inherit('SysML BindingConnectorAsUsage', sysml_connector_as_usage, {})
