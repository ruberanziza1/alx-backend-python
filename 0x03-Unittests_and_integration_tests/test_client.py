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

    @patch('utils.get_json')

    def test_org(self, org_name, mock_get_json):

        """Test that GithubOrgClient.org returns the correct value."""

        # Set up test payload

        test_payload = {"login": org_name, "id": 12345}

        mock_get_json.return_value = test_payload

        

        # Create client instance

        client = GithubOrgClient(org_name)

        

        # Call org property (memoized method becomes a property)

        result = client.org

        

        # Assert get_json was called once with expected URL

        expected_url = f"https://api.github.com/orgs/{org_name}"

        mock_get_json.assert_called_once_with(expected_url)

        

        # Assert result is the expected payload

        self.assertEqual(result, test_payload)





if __name__ == "__main__":

    unittest.main()
