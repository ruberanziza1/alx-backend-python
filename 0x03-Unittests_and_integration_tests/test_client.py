#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock # PropertyMock is not used in this specific test_org, but good to have
from parameterized import parameterized
from client import GithubOrgClient # This imports GithubOrgClient and get_json (implicitly)

class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos", "login": "google"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos", "login": "abc"}),
    ])
    @patch("client.get_json")  # This is the correct patch target!
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

if __name__ == "__main__":
    unittest.main()
