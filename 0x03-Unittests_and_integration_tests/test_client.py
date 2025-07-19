#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        # Parameterized test cases for different organization names
        # Each tuple contains (org_name, expected_payload_from_get_json)
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos",
                     "login": "google"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos",
                 "login": "abc"}),
    ])
    @patch("client.get_json")  # Patch the get_json function within the 'client' module
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct payload
        and that get_json is called once with the expected URL.
        """
        # Configure the mock_get_json to return the specific expected_payload
        # when it is called by client.GithubOrgClient.org
        mock_get_json.return_value = expected_payload

        # Instantiate the GithubOrgClient with the current organization name
        client = GithubOrgClient(org_name)

        # Access the 'org' property, which should trigger the mocked get_json call
        result = client.org

        # Assert that the result returned by client.org matches our expected payload
        self.assertEqual(result, expected_payload)

        # Assert that the mocked get_json was called exactly once
        # with the correct GitHub API URL for the organization
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    # This block allows running the tests directly from the command line
    unittest.main()
