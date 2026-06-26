from abc import ABC, abstractmethod


class SysMLElementRepository(ABC):

    def __init__(self, title):
        self.title = title

    @abstractmethod
    def find(self, element_id: str):
        ...

    @abstractmethod
    def list(self):
        ...

    @abstractmethod
    def create(self, element):
        ...

    @abstractmethod
    def update(self, element_id: str, element):
        ...

    @abstractmethod
    def delete(self, element_id: str) -> bool:
        ...


class SysMLRelationshipRepository(ABC):

    def __init__(self, title):
        self.title = title

    @abstractmethod
    def find(self, relationship_id: str):
        ...

    @abstractmethod
    def list(self):
        ...

    @abstractmethod
    def create(self, relationship):
        ...

    @abstractmethod
    def update(self, relationship_id: str, relationship):
        ...

    @abstractmethod
    def delete(self, relationship_id: str) -> bool:
        ...


class InMemorySysMLRepository(SysMLElementRepository, SysMLRelationshipRepository):

    def __init__(self, title='sysml-in-memory'):
        super().__init__(title)
        self._elements = {}
        self._relationships = {}

    def find(self, element_id: str):
        if element_id in self._elements:
            return self._elements[element_id]
        if element_id in self._relationships:
            return self._relationships[element_id]
        return None

    def list(self):
        return list(self._elements.values()) + list(self._relationships.values())

    def list_elements(self):
        return list(self._elements.values())

    def list_relationships(self):
        return list(self._relationships.values())

    def create(self, resource):
        from pyoslc.resources.domains.sysml import SysMLRelationship
        identifier = resource.identifier
        if not identifier:
            raise ValueError('identifier is required')
        if isinstance(resource, SysMLRelationship):
            if identifier in self._relationships:
                raise ValueError(f'Relationship {identifier} already exists')
            self._relationships[identifier] = resource
        else:
            if identifier in self._elements:
                raise ValueError(f'Element {identifier} already exists')
            self._elements[identifier] = resource
        return resource

    def update(self, element_id: str, resource):
        from pyoslc.resources.domains.sysml import SysMLRelationship
        if isinstance(resource, SysMLRelationship):
            if element_id not in self._relationships:
                from werkzeug.exceptions import NotFound
                raise NotFound(f'Relationship {element_id} not found')
            self._relationships[element_id] = resource
        else:
            if element_id not in self._elements:
                from werkzeug.exceptions import NotFound
                raise NotFound(f'Element {element_id} not found')
            self._elements[element_id] = resource
        return resource

    def delete(self, element_id: str) -> bool:
        if element_id in self._elements:
            del self._elements[element_id]
            return True
        if element_id in self._relationships:
            del self._relationships[element_id]
            return True
        from werkzeug.exceptions import NotFound
        raise NotFound(f'Element {element_id} not found')


_repository = None


def get_sysml_repository():
    global _repository
    if _repository is None:
        _repository = InMemorySysMLRepository()
    return _repository
