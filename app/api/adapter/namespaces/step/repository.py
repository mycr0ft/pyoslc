# -*- coding: utf-8 -*-
"""STEP-domain repository (same ABC pattern as the SysML one)."""

from abc import ABC, abstractmethod


class StepRepository(ABC):

    def __init__(self, title):
        self.title = title

    @abstractmethod
    def find(self, identifier: str):
        ...

    @abstractmethod
    def list(self):
        ...

    @abstractmethod
    def list_by_type(self, resource_class):
        ...

    @abstractmethod
    def create(self, resource):
        ...

    @abstractmethod
    def update(self, identifier: str, resource):
        ...

    @abstractmethod
    def delete(self, identifier: str) -> bool:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...


class InMemoryStepRepository(StepRepository):
    """Process-local store; the seeder loads stepper's P1 output at
    startup. Same lifecycle guarantees as the SysML in-memory repo."""

    def __init__(self, title="step-in-memory"):
        super().__init__(title)
        self._resources = {}
        self._files = {}    # file_ref -> StepFile resources (keyed id: file:NAME)

    def find(self, identifier: str):
        if identifier in self._resources:
            return self._resources[identifier]
        for store in (self._resources, self._files):
            if identifier in store:
                return store[identifier]
        return None

    def list(self):
        return list(self._resources.values()) + list(self._files.values())

    def list_by_type(self, resource_class):
        return [r for r in self.list() if isinstance(r, resource_class)]

    def create(self, resource):
        if not getattr(resource, "identifier", None):
            raise ValueError("identifier is required")
        key, store = self._store_for(resource)
        if resource.identifier in store:
            raise ValueError(f"{key} {resource.identifier} already exists")
        store[resource.identifier] = resource
        return resource

    def update(self, identifier: str, resource):
        key, store = self._store_for(resource)
        if identifier not in store:
            from werkzeug.exceptions import NotFound
            raise NotFound(f"{key} {identifier} not found")
        store[identifier] = resource
        return resource

    def delete(self, identifier: str) -> bool:
        from werkzeug.exceptions import NotFound
        for store in (self._resources, self._files):
            if identifier in store:
                del store[identifier]
                return True
        raise NotFound(f"{identifier} not found")

    def clear(self):
        self._resources = {}
        self._files = {}

    def _store_for(self, resource):
        from pyoslc.resources.domains.step import StepFile
        if isinstance(resource, StepFile):
            return "StepFile", self._files
        return "resource", self._resources


_repository = None


def get_step_repository():
    global _repository
    if _repository is None:
        _repository = InMemoryStepRepository()
    return _repository


def set_step_repository(repo) -> None:
    """Install a custom backend (test/oxigraph hook, mirrors sysml)."""
    global _repository
    _repository = repo