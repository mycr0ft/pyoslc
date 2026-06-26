from flask_restx import Namespace

from app.api.adapter.namespaces.sysml.routes import (
    SysMLElementList,
    SysMLElementItem,
    SysMLRelationshipList,
    SysMLRelationshipItem,
    SysMLPackageList,
    SysMLPackageItem,
    SysMLDefinitionList,
    SysMLDefinitionItem,
    SysMLUsageList,
    SysMLUsageItem,
    SysMLItemDefinitionList,
    SysMLItemDefinitionItem,
    SysMLItemUsageList,
    SysMLItemUsageItem,
    SysMLPartDefinitionList,
    SysMLPartDefinitionItem,
    SysMLPartUsageList,
    SysMLPartUsageItem,
    SysMLPortDefinitionList,
    SysMLPortDefinitionItem,
    SysMLPortUsageList,
    SysMLPortUsageItem,
    SysMLRequirementDefinitionList,
    SysMLRequirementDefinitionItem,
    SysMLRequirementUsageList,
    SysMLRequirementUsageItem,
    SysMLConcernDefinitionList,
    SysMLConcernDefinitionItem,
    SysMLConcernUsageList,
    SysMLConcernUsageItem,
    SysMLActionDefinitionList,
    SysMLActionDefinitionItem,
    SysMLActionUsageList,
    SysMLActionUsageItem,
    SysMLStateDefinitionList,
    SysMLStateDefinitionItem,
    SysMLStateUsageList,
    SysMLStateUsageItem,
    SysMLConstraintDefinitionList,
    SysMLConstraintDefinitionItem,
    SysMLConstraintUsageList,
    SysMLConstraintUsageItem,
    SysMLViewDefinitionList,
    SysMLViewDefinitionItem,
    SysMLViewUsageList,
    SysMLViewUsageItem,
    SysMLViewpointDefinitionList,
    SysMLViewpointDefinitionItem,
    SysMLViewpointUsageList,
    SysMLViewpointUsageItem,
    SysMLFeatureList,
    SysMLFeatureItem,
    SysMLClassifierList,
    SysMLClassifierItem,
    SysMLOccurrenceDefinitionList,
    SysMLOccurrenceDefinitionItem,
    SysMLOccurrenceUsageList,
    SysMLOccurrenceUsageItem,
    SysMLClassList,
    SysMLClassItem,
    SysMLStructureList,
    SysMLStructureItem,
    SysMLDataTypeList,
    SysMLDataTypeItem,
    SysMLBehaviorList,
    SysMLBehaviorItem,
    SysMLFunctionList,
    SysMLFunctionItem,
    SysMLPredicateList,
    SysMLPredicateItem,
    SysMLLibraryPackageList,
    SysMLLibraryPackageItem,
    SysMLAttributeDefinitionList,
    SysMLAttributeDefinitionItem,
    SysMLAttributeUsageList,
    SysMLAttributeUsageItem,
    SysMLEnumerationDefinitionList,
    SysMLEnumerationDefinitionItem,
    SysMLEnumerationUsageList,
    SysMLEnumerationUsageItem,
    SysMLCalculationDefinitionList,
    SysMLCalculationDefinitionItem,
    SysMLCalculationUsageList,
    SysMLCalculationUsageItem,
    SysMLCaseDefinitionList,
    SysMLCaseDefinitionItem,
    SysMLCaseUsageList,
    SysMLCaseUsageItem,
    SysMLUseCaseDefinitionList,
    SysMLUseCaseDefinitionItem,
    SysMLUseCaseUsageList,
    SysMLUseCaseUsageItem,
    SysMLAnalysisCaseDefinitionList,
    SysMLAnalysisCaseDefinitionItem,
    SysMLAnalysisCaseUsageList,
    SysMLAnalysisCaseUsageItem,
    SysMLVerificationCaseDefinitionList,
    SysMLVerificationCaseDefinitionItem,
    SysMLVerificationCaseUsageList,
    SysMLVerificationCaseUsageItem,
    SysMLConnectionDefinitionList,
    SysMLConnectionDefinitionItem,
    SysMLConnectionUsageList,
    SysMLConnectionUsageItem,
    SysMLFlowDefinitionList,
    SysMLFlowDefinitionItem,
    SysMLFlowUsageList,
    SysMLFlowUsageItem,
    SysMLInterfaceDefinitionList,
    SysMLInterfaceDefinitionItem,
    SysMLInterfaceUsageList,
    SysMLInterfaceUsageItem,
    SysMLAllocationDefinitionList,
    SysMLAllocationDefinitionItem,
    SysMLAllocationUsageList,
    SysMLAllocationUsageItem,
    SysMLRenderingDefinitionList,
    SysMLRenderingDefinitionItem,
    SysMLRenderingUsageList,
    SysMLRenderingUsageItem,
    SysMLReferenceUsageList,
    SysMLReferenceUsageItem,
    SysMLConjugatedPortDefinitionList,
    SysMLConjugatedPortDefinitionItem,
    SysMLConnectorAsUsageList,
    SysMLConnectorAsUsageItem,
    SysMLSuccessionAsUsageList,
    SysMLSuccessionAsUsageItem,
    SysMLBindingConnectorAsUsageList,
    SysMLBindingConnectorAsUsageItem,
)

