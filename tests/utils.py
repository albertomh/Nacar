# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Testing utilities
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Utility methods accessible to tests across the suite.

from typing import List


def get_nested_key(obj: dict, chain: List[str]):
    # Copy to avoid mutating original list in calling context.
    _chain = [li for li in chain]
    _key = _chain.pop(0)
    if _key in obj:
        if len(_chain) > 0:
            return get_nested_key(obj[_key], _chain)
        else:
            return obj[_key]
    return None
