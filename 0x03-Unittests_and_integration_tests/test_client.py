#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos", "login": "google"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos", "login": "abc"}),
    ])
    @patch("client.get_json")  # Patch where get_json is imported in client.py
    def test_org(self, org_name, expected_org_payload, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload."""
        # Setup the mock to return the full organization payload
        # that get_json would typically return.
        # The 'org' property of GithubOrgClient should then extract what it needs.
        # For this test, we assume 'client.get_json' is called with the org URL,
        # and that the 'org' property returns the *entire* JSON response for the organization.
        
        # If the 'org' property of GithubOrgClient processes the
        # full JSON and returns a subset, you'd adjust expected_org_payload accordingly.
        # For simplicity, let's assume it returns the direct result of get_json.

        mock_get_json.return_value = expected_org_payload

        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert the result matches expected
        self.assertEqual(result, expected_org_payload)

        # Assert get_json called once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    # Add this test if GithubOrgClient.org also uses an internal cache
    # @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    # def test_public_repos_url(self, mock_org):
    #     """Test that _public_repos_url returns the correct URL."""
    #     expected_repos_url = "https://api.github.com/orgs/someorg/repos"
    #     mock_org.return_value = {"repos_url": expected_repos_url}
    #     
    #     client = GithubOrgClient("someorg")
    #     self.assertEqual(client._public_repos_url, expected_repos_url)
    #     mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
