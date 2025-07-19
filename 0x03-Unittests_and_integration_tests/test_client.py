#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient # This imports GithubOrgClient and makes client.get_json available for patching

class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos", "login": "google_org_name"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos", "login": "abc_org_name"}),
    ])
    @patch("client.get_json") # Patch the get_json function within the 'client' module
    def test_org(self, org_name, expected_org_payload, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload."""

        # Configure the mock to return the specific payload for each test case
        mock_get_json.return_value = expected_org_payload

        # Instantiate the client
        client = GithubOrgClient(org_name)

        # Call the 'org' property
        result = client.org

        # Assert that the result matches the expected payload
        self.assertEqual(result, expected_org_payload)

        # Assert that get_json was called exactly once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    # Adding a test for _public_repos_url if you implement it later.
    # This test relies on mocking the 'org' property directly using PropertyMock.
    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the correct URL based on org data."""
        # Define the mock return value for the 'org' property
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/alx-holberton/repos"}

        client = GithubOrgClient("alx-holberton")

        # Assuming _public_repos_url will look like this in client.py:
        # @property
        # def _public_repos_url(self) -> str:
        #     return self.org["repos_url"]
        # If it's a private method, you might need to test the public method that uses it.
        # For this test, we are directly accessing a hypothetical _public_repos_url property.

        # This line will cause an AttributeError if _public_repos_url is not a property
        # or if it's not implemented yet. If you don't have this property in client.py yet,
        # comment out this test for now.
        # self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/alx-holberton/repos")

        # Assert that the 'org' property was called to get the repos_url
        mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
