#!/usr/bin/env python3
"""
Convert Airbus Apollo 11 SysML v2 model to pyoslc OSLC JSON format.

Parses .sysml files with sysmlpy, walks the model tree, and generates
JSON entries that the pyoslc seeder can load into the InMemorySysMLRepository.
"""
import json
import os
import re
import sys

try:
    from sysmlpy import loads
except ImportError:
    sys.stderr.write(
        "sysmlpy is not installed. Install it with:\n"
        "  pip install 'pyoslc[sysml]'\nor:\n"
        "  pip install sysmlpy\n"
    )
    sys.exit(1)


def _first_line(dump_str):
    """Get just the declaration line (first line, up to { or ;)."""
    if not dump_str:
        return ''
    line = dump_str.split('{')[0].split(';')[0].strip()
    return line


def extract_type_name(dump_str):
    """Extract the type name from the first line, e.g. 'part stage1: 'S-IC';'"""
    line = _first_line(dump_str)
    match = re.search(r":\s*'([^']+)'", line)
    if match:
        return match.group(1)
    match = re.search(r"\bpart\s+\w+\s*:\s*(\w+)", line)
    if match:
        return match.group(1)
    match = re.search(r"\bport\s+\w+\s*:\s*(~?)(\w+)", line)
    if match:
        return match.group(2)
    return None


def extract_doc(dump_str):
    """Extract doc comment from a dump string."""
    match = re.search(r'doc\s*/\*\s*(.*?)\s*\*/', dump_str)
    if match:
        return match.group(1).strip()
    return None


def extract_attribute_value(dump_str):
    """Extract value and unit from 'attribute height= 110.6[m];'"""
    match = re.search(r'=\s*([\d.]+)\s*\[([^\]]+)\]', dump_str)
    if match:
        return f"{match.group(1)} [{match.group(2)}]"
    return None


def sanitize_name(name):
    """Convert a SysML name to a safe identifier."""
    if name is None:
        return None
    return name.strip("'").replace(' ', '_').replace('-', '_')


def _child_identifier(elem, parent_qname):
    """Get the identifier for a child element without adding to seen_ids."""
    name = getattr(elem, 'name', None)
    if name is None or len(name) == 36 and name.count('-') == 4:
        return None
    child_qname = parent_qname + '::' + name if parent_qname else name
    return child_qname.replace('::', '-').replace("'", "").replace(' ', '_')


