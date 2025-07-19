#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        # Pycodestyle E501 and E261 fixes applied here
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos",
                     "login": "google_org_name"}),  # example payload
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos",
                 "login": "abc_org_name"}),  # example payload
    ])
    @patch("client.get_json")  # Patch where get_json is imported in client.py
    def test_org(self, org_name, expected_org_payload, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload."""
        mock_get_json.return_value = expected_org_payload

        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert the result matches expected
        self.assertEqual(result, expected_org_payload)

        # Assert get_json called once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.get_json")  # Mock get_json (decorator)
    def test_public_repos(self, mock_get_json):
        """
        Tests GithubOrgClient.public_repos by mocking _public_repos_url
        and get_json.
        """
        # Define the payload that get_json will return when called by public_repos
        mock_repos_payload = [
            {"name": "alx-repo-1", "license": {"key": "mit"}},
            {"name": "alx-project", "license": {"key": "apache-2.0"}},
            {"name": "holberton-repo", "license": None},
        ]
        mock_get_json.return_value = mock_repos_payload

        # Use patch as a context manager for _public_repos_url
        # We need to target the property for mocking.
        # PropertyMock ensures it behaves like a property.
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            # Set the return value for the mocked _public_repos_url property
            mock_public_repos_url.return_value = \
                "https://api.github.com/orgs/alx/repos"

            # Instantiate the client (org_name doesn't matter here due to mocking)
            client = GithubOrgClient("alx")

            # Call the public_repos method
            repos = client.public_repos()

            # Assert that the list of repos is what we expect
            self.assertEqual(repos, ["alx-repo-1", "alx-project", "holberton-repo"])

            # Test that the mocked _public_repos_url property was called once
            mock_public_repos_url.assert_called_once()

            # Test that the mocked get_json was called once
            # It should have been called with the URL returned by the mocked
            # _public_repos_url
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/alx/repos")


if __name__ == "__main__":
    unittest.main()
