#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient.
"""
from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from requests import Response

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

test_payload = TEST_PAYLOAD[0]


class TestGithubOrgClient(TestCase):
    """Unit tests for client.GithubOrgClient class.
    """

    @parameterized.expand([('google'),
                           ('abc')])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test the org method of GithubOrgClient.
        """
        client = GithubOrgClient(org_name)
        res = client.org()

        url = client.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Test the _public_repos_url property of GithubOrgClient.
        """
        url = 'https://org.github.com/google/repos'
        dummy_payload = {'repos_url': url}

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = dummy_payload
            client = GithubOrgClient('google')
            repos_url = client._public_repos_url

            mock_org.assert_called_once()
            self.assertEqual(client.org, dummy_payload)
            self.assertEqual(repos_url, url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method of GithubOrgClient.
        """
        dummy_payload = [
            {'name': 'repo one', 'license': {'key': '1'}},
            {'name': 'repo two', 'license': {'key': '2'}},
            {'name': 'repo three', 'license': {'key': '3'}},
        ]
        mock_get_json.return_value = dummy_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_pub_repos_url:
            mock_pub_repos_url.return_value = 'google/pub_repos'
            client = GithubOrgClient('google')
            repos = client.public_repos()

            mock_get_json.assert_called_once()
            mock_pub_repos_url.assert_called_once()
            assert repos == ['repo one', 'repo two', 'repo three']

    @parameterized.expand([({"license": {"key": "my_license"}},
                            'my_license', True),
                           ({"license": {"key": "other_license"}},
                            'my_license', False)])
    def test_has_license(self, repo, key, res):
        """tests has_license method
        """
        client = GithubOrgClient('google')
        self.assertEqual(client.has_license(repo, key), res)


@parameterized_class([
    {
        'org_payload': test_payload[0],
        'repos_payload': test_payload[1],
        'expected_repos': test_payload[2],
        'apache2_repos': test_payload[3]
    }
])
class TestIntegrationGithubOrgClient(TestCase):
    """Integration test cases for the GithubOrgClient class.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.org_url = "https://api.github.com/orgs/{org}"

        def side_effect(url):
            if url == cls.org_url.format(org='google'):
                return Mock(Response, json=lambda: cls.org_payload)
            if url == cls.org_payload['repos_url']:
                return Mock(Response, json=lambda: cls.repos_payload)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the test class.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method in an integration context.
        """
        client = GithubOrgClient('google')

        assert client.public_repos() == self.expected_repos

    def test_public_repos_with_license(self):
        """Test public_repos method with license argument."""
        # Create an instance of GithubOrgClient
        test_instance = GithubOrgClient("test_org")

        # Call the public_repos method with license argument
        result = test_instance.public_repos(license="apache-2.0")

        # Assert that the result is what is expected for the given license
        self.assertEqual(result, self.apache2_repos)
