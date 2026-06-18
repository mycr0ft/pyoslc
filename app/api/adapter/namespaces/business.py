from rdflib import Graph, DCTERMS
from werkzeug.exceptions import NotFound

from app.api.adapter.exceptions import NotModified
from app.api.adapter.mappings.specification import specification_map
from app.api.adapter.resources.repository import get_requirement_repository
from pyoslc.resources.domains.rm import Requirement

attributes = specification_map


def _repo():
    return get_requirement_repository()


def get_requirement(base_url, specification_id):
    repo = _repo()
    requirement = repo.find(specification_id)
    if requirement:
        about = base_url.replace('selector', 'requirement')
        requirement.about = about
    return requirement


def get_requirement_list(base_url, select, where):
    repo = _repo()
    return repo.list()


def get_requirements(base_url):
    repo = _repo()
    return repo.list()


def create_requirement(data):
    if data:
        requirement = Requirement()
        if isinstance(data, Graph):
            requirement.from_rdf(data, attributes=attributes)
            identifier = [(s, o) for s, o in data.subject_objects(DCTERMS.identifier)][0]
            if identifier:
                requirement.identifier = identifier[1]
                requirement.about = identifier[0]
        else:
            requirement.from_json(data=data, attributes=attributes)

        repo = _repo()
        existing = repo.find(requirement.identifier)
        if existing:
            return NotModified()

        repo.create(requirement)
        return requirement

    return NotFound()


def update_requirement(requirement_id, data):
    if data:
        requirement = Requirement()
        if isinstance(data, Graph):
            requirement.from_rdf(data, attributes=attributes)
            identifier = [(s, o) for s, o in data.subject_objects(DCTERMS.identifier)][0]
            if identifier:
                requirement.identifier = identifier[1]
                requirement.about = identifier[0]
        else:
            requirement.from_json(data=data, attributes=attributes)

        repo = _repo()
        try:
            repo.update(str(requirement_id), requirement)
            return requirement
        except NotFound:
            raise NotModified()

    return NotFound()


def delete_requirement(requirement_id):
    repo = _repo()
    try:
        repo.delete(str(requirement_id))
        return True
    except NotFound:
        raise NotModified()


def get_field_names(path):
    if _repo().csv_path():
        import csv
        with open(_repo().csv_path(), 'rb') as f:
            reader = csv.DictReader(f, delimiter=';')
            field_names = reader.fieldnames
        return field_names if field_names else None
    return None


def update_store(id, data):
    pass