def convert_element(elem, parent_qualified_name, seen_ids):
    """Convert a sysmlpy element to an OSLC JSON entry."""
    if elem is None:
        return None

    name = getattr(elem, 'name', None)
    if name is None or name.startswith('uuid:') or len(name) == 36 and name.count('-') == 4:
        return None

    cls_name = type(elem).__name__
    is_def = getattr(elem, 'is_definition', False)

    dump_str = ''
    g = getattr(elem, 'grammar', None)
    if g and hasattr(g, 'dump'):
        try:
            dump_str = g.dump()
        except Exception:
            pass

    type_name = extract_type_name(dump_str)
    doc = extract_doc(dump_str)

    qname = parent_qualified_name + '::' + name if parent_qualified_name else name
    identifier = qname.replace('::', '-').replace("'", "").replace(' ', '_')
    if identifier in seen_ids:
        return None
    seen_ids.add(identifier)

    entry = {
        'identifier': identifier,
        'title': name.strip("'").replace('_', ' '),
        'element_id': identifier,
        'declared_name': name.strip("'"),
        'name': name.strip("'"),
        'qualified_name': qname,
    }

    if doc:
        entry['description'] = doc

    # Map sysmlpy types to OSLC resource types
    if cls_name == 'Package':
        entry['type'] = 'SysMLPackage'
        owned = []
        for child in elem:
            child_id = _child_identifier(child, qname)
            if child_id:
                owned.append(child_id)
        entry['owned_member'] = owned

    elif cls_name == 'Part':
        if is_def:
            entry['type'] = 'SysMLPartDefinition'
        else:
            entry['type'] = 'SysMLPartUsage'

        if type_name:
            entry['definition'] = [sanitize_name(type_name)]

        # Collect owned parts, attributes, ports (just identifiers, no recursion)
        owned_parts = []
        owned_attrs = []
        owned_ports = []

        for child in getattr(elem, 'parts', []):
            child_id = _child_identifier(child, qname)
            if child_id:
                owned_parts.append(child_id)

        for child in getattr(elem, 'attributes', []):
            child_id = _child_identifier(child, qname)
            if child_id:
                owned_attrs.append(child_id)

        for child in getattr(elem, 'ports', []):
            child_id = _child_identifier(child, qname)
            if child_id:
                owned_ports.append(child_id)

        if owned_parts:
            entry['owned_part'] = owned_parts
        if owned_attrs:
            entry['owned_attribute'] = owned_attrs
        if owned_ports:
            entry['owned_port'] = owned_ports

    elif cls_name == 'Attribute':
        if is_def:
            entry['type'] = 'SysMLAttributeDefinition'
        else:
            entry['type'] = 'SysMLAttributeUsage'
        val = extract_attribute_value(dump_str)
        if val:
            entry['description'] = f"Value: {val}"

    elif cls_name == 'Port':
        if is_def:
            entry['type'] = 'SysMLPortDefinition'
        else:
            entry['type'] = 'SysMLPortUsage'
        if type_name:
            entry['definition'] = [sanitize_name(type_name)]

    elif cls_name == 'Requirement':
        if is_def:
            entry['type'] = 'SysMLRequirementDefinition'
        else:
            entry['type'] = 'SysMLRequirementUsage'
        req_id_match = re.search(r'reqId\s*=\s*"?([^";\s]+)"?', dump_str)
        if req_id_match:
            entry['req_id'] = req_id_match.group(1)
        text_match = re.search(r'text\s*=\s*"([^"]+)"', dump_str)
        if text_match:
            entry['text'] = [text_match.group(1)]

    elif cls_name == 'Connection':
        entry['type'] = 'SysMLConnectionUsage'

    elif cls_name == 'Interface':
        if is_def:
            entry['type'] = 'SysMLInterfaceDefinition'
        else:
            entry['type'] = 'SysMLInterfaceUsage'

    elif cls_name == 'Flow':
        entry['type'] = 'SysMLFlowUsage'

    elif cls_name == 'Allocation':
        entry['type'] = 'SysMLAllocationUsage'

    elif cls_name == 'Action':
        if is_def:
            entry['type'] = 'SysMLActionDefinition'
        else:
            entry['type'] = 'SysMLActionUsage'

    elif cls_name == 'State':
        if is_def:
            entry['type'] = 'SysMLStateDefinition'
        else:
            entry['type'] = 'SysMLStateUsage'

    elif cls_name == 'Constraint':
        if is_def:
            entry['type'] = 'SysMLConstraintDefinition'
        else:
            entry['type'] = 'SysMLConstraintUsage'

    elif cls_name == 'Calculation':
        if is_def:
            entry['type'] = 'SysMLCalculationDefinition'
        else:
            entry['type'] = 'SysMLCalculationUsage'

    elif cls_name == 'Case':
        if is_def:
            entry['type'] = 'SysMLCaseDefinition'
        else:
            entry['type'] = 'SysMLCaseUsage'

    elif cls_name == 'UseCase':
        if is_def:
            entry['type'] = 'SysMLUseCaseDefinition'
        else:
            entry['type'] = 'SysMLUseCaseUsage'

    elif cls_name == 'Item':
        if is_def:
            entry['type'] = 'SysMLItemDefinition'
        else:
            entry['type'] = 'SysMLItemUsage'

    else:
        entry['type'] = 'SysMLElement'

    return entry


def collect_all_entries(elem, parent_qname, seen_ids, all_entries):
    """Recursively collect all entries from the model tree."""
    entry = convert_element(elem, parent_qname, seen_ids)
    if entry:
        all_entries.append(entry)
        child_qname = entry.get('qualified_name', parent_qname)
    else:
        child_qname = parent_qname

    for child in elem:
        collect_all_entries(child, child_qname, seen_ids, all_entries)


def convert_sysml_to_oslc(sysml_dir, output_path):
    """Parse all .sysml files in a directory and generate OSLC JSON."""
    import glob

    files = sorted(glob.glob(os.path.join(sysml_dir, '*.sysml')))
    all_entries = []
    seen_ids = set()

    for fpath in files:
        fname = os.path.basename(fpath)
        print(f'  Parsing {fname}...', file=sys.stderr)
        try:
            with open(fpath, 'r') as f:
                text = f.read()
            model = loads(text)
            collect_all_entries(model, '', seen_ids, all_entries)
        except Exception as e:
            print(f'  WARNING: Could not parse {fname}: {e}', file=sys.stderr)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

    print(f'  Generated {len(all_entries)} OSLC elements -> {output_path}', file=sys.stderr)
    return all_entries


if __name__ == '__main__':
    sysml_dir = sys.argv[1] if len(sys.argv) > 1 else 'examples/saturn_v/sysml'
    output = sys.argv[2] if len(sys.argv) > 2 else 'examples/saturn_v/saturn_v.json'
    convert_sysml_to_oslc(sysml_dir, output)
