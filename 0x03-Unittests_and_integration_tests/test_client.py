#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos",
                     "login": "google"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos",
                 "login": "abc"}),
    ])
    @patch("client.get_json")  # Patch the get_json function in the client module
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the expected payload
        and that get_json is called once with the correct URL.
        """
        # Configure the mock to return the specific payload for each test case
        mock_get_json.return_value = expected_payload

        # Instantiate the client with the current organization name
        client = GithubOrgClient(org_name)

        # Call the 'org' property of the client
        result = client.org

        # Assert that the result matches the expected payload
        self.assertEqual(result, expected_payload)

        # Assert that get_json was called exactly once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
