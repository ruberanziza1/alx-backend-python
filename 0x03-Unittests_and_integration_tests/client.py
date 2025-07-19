#!/usr/bin/env python3
"""Test cases for client.py"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Set up the mock return value
        expected_result = {"name": org_name, "type": "Organization"}
        mock_get_json.return_value = expected_result
        
        # Create GithubOrgClient instance and call org method
        client = GithubOrgClient(org_name)
        result = client.org
        
        # Assert that get_json was called once with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Assert that the result is what we expect
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
