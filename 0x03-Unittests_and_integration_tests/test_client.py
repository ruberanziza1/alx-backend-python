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
        with patch('utils.get_json') as mock_get_json:
            test_payload = {"repos_url": "https://api.github.com/users/test/repos", "login": org_name}
            mock_get_json.return_value = test_payload
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, test_payload)
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/{}".format(org_name))


if __name__ == "__main__":
    unittest.main()
