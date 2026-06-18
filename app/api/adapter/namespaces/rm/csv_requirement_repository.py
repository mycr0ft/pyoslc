import csv
import os
import shutil
from tempfile import NamedTemporaryFile

from werkzeug.exceptions import NotFound

from app.api.adapter.resources.repository import RequirementRepository
from pyoslc.resources.domains.rm import Requirement


class CsvRequirementRepository(RequirementRepository):

    specification_map = {
        'Specification_id': {'attribute': '_BaseResource__identifier', 'oslc_property': 'DCTERMS.identifier'},
        'Title': {'attribute': '_BaseResource__title', 'oslc_property': 'DCTERMS.title'},
        'Description': {'attribute': '_BaseResource__description', 'oslc_property': 'DCTERMS.description'},
        'Author': {'attribute': '_BaseResource__creator', 'oslc_property': 'DCTERMS.creator'},
        'Product': {'attribute': '_BaseResource__short_title', 'oslc_property': 'DCTERMS.shortTitle'},
        'Subject': {'attribute': '_BaseResource__subject', 'oslc_property': 'DCTERMS.subject'},
        'Source': {'attribute': '_Requirement__elaborated_by', 'oslc_property': 'OSLC_RM.elaboratedBy'},
        'Category': {'attribute': '_Requirement__constrained_by', 'oslc_property': 'OSLC_RM.constrainedBy'},
        'Discipline': {'attribute': '_Requirement__satisfied_by', 'oslc_property': 'OSLC_RM.satisfiedBy'},
        'Revision': {'attribute': '_Requirement__tracked_by', 'oslc_property': 'OSLC_RM.trackedBy'},
        'Target_Value': {'attribute': '_Requirement__validated_by', 'oslc_property': 'OSLC_RM.validatedBy'},
        'Degree_of_fulfillment': {'attribute': '_Requirement__affected_by', 'oslc_property': 'OSLC_RM.affectedBy'},
        'Status': {'attribute': '_Requirement__decomposed_by', 'oslc_property': 'OSLC_RM.decomposedBy'},
        'PUID': {'attribute': '_Requirement__puid', 'oslc_property': 'OSLC_RM.puid'},
        'Project': {'attribute': '_BaseResource__subject', 'oslc_property': 'DCTERMS.subject'},
    }

    def __init__(self, title: str, csv_file_path: str | None = None):
        super().__init__(title)
        self.csv_file_path = csv_file_path or os.path.join(
            os.path.abspath(''), 'examples', 'specifications.csv')

    def csv_path(self) -> str | None:
        return self.csv_file_path

    def find(self, requirement_id: str) -> Requirement | None:
        with open(self.csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                if row['Specification_id'] == requirement_id:
                    requirement = Requirement()
                    requirement.update(row, attributes=self.specification_map)
                    return requirement
        return None

    def list(self) -> list[Requirement]:
        requirements: list[Requirement] = []
        if not os.path.isfile(self.csv_file_path):
            return requirements
        with open(self.csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                requirement = Requirement()
                requirement.update(row, attributes=self.specification_map)
                requirements.append(requirement)
        return requirements

    def _csv_fieldnames(self):
        if not os.path.isfile(self.csv_file_path):
            return list(self.specification_map.keys())
        with open(self.csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            return reader.fieldnames if reader.fieldnames else []

    def create(self, requirement):
        fieldnames = self._csv_fieldnames()
        with open(self.csv_file_path, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writerow(self._requirement_to_dict(requirement, fieldnames))
        return requirement

    @staticmethod
    def _sanitize_row(row):
        row.pop(None, None)
        row.pop('', None)
        return row

    def _rewrite_csv(self, requirement_id, modify_func):
        path = self.csv_file_path
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            field_names = reader.fieldnames

        found = False
        with open(path, 'r', encoding='utf-8') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=field_names, delimiter=';')
            writer = csv.DictWriter(tempfile, fieldnames=field_names, delimiter=';')
            for row in reader:
                found = modify_func(row, writer) or found

        shutil.move(tempfile.name, path)
        return found

    def update(self, requirement_id: str, requirement):
        field_names = self._csv_fieldnames()

        def _do_update(row, writer):
            if row['Specification_id'] == str(requirement_id):
                writer.writerow(self._requirement_to_dict(requirement, field_names))
                return True
            writer.writerow(self._sanitize_row(row))
            return False

        found = self._rewrite_csv(requirement_id, _do_update)
        if not found:
            raise NotFound(f'Requirement {requirement_id} not found')
        return requirement

    def delete(self, requirement_id: str):
        def _do_delete(row, writer):
            if row['Specification_id'] != str(requirement_id):
                writer.writerow(self._sanitize_row(row))
                return False
            return True

        found = self._rewrite_csv(requirement_id, _do_delete)
        if not found:
            raise NotFound(f'Requirement {requirement_id} not found')
        return True

    def _requirement_to_dict(self, requirement, fieldnames=None):
        if fieldnames is None:
            fieldnames = self._csv_fieldnames()
        specification: dict = {}
        for key in fieldnames:
            if key not in self.specification_map:
                continue
            attribute_name = self.specification_map[key]['attribute']
            if hasattr(requirement, attribute_name):
                attribute_value = getattr(requirement, attribute_name)
                if attribute_value:
                    if isinstance(attribute_value, set):
                        specification[key] = next(iter(attribute_value))
                    else:
                        specification[key] = attribute_value
        return specification
