#!/usr/bin/env python3
"""Ge Unit tests for utils.access_nested_map..
"""
from typing import Mapping, Sequence
from unittest import TestCase
from unittest.mock import Mock, patch
from parameterized import parameterized
import requests

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(TestCase):
    """Test cases for the access_nested_map function.
    """

    @parameterized.expand([({'a': 1}, ('a',), 1),
                           ({"a": {"b": 2}}, ('a',), {'b': 2}),
                           ({"a": {"b": 2}}, ('a', 'b'), 2)])
    def test_access_nested_map(self, nested_map: Mapping, nested_path: Sequence,
                               expected: Mapping):
        """Test access_nested_map with various inputs.
        """
        self.assertEqual(access_nested_map(nested_map, nested_path), expected)

    @parameterized.expand([({}, ('a')), ({'a': 1}, ('a', 'b'))])
    def test_access_nested_map_exception(self, nested_map, nested_path):
        """Test access_nested_map when it raises a KeyError.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(map, nested_path)

        self.assertIn(nested_path[-1], str(context.exception))


class TestGetJson(TestCase):
    """Test cases for the get_json function.
    """

    @parameterized.expand([("http://example.com", {"payload": True}),
                           ("http://holberton.io", {"payload": False})])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json with various inputs.
        """
        mock_get.return_value = Mock(requests.Response, json=lambda: test_payload)

        res = get_json(test_url)

        mock_get.assert_called_once()
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(res, test_payload)


class TestMemoize(TestCase):
    """Test cases for the memoize decorator.
    """

    def test_memoize(self):
        """Tests utils.memoize
        """
        class TestClass:
            """Test class with a_method and a_property."""

            def a_method(self):
                """A simple method."""
                return 42

            @memoize
            def a_property(self):
                """A memoized property."""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            test_cls = TestClass()

            res1 = test_cls.a_property
            res2 = test_cls.a_property

            self.assertEqual(res1, res2)
            mock_a_method.assert_called_once()
