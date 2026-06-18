import logging

import requests
from pyoxigraph import Store
from rdflib import Graph, RDF, DCTERMS
from rdflib.plugin import PluginException

from app.api.adapter.mappings.specification import specification_map
from app.api.adapter.resources.repository import RequirementRepository
from pyoslc.resources.domains.rm import Requirement
from pyoslc.vocabularies.core import OSLC
from pyoslc.vocabularies.rm import OSLC_RM

logger = logging.getLogger(__name__)

attributes = specification_map

REQUIREMENT_GRAPH_URI = 'urn:requirements'


class OxigraphRequirementRepository(RequirementRepository):

    def __init__(self, title: str, url: str = 'http://127.0.0.1:7878'):
        super().__init__(title)
        self.url = url.rstrip('/')
        self._store = Store(self.url)
        self._sparql_endpoint = f'{self.url}/query'
        self._update_endpoint = f'{self.url}/update'

    def csv_path(self):
        return None

    def _sparql_query(self, query: str) -> list[dict]:
        r = requests.post(
            self._sparql_endpoint,
            data={'query': query},
            headers={'Accept': 'application/sparql-results+json'},
        )
        r.raise_for_status()
        return r.json()['results']['bindings']

    def _sparql_update(self, query: str):
        r = requests.post(
            self._update_endpoint,
            data={'update': query},
        )
        r.raise_for_status()

    def _graph_for_id(self, requirement_id: str) -> Graph | None:
        query = (
            f'CONSTRUCT {{ ?s ?p ?o }} FROM <{REQUIREMENT_GRAPH_URI}> '
            f'WHERE {{ ?s ?p ?o . '
            f'?s <{DCTERMS.identifier}> "{requirement_id}"^^<http://www.w3.org/2001/XMLSchema#string> . '
            f'}}'
        )
        r = requests.post(
            self._sparql_endpoint,
            data={'query': query},
            headers={'Accept': 'text/turtle'},
        )
        if r.status_code != 200 or not r.text.strip():
            return None
        g = Graph()
        try:
            g.parse(data=r.text, format='turtle')
        except PluginException:
            return None
        return g

    def _all_graph(self) -> Graph:
        query = f'CONSTRUCT {{ ?s ?p ?o }} FROM <{REQUIREMENT_GRAPH_URI}> WHERE {{ ?s ?p ?o }}'
        r = requests.post(
            self._sparql_endpoint,
            data={'query': query},
            headers={'Accept': 'text/turtle'},
        )
        g = Graph()
        if r.status_code == 200 and r.text.strip():
            try:
                g.parse(data=r.text, format='turtle')
            except PluginException:
                pass
        return g

    def _requirement_from_graph(self, g: Graph) -> Requirement | None:
        for s in g.subjects(RDF.type, OSLC_RM.Requirement):
            req = Requirement()
            req.from_rdf(g, attributes)
            return req
        return None

    def find(self, requirement_id: str) -> Requirement | None:
        g = self._graph_for_id(requirement_id)
        if g is None:
            return None
        return self._requirement_from_graph(g)

    def list(self) -> list[Requirement]:
        g = self._all_graph()
        results: list[Requirement] = []
        for s in g.subjects(RDF.type, OSLC_RM.Requirement):
            req = Requirement()
            req.from_rdf(g, attributes)
            results.append(req)
        return results

    def create(self, requirement: Requirement) -> Requirement:
        existing = self.find(requirement.identifier)
        if existing:
            raise ValueError(f'Requirement {requirement.identifier} already exists')

        base_url = f'http://example.com/req/{requirement.identifier}'
        g = Graph()
        g.bind('dcterms', DCTERMS)
        g.bind('oslc', OSLC)
        g.bind('oslc_rm', OSLC_RM)
        g += requirement.to_rdf(g, base_url, attributes)

        turtle_data = g.serialize(format='turtle')
        query = (
            f'INSERT DATA {{ GRAPH <{REQUIREMENT_GRAPH_URI}> {{ '
            f'{turtle_data}'
            f' }} }}'
        )
        self._sparql_update(query)
        return requirement

    def update(self, requirement_id: str, requirement: Requirement) -> Requirement:
        existing = self.find(requirement_id)
        if not existing:
            from werkzeug.exceptions import NotFound
            raise NotFound(f'Requirement {requirement_id} not found')

        base_url = f'http://example.com/req/{requirement.identifier}'
        g = Graph()
        g.bind('dcterms', DCTERMS)
        g.bind('oslc', OSLC)
        g.bind('oslc_rm', OSLC_RM)
        g += requirement.to_rdf(g, base_url, attributes)

        turtle_data = g.serialize(format='turtle')

        delete_query = (
            f'DELETE {{ GRAPH <{REQUIREMENT_GRAPH_URI}> {{ ?s ?p ?o }} }} '
            f'USING <{REQUIREMENT_GRAPH_URI}> '
            f'WHERE {{ ?s ?p ?o . '
            f'?s <{DCTERMS.identifier}> "{requirement_id}"^^<http://www.w3.org/2001/XMLSchema#string> . '
            f'}}'
        )

        insert_query = (
            f'INSERT DATA {{ GRAPH <{REQUIREMENT_GRAPH_URI}> {{ '
            f'{turtle_data}'
            f' }} }}'
        )

        self._sparql_update(delete_query)
        self._sparql_update(insert_query)
        return requirement

    def delete(self, requirement_id: str) -> bool:
        existing = self.find(requirement_id)
        if not existing:
            from werkzeug.exceptions import NotFound
            raise NotFound(f'Requirement {requirement_id} not found')

        delete_query = (
            f'DELETE {{ GRAPH <{REQUIREMENT_GRAPH_URI}> {{ ?s ?p ?o }} }} '
            f'USING <{REQUIREMENT_GRAPH_URI}> '
            f'WHERE {{ ?s ?p ?o . '
            f'?s <{DCTERMS.identifier}> "{requirement_id}"^^<http://www.w3.org/2001/XMLSchema#string> . '
            f'}}'
        )
        self._sparql_update(delete_query)
        return True
