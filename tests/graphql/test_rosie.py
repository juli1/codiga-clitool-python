"""
Test for methods in graphql/rosie.py
"""

import unittest
from unittest.mock import patch

from codiga.graphql.rosie import graphql_get_rulesets, get_rulesets_name_string


class TestRosie(unittest.TestCase):
    """
    Tests for graphql/rosie.py
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_graphql_get_rulesets_invalid_argument(self):
        """
        Check that invalid arguments raise an exception
        :return:
        """
        with self.assertRaises(ValueError):
            graphql_get_rulesets(None, ["daniel-ruleset", "real-ruleset"])
        with self.assertRaises(ValueError):
            graphql_get_rulesets("blo", [])

    @patch('codiga.graphql.rosie.do_graphql_query')
    def test_graphql_get_rulesets_valid_argument(self, do_graphql_query_mock):
        """
        Check the value returned when called with valid arguments
        :return:
        """
        fake_data = [
            {
                "id": 1,
                "name": "daniel-ruleset",
                "rules": [
                    {
                        "id": 1,
                        "name": "rule-1",
                        "content": "cHJpbnQoIkhlbGxvIFdvcmxkISIp",
                        "language": "Python",
                        "ruleType": "Ast",
                        "pattern": None,
                        "patternMultiline": None,
                        "elementChecked": "FunctionCall"
                    }
                ]
            },
            {
                "id": 2,
                "name": "real-ruleset",
                "rules": [
                    {
                        "id": 3,
                        "name": "rule-3",
                        "content": "cHJpbnQoIkhlbGxvIFdvcmxkISIp",
                        "language": "Python",
                        "ruleType": "Ast",
                        "pattern": None,
                        "patternMultiline": None,
                        "elementChecked": "FunctionCall"
                    }
                ]
            }
        ]
        do_graphql_query_mock.return_value = {"ruleSetsForClient": fake_data}
        data = graphql_get_rulesets("api_token", ["daniel-ruleset", "real-ruleset"])
        do_graphql_query_mock.assert_called_with("api_token", {"query": """
        {
            ruleSetsForClient(names: """ + get_rulesets_name_string(["daniel-ruleset", "real-ruleset"]) + """){
            id
            name
            rules(howmany: 10000, skip: 0){
              id
              name
              content
              language
              ruleType
              pattern
              patternMultiline
              elementChecked
            }
          }
        }"""})
        self.assertEqual(fake_data, data)

    @patch('codiga.graphql.rosie.do_graphql_query')
    def test_graphql_get_rulesets_call(self, do_graphql_query_mock):
        """
        Check that we call the right method when arguments are valid
        :return:
        """
        graphql_get_rulesets("api_token", ["daniel-ruleset", "real-ruleset"])
        query1 = """
        {
            ruleSetsForClient(names: """ + get_rulesets_name_string(["daniel-ruleset", "real-ruleset"]) + """){
            id
            name
            rules(howmany: 10000, skip: 0){
              id
              name
              content
              language
              ruleType
              pattern
              patternMultiline
              elementChecked
            }
          }
        }"""
        do_graphql_query_mock.assert_called_with("api_token", {"query": query1})

        graphql_get_rulesets("api_token", ["real-ruleset"])
        query2 = """
        {
            ruleSetsForClient(names: """ + get_rulesets_name_string(["real-ruleset"]) + """){
            id
            name
            rules(howmany: 10000, skip: 0){
              id
              name
              content
              language
              ruleType
              pattern
              patternMultiline
              elementChecked
            }
          }
        }"""
        do_graphql_query_mock.assert_called_with("api_token", {"query": query2})
