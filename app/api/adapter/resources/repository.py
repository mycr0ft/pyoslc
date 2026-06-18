from abc import ABC, abstractmethod


class Repository(object):

    def __init__(self, title):
        self.title = title

    def get(self):
        pass


class RequirementRepository(ABC):

    def __init__(self, title):
        self.title = title

    @abstractmethod
    def find(self, requirement_id: str):
        ...

    @abstractmethod
    def list(self):
        ...

    @abstractmethod
    def create(self, requirement):
        """Create and return the requirement. Raises if duplicate."""
        ...

    @abstractmethod
    def update(self, requirement_id: str, requirement):
        """Update and return the requirement. Raises if not found."""
        ...

    @abstractmethod
    def delete(self, requirement_id: str) -> bool:
        """Delete and return True. Raises if not found."""
        ...

    @abstractmethod
    def csv_path(self):
        """Return the CSV file path if backed by CSV, else None."""
        ...


def get_requirement_repository(app=None):
    """Factory: return the RequirementRepository implementation configured for the app."""
    if app is None:
        from flask import current_app
        app = current_app

    backend = app.config.get('STORAGE_BACKEND', 'csv')

    if backend == 'oxigraph':
        from app.api.adapter.namespaces.rm.oxigraph_requirement_repository import OxigraphRequirementRepository
        return OxigraphRequirementRepository(
            'oxigraph-requirements',
            url=app.config.get('OXYGRAPH_URL', 'http://127.0.0.1:7878'),
        )

    from app.api.adapter.namespaces.rm.csv_requirement_repository import CsvRequirementRepository
    return CsvRequirementRepository(
        'csv-requirements',
        csv_file_path=app.config.get('CSV_REQUIREMENT_PATH'),
    )
