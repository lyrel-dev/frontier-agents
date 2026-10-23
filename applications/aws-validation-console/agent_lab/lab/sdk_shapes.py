"""Bounded, complete input schemas for the installed SDK's read operations.

Fail instead of returning a partially described container. A truncated list or
structure cannot safely generate the operator's resource-parameter form.
"""
from __future__ import annotations
from .util import Blocked


def input_shape(root, *, max_depth: int = 16, max_nodes: int = 4096):
    count = 0

    def visit(shape, depth, ancestors):
        nonlocal count
        if shape is None:
            return {}
        count += 1
        if count > max_nodes or depth > max_depth:
            raise Blocked('SDK input exceeds the supported form complexity; no partial parameter schema was returned')
        name = getattr(shape, 'name', None)
        if name and name in ancestors:
            raise Blocked('Recursive SDK input is not supported by the guided parameter form')
        path = (*ancestors, name) if name else ancestors
        result = {'type': shape.type_name, 'required': list(getattr(shape, 'required_members', []))}
        if shape.type_name == 'structure':
            result['fields'] = {key: visit(value, depth + 1, path) for key, value in shape.members.items()}
        elif shape.type_name == 'list':
            result['items'] = visit(shape.member, depth + 1, path)
        elif shape.type_name == 'map':
            result['values'] = visit(shape.value, depth + 1, path)
        return result

    return visit(root, 0, ())
