#!python3

import os
import sys
import datetime
from github import Github

blacklist = []
labels = ""

def get_repo_stats(type, repo, days):
    global blacklist, labels

    org = "None"
    if repo.organization is not None:
        org = repo.organization.name
    if org in blacklist:
        return

    today = datetime.datetime.utcnow().date()
    try:
        if type == "views":
            stats = repo.get_views_traffic("day")
        else:
            stats = repo.get_clones_traffic("day")
    except Exception as e:
        # skip repos with missing permissions
        print(f"Failed to get stats from repo {repo} {e}", file=sys.stderr)
        return

    lines = {}

    # process day by day
    while days >= 0:
        day = today - datetime.timedelta(days)
        days = days - 1

        for s in stats[type]:
            time = datetime.datetime.strptime(str(s.timestamp), "%Y-%m-%d %H:%M:%S+00:00")

            if time.strftime("%Y-%m-%d") != day.strftime("%Y-%m-%d"):
                continue

            lines[
                time.strftime("%s")
            ] = "github_%s,repo=%s,org=\"%s\"%s count=%d,unique=%d %s" % (
                type,
                repo.name,
                org,
                labels,
                s.count,
                s.uniques,
                time.strftime("%s"),
            )
        # fill with 0 values
        if day.strftime("%s") not in lines:
            lines[
                day.strftime("%s")
            ] = "github_%s,repo=%s,org=\"%s\"%s count=%d,unique=%d %s" % (
                type,
                repo.name,
                org,
                labels,
                0,
                0,
                day.strftime("%s"),
            )

    for d in sorted(lines, key=lines.get):
        print(lines[d])


def get_asset_stats(repo):
    global blacklist, labels

    today = datetime.datetime.today()
    org = None
    if repo.organization is not None:
        org = repo.organization.name
    if org in blacklist:
        return

    try:
        rel = repo.get_releases()
        lines = []
        for r in rel:
            rel_time = datetime.datetime.strptime(str(r.published_at), "%Y-%m-%d %H:%M:%S+00:00")
            if (today - rel_time).days > 365:
                # print("Skipping release older than 1 year")
                continue
            # print(vars(r))
            # print(f"Repo {repo.name} Release {r.title} {r.tag_name} {r.published_at}")

            for a in r.assets:
                # print(vars(a))
                # print(f"Asset {a.name} = {a.download_count}")
                lines.append("github_releases,repo=%s,org=\"%s\"%s downloads=%d %s" % (
                    repo.name,
                    org,
                    f"{labels},release={r.tag_name},asset={a.name}",
                    a.download_count,
                    today.strftime("%s"),
                ))
    except Exception as e:
        print(f"Failed to get asset stats from repo {repo} {e}", file=sys.stderr)
        return

    for l in lines:
        print(l)


def get_repo_popularity(repo):
    global blacklist, labels

    today = datetime.datetime.today()
    org = None
    if repo.organization is not None:
        org = repo.organization.name
    if org in blacklist:
        return

    lines = []
    lines.append("github_popularity,repo=%s,org=\"%s\"%s stars=%d %s" % (
        repo.name,
        org,
        labels,
        repo.stargazers_count,
        today.strftime("%s"),
    ))
    lines.append("github_popularity,repo=%s,org=\"%s\"%s watchers=%d %s" % (
        repo.name,
        org,
        labels,
        repo.watchers_count,
        today.strftime("%s"),
    ))
    lines.append("github_popularity,repo=%s,org=\"%s\"%s forks=%d %s" % (
        repo.name,
        org,
        labels,
        repo.forks_count,
        today.strftime("%s"),
    ))

    for l in lines:
        print(l)

# loops over repos and gets clones stats
def get_clones(g, days):
    for repo in g.get_user().get_repos():
        get_repo_stats("clones", repo, days)


# loops over repos and gets views stats
def get_traffic(g, days):
    for repo in g.get_user().get_repos():
        get_repo_stats("views", repo, days)


def get_releases(g):
    for repo in g.get_user().get_repos():
        get_asset_stats(repo)


def get_popularity(g):
    for repo in g.get_user().get_repos():
        get_repo_popularity(repo)


if __name__ == "__main__":
    token = os.environ["GITHUB_TOKEN"]
    if not token:
        print("Environment variable GITHUB_TOKEN is required")
        print("Use a personal token you can generate in:")
        print("GitHub -> Settings -> Developer Settings -> Personal access tokens")
        exit(1)
    if "GITHUB_DAYS" in os.environ:
        days = int(os.environ["GITHUB_DAYS"])
    else:
        days = 3

    labels = ""
    if "INFLUX_LABELS" in os.environ and os.environ["INFLUX_LABELS"] != "":
        labels = "," + os.environ["INFLUX_LABELS"]

    blacklist = []
    if "INFLUX_ORG_BLACKLIST" in os.environ and os.environ["INFLUX_ORG_BLACKLIST"] != "":
        blacklist = os.environ["INFLUX_ORG_BLACKLIST"].split(",")

    g = Github(token)

    if len(sys.argv) == 1:
        get_traffic(g, days)
        get_clones(g, days)
        get_releases(g)
        get_popularity(g)
    else:
        if sys.argv[1] == "--traffic":
            get_traffic(g, days)
        if sys.argv[1] == "--clones":
            get_clones(g, days)
        if sys.argv[1] == "--releases":
            get_releases(g)
        if sys.argv[1] == "--popularity":
            get_popularity(g)
