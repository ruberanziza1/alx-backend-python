#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # Patch where get_json is imported in client.py
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload."""
        expected_payload = {
            "repos_url": f"https://api.github.com/users/{org_name}/repos",
            "login": org_name,
        }

        # Setup the mock to return expected payload
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert the result matches expected
        self.assertEqual(result, expected_payload)

        # Assert get_json called once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
