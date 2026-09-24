import requests

BASE_URL = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json"
}

def get_user(username):
    """Fetch basic profile info for a GitHub user."""
    url = f"{BASE_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 404:
        return None, "User not found. Check the username and try again."
    if response.status_code == 403:
        return None, "GitHub API rate limit hit. Wait a minute and try again."
    if response.status_code != 200:
        return None, f"GitHub API error: {response.status_code}"

    return response.json(), None


def get_repos(username):
    """Fetch all public repos for a GitHub user (up to 100)."""
    url = f"{BASE_URL}/users/{username}/repos"
    params = {"per_page": 100, "sort": "updated"}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        return [], f"Could not fetch repos: {response.status_code}"

    return response.json(), None


def get_events(username):
    """Fetch recent public activity/events for a GitHub user."""
    url = f"{BASE_URL}/users/{username}/events/public"
    params = {"per_page": 100}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        return [], None

    return response.json(), None
