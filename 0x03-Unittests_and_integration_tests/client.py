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
        # Internal cache for organization data to prevent repeated API calls
        self._org = None

    @property
    def org(self) -> dict:
        """
        Returns the organization payload from the GitHub API.
        Caches the result after the first call.
        """
        if self._org is None:
            self._org = get_json(f"https://api.github.com/orgs/{self.org_name}")
        return self._org
