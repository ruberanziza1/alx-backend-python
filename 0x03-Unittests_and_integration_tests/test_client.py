#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""
    
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct payload
        and that get_json is called once with the expected URL.
        """
        # Import here to avoid import errors if client module has issues
        try:
            from client import GithubOrgClient
        except ImportError as e:
            self.fail(f"Could not import GithubOrgClient: {e}")
        
        # Set up expected payload
        expected_payload = {
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos",
            "login": org_name
        }
        
        # Configure the mock to return our expected payload
        mock_get_json.return_value = expected_payload
        
        # Create client instance
        client = GithubOrgClient(org_name)
        
        # Get the org property/method result
        try:
            result = client.org
        except AttributeError:
            # Try calling it as a method if it's not a property
            result = client.org()
        
        # Verify the result matches expected payload
        self.assertEqual(result, expected_payload)
        
        # Verify get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
