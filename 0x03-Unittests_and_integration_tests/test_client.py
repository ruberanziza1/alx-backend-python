#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"repos_url": "url", "login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"repos_url": "url", "login": org_name})
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

if __name__ == "__main__":
    unittest.main()
