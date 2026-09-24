from datetime import datetime, timezone


def get_top_languages(repos):
    """Count how many repos use each language."""
    language_count = {}

    for repo in repos:
        lang = repo.get("language")
        if lang:
            language_count[lang] = language_count.get(lang, 0) + 1

    # Sort by count descending
    sorted_langs = sorted(language_count.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_langs)


def get_top_repos(repos, top_n=5):
    """Return top repos sorted by star count."""
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return sorted_repos[:top_n]


def get_recently_updated(repos, top_n=5):
    """Return most recently updated repos."""
    sorted_repos = sorted(repos, key=lambda r: r.get("updated_at", ""), reverse=True)
    return sorted_repos[:top_n]


def get_total_stars(repos):
    """Sum up all stars across all repos."""
    return sum(repo.get("stargazers_count", 0) for repo in repos)


def get_total_forks(repos):
    """Sum up all forks across all repos."""
    return sum(repo.get("forks_count", 0) for repo in repos)


def was_active_recently(events, days=30):
    """Check if user pushed code in the last N days."""
    now = datetime.now(timezone.utc)

    for event in events:
        if event.get("type") == "PushEvent":
            created_at = event.get("created_at", "")
            if created_at:
                event_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                delta = (now - event_time).days
                if delta <= days:
                    return True
    return False


def has_profile_readme(repos, username):
    """Check if the user has a special profile README repo."""
    for repo in repos:
        if repo.get("name", "").lower() == username.lower():
            return True
    return False


def account_age_years(created_at):
    """Return how many years old the GitHub account is."""
    if not created_at:
        return 0
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return (now - created).days / 365


def calculate_score(user, repos, events):
    """
    Calculate a profile score out of 100.
    Returns the score and a breakdown dict showing what contributed.
    """
    score = 0
    breakdown = {}

    # Has bio (+10)
    if user.get("bio"):
        score += 10
        breakdown["Has bio"] = 10
    else:
        breakdown["Has bio"] = 0

    # Has website/blog (+10)
    if user.get("blog"):
        score += 10
        breakdown["Has portfolio/website"] = 10
    else:
        breakdown["Has portfolio/website"] = 0

    # Has profile README (+15)
    username = user.get("login", "")
    if has_profile_readme(repos, username):
        score += 15
        breakdown["Has profile README"] = 15
    else:
        breakdown["Has profile README"] = 0

    # Followers (+10 if 10+)
    followers = user.get("followers", 0)
    if followers >= 10:
        score += 10
        breakdown["10+ followers"] = 10
    elif followers >= 1:
        score += 5
        breakdown["10+ followers"] = 5
    else:
        breakdown["10+ followers"] = 0

    # Repo count (+10 if 5+)
    repo_count = len(repos)
    if repo_count >= 5:
        score += 10
        breakdown["5+ public repos"] = 10
    elif repo_count >= 1:
        score += 5
        breakdown["5+ public repos"] = 5
    else:
        breakdown["5+ public repos"] = 0

    # Recent activity (+15 if committed in last 30 days)
    if was_active_recently(events, days=30):
        score += 15
        breakdown["Active in last 30 days"] = 15
    else:
        breakdown["Active in last 30 days"] = 0

    # Stars received (up to +15)
    total_stars = get_total_stars(repos)
    if total_stars >= 50:
        score += 15
        breakdown["Stars earned"] = 15
    elif total_stars >= 10:
        score += 10
        breakdown["Stars earned"] = 10
    elif total_stars >= 1:
        score += 5
        breakdown["Stars earned"] = 5
    else:
        breakdown["Stars earned"] = 0

    # Account age (+10 if 1+ years)
    age = account_age_years(user.get("created_at", ""))
    if age >= 1:
        score += 10
        breakdown["Account 1+ years old"] = 10
    else:
        breakdown["Account 1+ years old"] = 0

    # Avatar set (+5)
    avatar = user.get("avatar_url", "")
    if avatar and "gravatar" not in avatar:
        score += 5
        breakdown["Custom avatar set"] = 5
    else:
        breakdown["Custom avatar set"] = 0

    return min(score, 100), breakdown
