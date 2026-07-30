"""Tests for maas_engine.update.migration helpers"""

from maas_engine.update.migration import MaasMigrator


def test_strip_field_descriptions():
    """the maas-only "description" metadata is removed recursively while the
    rest of the mapping (type, meta, nested properties) is left untouched"""
    properties = {
        "mission": {"type": "keyword", "description": "Mission identifier"},
        "count": {"type": "integer"},
        "meta_obj": {
            "type": "object",
            "description": "Nested metadata block",
            "properties": {
                "inner": {"type": "keyword", "description": "Inner value"},
                "kept_meta": {
                    "type": "keyword",
                    "meta": {"_specific": "S1"},
                },
            },
        },
    }

    MaasMigrator.strip_field_descriptions(properties)

    assert properties == {
        "mission": {"type": "keyword"},
        "count": {"type": "integer"},
        "meta_obj": {
            "type": "object",
            "properties": {
                "inner": {"type": "keyword"},
                "kept_meta": {"type": "keyword", "meta": {"_specific": "S1"}},
            },
        },
    }
