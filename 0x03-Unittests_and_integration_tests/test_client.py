#!/usr/bin/env python3
"""Unit tests for client.py"""

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
    @patch("client.get_json")  # ✅ Patch where it's used, not defined
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        test_payload = {
            "repos_url": f"https://api.github.com/users/{org_name}/repos",
            "login": org_name
        }

        # Set the mock's return value
        mock_get_json.return_value = test_payload

        # Create an instance of the client
        client = GithubOrgClient(org_name)

        # Access the org property
        result = client.org

        # Check that the return value is correct
        self.assertEqual(result, test_payload)

        # Check that get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