sysml_ns = Namespace(name='sysml', description='SysML v2 Domain', path='/sysml')

sysml_ns.add_resource(SysMLElementList, "/element")
sysml_ns.add_resource(SysMLElementItem, "/element/<string:id>")
sysml_ns.add_resource(SysMLRelationshipList, "/relationship")
sysml_ns.add_resource(SysMLRelationshipItem, "/relationship/<string:id>")
sysml_ns.add_resource(SysMLPackageList, "/package")
sysml_ns.add_resource(SysMLPackageItem, "/package/<string:id>")
sysml_ns.add_resource(SysMLDefinitionList, "/definition")
sysml_ns.add_resource(SysMLDefinitionItem, "/definition/<string:id>")
sysml_ns.add_resource(SysMLUsageList, "/usage")
sysml_ns.add_resource(SysMLUsageItem, "/usage/<string:id>")
sysml_ns.add_resource(SysMLItemDefinitionList, "/itemDefinition")
sysml_ns.add_resource(SysMLItemDefinitionItem, "/itemDefinition/<string:id>")
sysml_ns.add_resource(SysMLItemUsageList, "/itemUsage")
sysml_ns.add_resource(SysMLItemUsageItem, "/itemUsage/<string:id>")
sysml_ns.add_resource(SysMLPartDefinitionList, "/partDefinition")
sysml_ns.add_resource(SysMLPartDefinitionItem, "/partDefinition/<string:id>")
sysml_ns.add_resource(SysMLPartUsageList, "/partUsage")
sysml_ns.add_resource(SysMLPartUsageItem, "/partUsage/<string:id>")
sysml_ns.add_resource(SysMLPortDefinitionList, "/portDefinition")
sysml_ns.add_resource(SysMLPortDefinitionItem, "/portDefinition/<string:id>")
sysml_ns.add_resource(SysMLPortUsageList, "/portUsage")
sysml_ns.add_resource(SysMLPortUsageItem, "/portUsage/<string:id>")
sysml_ns.add_resource(SysMLRequirementDefinitionList, "/requirementDefinition")
sysml_ns.add_resource(SysMLRequirementDefinitionItem, "/requirementDefinition/<string:id>")
sysml_ns.add_resource(SysMLRequirementUsageList, "/requirementUsage")
sysml_ns.add_resource(SysMLRequirementUsageItem, "/requirementUsage/<string:id>")
sysml_ns.add_resource(SysMLConcernDefinitionList, "/concernDefinition")
sysml_ns.add_resource(SysMLConcernDefinitionItem, "/concernDefinition/<string:id>")
sysml_ns.add_resource(SysMLConcernUsageList, "/concernUsage")
sysml_ns.add_resource(SysMLConcernUsageItem, "/concernUsage/<string:id>")
sysml_ns.add_resource(SysMLActionDefinitionList, "/actionDefinition")
sysml_ns.add_resource(SysMLActionDefinitionItem, "/actionDefinition/<string:id>")
sysml_ns.add_resource(SysMLActionUsageList, "/actionUsage")
sysml_ns.add_resource(SysMLActionUsageItem, "/actionUsage/<string:id>")
sysml_ns.add_resource(SysMLStateDefinitionList, "/stateDefinition")
sysml_ns.add_resource(SysMLStateDefinitionItem, "/stateDefinition/<string:id>")
sysml_ns.add_resource(SysMLStateUsageList, "/stateUsage")
sysml_ns.add_resource(SysMLStateUsageItem, "/stateUsage/<string:id>")
sysml_ns.add_resource(SysMLConstraintDefinitionList, "/constraintDefinition")
sysml_ns.add_resource(SysMLConstraintDefinitionItem, "/constraintDefinition/<string:id>")
sysml_ns.add_resource(SysMLConstraintUsageList, "/constraintUsage")
sysml_ns.add_resource(SysMLConstraintUsageItem, "/constraintUsage/<string:id>")
sysml_ns.add_resource(SysMLViewDefinitionList, "/viewDefinition")
sysml_ns.add_resource(SysMLViewDefinitionItem, "/viewDefinition/<string:id>")
sysml_ns.add_resource(SysMLViewUsageList, "/viewUsage")
sysml_ns.add_resource(SysMLViewUsageItem, "/viewUsage/<string:id>")
sysml_ns.add_resource(SysMLViewpointDefinitionList, "/viewpointDefinition")
sysml_ns.add_resource(SysMLViewpointDefinitionItem, "/viewpointDefinition/<string:id>")
sysml_ns.add_resource(SysMLViewpointUsageList, "/viewpointUsage")
sysml_ns.add_resource(SysMLViewpointUsageItem, "/viewpointUsage/<string:id>")
sysml_ns.add_resource(SysMLFeatureList, "/feature")
sysml_ns.add_resource(SysMLFeatureItem, "/feature/<string:id>")
sysml_ns.add_resource(SysMLClassifierList, "/classifier")
sysml_ns.add_resource(SysMLClassifierItem, "/classifier/<string:id>")
sysml_ns.add_resource(SysMLOccurrenceDefinitionList, "/occurrenceDefinition")
sysml_ns.add_resource(SysMLOccurrenceDefinitionItem, "/occurrenceDefinition/<string:id>")
sysml_ns.add_resource(SysMLOccurrenceUsageList, "/occurrenceUsage")
sysml_ns.add_resource(SysMLOccurrenceUsageItem, "/occurrenceUsage/<string:id>")
sysml_ns.add_resource(SysMLClassList, "/class")
sysml_ns.add_resource(SysMLClassItem, "/class/<string:id>")
sysml_ns.add_resource(SysMLStructureList, "/structure")
sysml_ns.add_resource(SysMLStructureItem, "/structure/<string:id>")
sysml_ns.add_resource(SysMLDataTypeList, "/dataType")
sysml_ns.add_resource(SysMLDataTypeItem, "/dataType/<string:id>")
sysml_ns.add_resource(SysMLBehaviorList, "/behavior")
sysml_ns.add_resource(SysMLBehaviorItem, "/behavior/<string:id>")
sysml_ns.add_resource(SysMLFunctionList, "/function")
sysml_ns.add_resource(SysMLFunctionItem, "/function/<string:id>")
sysml_ns.add_resource(SysMLPredicateList, "/predicate")
sysml_ns.add_resource(SysMLPredicateItem, "/predicate/<string:id>")
sysml_ns.add_resource(SysMLLibraryPackageList, "/libraryPackage")
sysml_ns.add_resource(SysMLLibraryPackageItem, "/libraryPackage/<string:id>")
sysml_ns.add_resource(SysMLAttributeDefinitionList, "/attributeDefinition")
sysml_ns.add_resource(SysMLAttributeDefinitionItem, "/attributeDefinition/<string:id>")
sysml_ns.add_resource(SysMLAttributeUsageList, "/attributeUsage")
sysml_ns.add_resource(SysMLAttributeUsageItem, "/attributeUsage/<string:id>")
sysml_ns.add_resource(SysMLEnumerationDefinitionList, "/enumerationDefinition")
sysml_ns.add_resource(SysMLEnumerationDefinitionItem, "/enumerationDefinition/<string:id>")
sysml_ns.add_resource(SysMLEnumerationUsageList, "/enumerationUsage")
sysml_ns.add_resource(SysMLEnumerationUsageItem, "/enumerationUsage/<string:id>")
sysml_ns.add_resource(SysMLCalculationDefinitionList, "/calculationDefinition")
sysml_ns.add_resource(SysMLCalculationDefinitionItem, "/calculationDefinition/<string:id>")
sysml_ns.add_resource(SysMLCalculationUsageList, "/calculationUsage")
sysml_ns.add_resource(SysMLCalculationUsageItem, "/calculationUsage/<string:id>")
sysml_ns.add_resource(SysMLCaseDefinitionList, "/caseDefinition")
sysml_ns.add_resource(SysMLCaseDefinitionItem, "/caseDefinition/<string:id>")
sysml_ns.add_resource(SysMLCaseUsageList, "/caseUsage")
sysml_ns.add_resource(SysMLCaseUsageItem, "/caseUsage/<string:id>")
sysml_ns.add_resource(SysMLUseCaseDefinitionList, "/useCaseDefinition")
sysml_ns.add_resource(SysMLUseCaseDefinitionItem, "/useCaseDefinition/<string:id>")
sysml_ns.add_resource(SysMLUseCaseUsageList, "/useCaseUsage")
sysml_ns.add_resource(SysMLUseCaseUsageItem, "/useCaseUsage/<string:id>")
sysml_ns.add_resource(SysMLAnalysisCaseDefinitionList, "/analysisCaseDefinition")
sysml_ns.add_resource(SysMLAnalysisCaseDefinitionItem, "/analysisCaseDefinition/<string:id>")
sysml_ns.add_resource(SysMLAnalysisCaseUsageList, "/analysisCaseUsage")
sysml_ns.add_resource(SysMLAnalysisCaseUsageItem, "/analysisCaseUsage/<string:id>")
sysml_ns.add_resource(SysMLVerificationCaseDefinitionList, "/verificationCaseDefinition")
sysml_ns.add_resource(SysMLVerificationCaseDefinitionItem, "/verificationCaseDefinition/<string:id>")
sysml_ns.add_resource(SysMLVerificationCaseUsageList, "/verificationCaseUsage")
sysml_ns.add_resource(SysMLVerificationCaseUsageItem, "/verificationCaseUsage/<string:id>")
sysml_ns.add_resource(SysMLConnectionDefinitionList, "/connectionDefinition")
sysml_ns.add_resource(SysMLConnectionDefinitionItem, "/connectionDefinition/<string:id>")
sysml_ns.add_resource(SysMLConnectionUsageList, "/connectionUsage")
sysml_ns.add_resource(SysMLConnectionUsageItem, "/connectionUsage/<string:id>")
sysml_ns.add_resource(SysMLFlowDefinitionList, "/flowDefinition")
sysml_ns.add_resource(SysMLFlowDefinitionItem, "/flowDefinition/<string:id>")
sysml_ns.add_resource(SysMLFlowUsageList, "/flowUsage")
sysml_ns.add_resource(SysMLFlowUsageItem, "/flowUsage/<string:id>")
sysml_ns.add_resource(SysMLInterfaceDefinitionList, "/interfaceDefinition")
sysml_ns.add_resource(SysMLInterfaceDefinitionItem, "/interfaceDefinition/<string:id>")
sysml_ns.add_resource(SysMLInterfaceUsageList, "/interfaceUsage")
sysml_ns.add_resource(SysMLInterfaceUsageItem, "/interfaceUsage/<string:id>")
sysml_ns.add_resource(SysMLAllocationDefinitionList, "/allocationDefinition")
sysml_ns.add_resource(SysMLAllocationDefinitionItem, "/allocationDefinition/<string:id>")
sysml_ns.add_resource(SysMLAllocationUsageList, "/allocationUsage")
sysml_ns.add_resource(SysMLAllocationUsageItem, "/allocationUsage/<string:id>")
sysml_ns.add_resource(SysMLRenderingDefinitionList, "/renderingDefinition")
sysml_ns.add_resource(SysMLRenderingDefinitionItem, "/renderingDefinition/<string:id>")
sysml_ns.add_resource(SysMLRenderingUsageList, "/renderingUsage")
sysml_ns.add_resource(SysMLRenderingUsageItem, "/renderingUsage/<string:id>")
sysml_ns.add_resource(SysMLReferenceUsageList, "/referenceUsage")
sysml_ns.add_resource(SysMLReferenceUsageItem, "/referenceUsage/<string:id>")
sysml_ns.add_resource(SysMLConjugatedPortDefinitionList, "/conjugatedPortDefinition")
sysml_ns.add_resource(SysMLConjugatedPortDefinitionItem, "/conjugatedPortDefinition/<string:id>")
sysml_ns.add_resource(SysMLConnectorAsUsageList, "/connectorAsUsage")
sysml_ns.add_resource(SysMLConnectorAsUsageItem, "/connectorAsUsage/<string:id>")
sysml_ns.add_resource(SysMLSuccessionAsUsageList, "/successionAsUsage")
sysml_ns.add_resource(SysMLSuccessionAsUsageItem, "/successionAsUsage/<string:id>")
sysml_ns.add_resource(SysMLBindingConnectorAsUsageList, "/bindingConnectorAsUsage")
sysml_ns.add_resource(SysMLBindingConnectorAsUsageItem, "/bindingConnectorAsUsage/<string:id>")
