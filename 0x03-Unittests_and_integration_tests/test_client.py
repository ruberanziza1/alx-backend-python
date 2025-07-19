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
    def test_org(self, org_name):
        """Test that GithubOrgClient.org returns the correct value."""
        # Define the payload that mock_get_json should return for the org API call
        # This mocks the data that GithubOrgClient.org expects to receive
        test_payload = {"repos_url": f"https://api.github.com/users/{org_name}/repos", "login": org_name}

        # Patch 'utils.get_json'. The 'client' module imports 'utils', so we patch 'client.utils.get_json'.
        # However, if 'utils' is imported as `from utils import get_json`, then
        # you need to patch 'client.get_json' if you're patching where it's used.
        # Given your 'from utils import (get_json, ...)' in client.py,
        # patching `client.utils.get_json` is the correct approach to mock the function itself.
        # If your `GithubOrgClient` directly imports `get_json` as `from utils import get_json`,
        # then patching `client.get_json` might be needed.
        # Let's stick with patching `utils.get_json` at its source, which is generally cleaner.
        with patch('utils.get_json') as mock_get_json:
            mock_get_json.return_value = test_payload

            client = GithubOrgClient(org_name)

            # Assert that the client.org property returns the expected payload
            # client.org calls utils.get_json, which we've mocked to return test_payload
            self.assertEqual(client.org, test_payload)

            # Assert that utils.get_json was called exactly once with the correct URL
            expected_url = f"https://api.github.com/orgs/{org_name}"
            mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
