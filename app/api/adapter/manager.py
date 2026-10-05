from app.api.adapter.services.specification import (
    Specification, StepSpecification, SysMLSpecification
)


class CSVImplementation(object):

    @classmethod
    def get_service_provider_info(cls):
        service_providers = [{
            'id': 'Project-1',
            'name': 'PyOSLC Service Provider for Project 1',
            'class': Specification
        }, {
            'id': 'SysML-1',
            'name': 'PyOSLC SysML Service Provider',
            'class': SysMLSpecification
        }, {
            'id': 'Step-1',
            'name': 'PyOSLC STEP Service Provider',
            'class': StepSpecification
        }]

        return service_providers

    @classmethod
    def get_configuration_info(cls):
        components = [{
            'id': 'Component-1',
            'name': 'PyOSLC Configuration Component'
        }]

        return components
