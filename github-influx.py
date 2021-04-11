#!python3

import datetime
import os
import sys

from github import Github


# always returns a result for yesterday and today and fills with 0 values
def get_traffic(g):
    today = datetime.datetime.utcnow().date()
    yesterday = today - datetime.timedelta(days=1)

    for repo in g.get_user().get_repos():
        # print(repo.name)
        stats = repo.get_views_traffic('day')
        # print(stats)
        lines = {}
        for s in stats['views']:
            time = datetime.datetime.strptime(str(s.timestamp), "%Y-%m-%d %H:%M:%S")

            if time.strftime('%Y-%m-%d') not in [yesterday.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')]:
                continue

            lines[time.strftime('%s')] = "github_views,repo=%s count=%d,unique=%d %s" % (
                repo.name, s.count, s.uniques, time.strftime('%s'))
        # fill with 0 values
        if yesterday.strftime('%s') not in lines:
            lines[yesterday.strftime('%s')] = "github_views,repo=%s count=%d,unique=%d %s" % (
                repo.name, 0, 0, yesterday.strftime('%s'))

        if today.strftime('%s') not in lines:
            lines[today.strftime('%s')] = "github_views,repo=%s count=%d,unique=%d %s" % (
                repo.name, 0, 0, today.strftime('%s'))

        for d in sorted(lines, key=lines.get):
            print(lines[d])


# always returns a result for yesterday and today and fills with 0 values
def get_clones(g):
    today = datetime.datetime.utcnow().date()
    yesterday = today - datetime.timedelta(days=1)

    for repo in g.get_user().get_repos():
        stats = repo.get_clones_traffic('day')
        # print(stats)
        lines = {}
        for s in stats['clones']:
            time = datetime.datetime.strptime(str(s.timestamp), "%Y-%m-%d %H:%M:%S")

            if time.strftime('%Y-%m-%d') not in [yesterday.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')]:
                continue

            lines[time.strftime('%s')] = "github_clones,repo=%s count=%d,unique=%d %s" % (
                repo.name, s.count, s.uniques, time.strftime('%s'))

        # fill with 0 values
        if yesterday.strftime('%s') not in lines:
            lines[yesterday.strftime('%s')] = "github_clones,repo=%s count=%d,unique=%d %s" % (
                repo.name, 0, 0, yesterday.strftime('%s'))

        if today.strftime('%s') not in lines:
            lines[today.strftime('%s')] = "github_clones,repo=%s count=%d,unique=%d %s" % (
                repo.name, 0, 0, today.strftime('%s'))

        for d in sorted(lines, key=lines.get):
            print(lines[d])


if __name__ == "__main__":
    token = os.environ["GITHUB_TOKEN"]
    if not token:
        print('Environment variable GITHUB_TOKEN is required')
        print('Use a personal token you can generate in:')
        print('GitHub -> Settings -> Developer Settings -> Personal access tokens')
        exit(1)

    gh = Github(token)

    if len(sys.argv) == 1:
        get_traffic(gh)
        get_clones(gh)
    else:
        if sys.argv[1] == '--traffic':
            get_traffic(gh)
        if sys.argv[1] == '--clones':
            get_clones(gh)
