from corehq.apps.case_search.models import merge_queries, QueryMergeException
from django.test import SimpleTestCase

from corehq.util.test_utils import generate_cases

from corehq.apps.case_search.models import SEARCH_QUERY_CUSTOM_VALUE, replace_custom_query_variables


class TestQueryMerge(SimpleTestCase):
    def test_invalid_merge(self):
        with self.assertRaises(QueryMergeException):
            merge_queries(
                {"a": {"b": [1, 2, 3]}},
                {"a": {"b": "banana"}},
            )
        with self.assertRaises(QueryMergeException):
            merge_queries(
                {"a": {"b": 1}},
                {"a": "banana"},
            )


@generate_cases([
    # base case
    ({}, {}, {}),
    # simple merge
    ({"a": 1}, {"b": 2}, {"a": 1, "b": 2}),
    # second level merge
    ({'a': {'b': {'c': 1}}}, {'a': {'b2': 2}}, {'a': {'b': {'c': 1}, 'b2': 2}}),
    # list merge
    ({'a': [1, 2]}, {'a': [3]}, {'a': [1, 2, 3]}),
    # complex multi-branch merge
    (
        {"a": {("tuple", "key"): [1, 2]}, "b": [1, 2], "c": {"d": 1, "e": 2}},
        {"a": {("tuple", "key"): [3]}, "c": {"f": {"g": 4}}},
        {"a": {("tuple", "key"): [1, 2, 3]}, "b": [1, 2], "c": {"d": 1, "e": 2, "f": {"g": 4}}},
    ),
], TestQueryMerge)
def test_merge(self, base_query, addition, expected):
    new = merge_queries(base_query, addition)
    self.assertDictEqual(new, expected)


class TestCustomQueryValues(SimpleTestCase):
    def test_custom_values(self):
        initial_custom_query = {
            "nested": {
                "path": "case_properties",
                "query": {
                    "filtered": {
                        "filter": {
                            "term": {
                                "case_properties.key": "thing_1"
                            }
                        },
                        "query": {
                            "match": {
                                "case_properties.value": {
                                    "fuzziness": "0",
                                    "query": "__thing_1"
                                }
                            }
                        }
                    }
                }
            }
        }

        search_criteria = {
            "{}__thing_1".format(SEARCH_QUERY_CUSTOM_VALUE): "boop",
            "name": "Jon Snow",
        }

        expected = {
            "nested": {
                "path": "case_properties",
                "query": {
                    "filtered": {
                        "filter": {
                            "term": {
                                "case_properties.key": "thing_1"
                            }
                        },
                        "query": {
                            "match": {
                                "case_properties.value": {
                                    "fuzziness": "0",
                                    "query": "boop"
                                }
                            }
                        }
                    }
                }
            }
        }
        self.assertDictEqual(
            expected,
            replace_custom_query_variables(initial_custom_query, search_criteria)
        )
