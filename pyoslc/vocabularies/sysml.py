from rdflib import URIRef
from rdflib.namespace import ClosedNamespace

OSLC_SYSML = ClosedNamespace(
    uri=URIRef("https://www.omg.org/spec/sysml/vocabulary#"),
    terms=[
        # Classes - Core
        "Element", "Relationship", "Namespace", "Type", "Feature",
        "Classifier", "Class", "Structure", "Definition", "Usage",

        # Classes - Namespace/Package
        "Package", "LibraryPackage",

        # Classes - Type hierarchy
        "DataType", "Behavior", "Function", "Predicate",
        "OccurrenceDefinition", "OccurrenceUsage",
        "ItemDefinition", "ItemUsage",
        "PartDefinition", "PartUsage",
        "PortDefinition", "PortUsage",
        "AttributeDefinition", "AttributeUsage",
        "EnumerationDefinition", "EnumerationUsage",

        # Classes - Definition/Usage pairs
        "ActionDefinition", "ActionUsage",
        "ConstraintDefinition", "ConstraintUsage",
        "RequirementDefinition", "RequirementUsage",
        "CalculationDefinition", "CalculationUsage",
        "CaseDefinition", "CaseUsage",
        "StateDefinition", "StateUsage",
        "ConnectionDefinition", "ConnectionUsage",
        "FlowDefinition", "FlowUsage",
        "InterfaceDefinition", "InterfaceUsage",
        "AllocationDefinition", "AllocationUsage",
        "ViewDefinition", "ViewUsage",
        "ViewpointDefinition", "ViewpointUsage",
        "ConcernDefinition", "ConcernUsage",
        "UseCaseDefinition", "UseCaseUsage",
        "AnalysisCaseDefinition", "AnalysisCaseUsage",
        "VerificationCaseDefinition", "VerificationCaseUsage",
        "RenderingDefinition", "RenderingUsage",
        "ReferenceUsage",

        # Classes - Membership
        "Membership", "OwningMembership", "FeatureMembership",
        "ParameterMembership", "EndFeatureMembership",
        "ActorMembership", "ObjectiveMembership",
        "StakeholderMembership", "SubjectMembership",
        "ReturnParameterMembership",
        "RequirementConstraintMembership",
        "VariantMembership",
        "ElementFilterMembership",
        "StateSubactionMembership",
        "TransitionFeatureMembership",
        "ViewRenderingMembership",
        "FramedConcernMembership",
        "ResultExpressionMembership",
        "RequirementVerificationMembership",

        # Classes - Relationship subtypes
        "Annotation", "Dependency", "Conjugation", "PortConjugation",
        "Specialization", "Subclassification",
        "Subsetting", "Redefinition", "ReferenceSubsetting",
        "CrossSubsetting",
        "FeatureTyping", "ConjugatedPortTyping",
        "FeatureChaining", "FeatureInverting",
        "TypeFeaturing",
        "Differencing", "Intersecting", "Unioning", "Disjoining",
        "Import", "MembershipImport", "NamespaceImport",
        "Expose", "MembershipExpose", "NamespaceExpose",
        "FeatureValue", "Connector", "Flow", "Succession",
        "Association", "AssociationStructure",
        "Invariant", "Multiplicity", "MultiplicityRange",
        "MetadataFeature", "MetadataDefinition", "MetadataUsage",
        "Metaclass",

        # Classes - Annotating
        "AnnotatingElement", "Comment", "Documentation",
        "TextualRepresentation",

        # Classes - Expressions
        "Expression", "Step", "BooleanExpression",
        "LiteralExpression", "LiteralBoolean", "LiteralInteger",
        "LiteralString", "LiteralRational", "LiteralInfinity",
        "OperatorExpression", "InvocationExpression",
        "InstantiationExpression", "FeatureReferenceExpression",
        "NullExpression", "SelectExpression",
        "CollectExpression", "IndexExpression",
        "FeatureChainExpression", "ConstructorExpression",
        "TriggerInvocationExpression", "MetadataAccessExpression",

        # Classes - Control/Action
        "ControlNode", "DecisionNode", "ForkNode", "JoinNode",
        "MergeNode",
        "LoopActionUsage", "WhileLoopActionUsage", "ForLoopActionUsage",
        "IfActionUsage", "AcceptActionUsage", "SendActionUsage",
        "AssignmentActionUsage", "TerminateActionUsage",
        "PerformActionUsage", "ExhibitStateUsage",
        "AssertConstraintUsage", "SatisfyRequirementUsage",
        "TransitionUsage", "EventOccurrenceUsage",
        "IncludeUseCaseUsage", "FlowEnd", "PayloadFeature",

        # Classes - Interaction/Flow
        "Interaction", "SuccessionFlow", "SuccessionFlowUsage",
        "SuccessionAsUsage", "ConnectorAsUsage",
        "BindingConnector", "BindingConnectorAsUsage",
        "ConjugatedPortDefinition",

        # Classes - Misc
        "FlowUsage", "StateUsage",

        # Properties - Identity/Name
        "elementId", "aliasIds",
        "declaredName", "declaredShortName",
        "name", "shortName", "qualifiedName",

        # Properties - Boolean flags
        "isImpliedIncluded", "isLibraryElement",
        "isImplied", "isAbstract", "isConjugated", "isSufficient",
        "isComposite", "isConstant", "isDerived", "isEnd",
        "isOrdered", "isPortion", "isReference", "isUnique",
        "isVariable", "isVariation", "isIndividual",
        "isNegated", "isDefault", "isInitial", "isStandard",
        "isImportAll", "isRecursive", "isParallel",
        "isModelLevelEvaluable", "mayTimeVary",

        # Properties - Ownership/Containment
        "owner", "owningNamespace", "owningMembership",
        "owningRelationship",
        "ownedElement", "ownedRelationship", "ownedAnnotation",
        "ownedMember", "ownedMemberElement",
        "ownedMemberName", "ownedMemberShortName",
        "ownedMemberElementId",
        "owningRelatedElement", "ownedRelatedElement",

        # Properties - Membership
        "member", "membership",
        "memberElement", "memberName", "memberShortName",
        "memberElementId",
        "membershipOwningNamespace",
        "ownedMembership", "ownedFeatureMembership",
        "featureMembership", "inheritedMembership",
        "importedMembership",
        "visibility",

        # Properties - Relationship
        "source", "target",
        "relatedElement",

        # Properties - Type/Feature
        "feature", "directedFeature", "endFeature",
        "ownedFeature", "ownedEndFeature",
        "inheritedFeature",
        "input", "output",
        "multiplicity",
        "featureTarget", "endOwningType",
        "owningType", "owningFeatureMembership",
        "direction",
        "crossFeature",

        # Properties - Typing/Specialization
        "type",
        "ownedTyping", "typedFeature",
        "ownedSpecialization", "ownedSubclassification",
        "ownedConjugator", "ownedDifferencing",
        "ownedDisjoining", "ownedIntersecting", "ownedUnioning",
        "general", "specific",
        "subclassifier", "superclassifier",
        "subsettedFeature", "subsettingFeature",
        "redefinedFeature", "redefiningFeature",
        "featureOfType",

        # Properties - Feature relationships
        "ownedSubsetting", "ownedRedefinition",
        "ownedReferenceSubsetting",
        "ownedFeatureChaining", "ownedFeatureInverting",
        "ownedCrossSubsetting", "ownedTypeFeaturing",
        "chainingFeature",
        "featureInverted", "invertingFeature",
        "featureChained",
        "crossingFeature", "crossedFeature",
        "featuringType", "defaultFeaturingType",
        "conjugatedType", "originalType",

        # Properties - Usage
        "definition", "owningDefinition", "owningUsage",
        "portionKind",
        "individualDefinition",
        "occurrenceDefinition",

        # Properties - Nested usages
        "nestedAction", "nestedAllocation",
        "nestedAnalysisCase", "nestedAttribute",
        "nestedCalculation", "nestedCase",
        "nestedConcern", "nestedConnection",
        "nestedConstraint", "nestedEnumeration",
        "nestedFlow", "nestedInterface",
        "nestedItem", "nestedMetadata",
        "nestedOccurrence", "nestedPart",
        "nestedPort", "nestedReference",
        "nestedRendering", "nestedRequirement",
        "nestedState", "nestedTransition",
        "nestedUsage", "nestedUseCase",
        "nestedVerificationCase", "nestedView",
        "nestedViewpoint",

        # Properties - Owned usages (definitions)
        "ownedAction", "ownedAllocation",
        "ownedAnalysisCase", "ownedAttribute",
        "ownedCalculation", "ownedCase",
        "ownedConcern", "ownedConnection",
        "ownedConstraint", "ownedEnumeration",
        "ownedFlow", "ownedInterface",
        "ownedItem", "ownedMetadata",
        "ownedOccurrence", "ownedPart",
        "ownedPort", "ownedReference",
        "ownedRendering", "ownedRequirement",
        "ownedState", "ownedTransition",
        "ownedUsage", "ownedUseCase",
        "ownedVerificationCase", "ownedView",
        "ownedViewpoint",
        "ownedEnumeration",

        # Properties - Connector/Flow
        "connectorEnd", "associationEnd",
        "connectionEnd", "interfaceEnd",
        "sourceFeature", "targetFeature",
        "sourceType", "targetType",
        "sourceOutputFeature", "targetInputFeature",
        "payloadType", "payloadFeature",
        "payloadParameter", "payloadArgument",
        "senderArgument",
        "flowEnd",

        # Properties - Action/Control
        "action", "behavior", "step", "parameter",
        "bodyAction", "thenAction", "elseAction",
        "ifArgument", "whileArgument", "untilArgument",
        "loopVariable", "seqArgument",
        "guardExpression", "triggerAction", "effectAction",
        "entryAction", "exitAction", "doAction",
        "transitionFeature",
        "receiverArgument", "terminatedOccurrenceArgument",
        "valueExpression", "targetArgument",

        # Properties - State
        "state",
        "stateDefinition",

        # Properties - Requirement
        "reqId", "text",
        "assumedConstraint", "requiredConstraint",
        "framedConcern", "referencedConcern",
        "objectiveRequirement",
        "ownedObjectiveRequirement",
        "ownedStakeholderParameter",
        "ownedSubjectParameter",
        "ownedActorParameter",
        "ownedMemberParameter",
        "stakeholderParameter", "subjectParameter",
        "actorParameter",
        "referencedRendering",
        "viewpointStakeholder",

        # Properties - Expression
        "result", "resultExpression",
        "ownedResultExpression",
        "expression", "operator",
        "argument", "condition",
        "bound", "lowerBound", "upperBound",
        "function", "predicate",
        "instantiatedType",
        "referent", "referencedFeature",
        "referencingFeature",
        "representedElement",
        "documentedElement",
        "annotatedElement", "annotatingElement",
        "owningAnnotatedElement",
        "owningAnnotatingElement",
        "owningAnnotatingRelationship",
        "ownedAnnotatingElement",
        "ownedAnnotatingRelationship",

        # Properties - Import
        "importOwningNamespace",
        "importedNamespace", "importedElement",
        "filterCondition",
        "exposedElement",

        # Properties - Misc
        "kind", "when",
        "body", "language", "locale",
        "originalPortDefinition",
        "conjugatedPortDefinition",
        "ownedPortConjugator",
        "includedUseCase", "useCaseIncluded",
        "performedAction", "exhibitedState",
        "satisfiedRequirement", "satisfyingFeature",
        "satisfiedViewpoint",
        "verifiedRequirement",
        "referencedConstraint", "assertedConstraint",
        "variant", "variantMembership",
        "enumeratedValue", "enumerationDefinition",
        "actionDefinition", "calculationDefinition",
        "caseDefinition", "concernDefinition",
        "connectionDefinition", "constraintDefinition",
        "flowDefinition", "interfaceDefinition",
        "itemDefinition", "metadataDefinition",
        "partDefinition", "portDefinition",
        "renderingDefinition", "requirementDefinition",
        "stateDefinition", "useCaseDefinition",
        "verificationCaseDefinition", "viewDefinition",
        "viewpointDefinition", "allocationDefinition",
        "ownedVariantUsage",
        "usage", "directedUsage",
        "owningClassifier",
        "association", "interaction",
        "metaclass",
        "typeDifferenced", "typeDisjoined",
        "typeIntersected", "typeUnioned",
        "unioningType", "differencingType",
        "intersectingType", "disjoiningType",
        "view", "viewCondition", "viewRendering",
        "viewDefinition",
        "succession",
        "value",

        # OSLC linking properties (used in shapes)
        "derives", "elaborates", "external",
        "refine", "satisfy", "trace",

        # Ordering property for reification
        "order",

        # Individuals - FeatureDirectionKind
        "in", "out", "inout",

        # Individuals - VisibilityKind
        "public", "protected", "private",

        # Individuals - TriggerKind
        "after", "at",

        # Individuals - RequirementConstraintKind
        "assumption", "requirement",

        # Individuals - StateSubactionKind
        "entry", "do", "exit",

        # Individuals - TransitionFeatureKind
        "trigger", "guard", "effect",

        # Individuals - PortionKind
        "snapshot", "timeslice",
    ]
)
