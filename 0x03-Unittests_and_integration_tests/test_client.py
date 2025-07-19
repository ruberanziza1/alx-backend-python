#!/usr/bin/env python3
"""Unit and integration tests for client.py"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        payload = {"repos_url": f"https://api.github.com/users/{org_name}/repos",
                   "login": org_name}
        mock_get_json.return_value = payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        client = GithubOrgClient("any")
        with patch.object(GithubOrgClient, "org",
                          new_callable=PatchProperty) as mock_org:
            mock_org.return_value = {"repos_url": "http://fake-repos/"}
            self.assertEqual(client._public_repos_url, "http://fake-repos/")

    @parameterized.expand([
        ([], [{"name": "repo1", "license": {"key": "mit"}}, {"name": "repo2", "license": {"key": "apache-2.0"}}], None, ["repo1", "repo2"]),
        ([], [{"name": "repo1", "license": {"key": "mit"}}, {"name": "repo2", "license": {"key": "apache-2.0"}}], "apache-2.0", ["repo2"]),
    ])
    @patch("client.get_json")
    def test_public_repos(self, _, repos, license_key, expected):
        client = GithubOrgClient("org")
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=Mock, return_value="URL"):
            mock_get_json.return_value = repos
            result = client.public_repos(license_key)
            self.assertEqual(result, expected)
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), [
    (org_payload, repos_payload, expected_repos, apache2_repos),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using fixtures."""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def json_side_effect(url):
            if url == org_payload["url"]:
                return Mock(json=Mock(return_value=org_payload)).json()
            return Mock(json=Mock(return_value=repos_payload)).json()

        mock_get.return_value = Mock(json=Mock(side_effect=lambda: json_side_effect(mock_get.call_args[0][0])))

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
