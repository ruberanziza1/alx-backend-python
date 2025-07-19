# client.py
import requests

def get_json(url: str):
    """Fetches JSON data from a given URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    return response.json()

class GithubOrgClient:
    """A client to interact with the GitHub API for organizations."""
    def __init__(self, org_name: str):
        self.org_name = org_name
        self._org = None # Internal cache for organization data

    @property
    def org(self) -> dict:
        """
        Returns the organization payload from the GitHub API.
        Caches the result after the first call.
        """
        if self._org is None:
            self._org = get_json(f"https://api.github.com/orgs/{self.org_name}")
        return self._org

    @property
    def _public_repos_url(self) -> str:
        """Returns the URL for public repositories of the organization."""
        return self.org["repos_url"]

    def public_repos(self, class_name=None) -> list:
        """
        Returns a list of public repositories for the organization.
        Optionally filters by projects whose name contains class_name.
        """
        repos_payload = get_json(self._public_repos_url)
        
        repos = []
        for repo in repos_payload:
            if class_name is None:
                repos.append(repo["name"])
            elif class_name in repo["name"]:
                repos.append(repo["name"])
        return repos
