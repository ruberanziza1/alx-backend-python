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
    @patch("client.get_json")  # Patch get_json where client uses it
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected data."""
        expected_payload = {
            "repos_url": f"https://api.github.com/users/{org_name}/repos",
            "login": org_name,
        }

        # Setup mock to return expected_payload without executing real HTTP calls
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)

        # Call the org property which internally calls the mocked get_json
        result = client.org

        # Assert the result matches expected payload
        self.assertEqual(result, expected_payload)

        # Assert get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
