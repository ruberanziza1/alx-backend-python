#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
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
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)

        result = client.org

        self.assertEqual(result, expected_payload)

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.get_json")  # Mock get_json (decorator)
    def test_public_repos(self, mock_get_json):
        """
        Tests GithubOrgClient.public_repos by mocking _public_repos_url
        and get_json.
        """
        mock_repos_payload = [
            {"name": "alx-repo-1", "license": {"key": "mit"}},
            {"name": "alx-project", "license": {"key": "apache-2.0"}},
            {"name": "holberton-repo", "license": None},
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = \
                "https://api.github.com/orgs/alx/repos"

            client = GithubOrgClient("alx")

            repos = client.public_repos()

            self.assertEqual(repos, ["alx-repo-1", "alx-project", "holberton-repo"])

            mock_public_repos_url.assert_called_once()

            mock_get_json.assert_called_once_with("https://api.github.com/orgs/alx/repos")
