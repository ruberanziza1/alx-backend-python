#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.org
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Mocked expected return value
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Create instance and call org()
        client = GithubOrgClient(org_name)
        result = client.org()

        # Assertions
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == '__main__':
    unittest.main()
