# -*- encoding: utf-8 -*-
"""
A script that will mirror every repository in a Github organization locally.

Usage:
    github-mirror (init|sync) <organization> [options]

Options:
    --workdir=/path   Path to sync repositories to
    --only-repo=repo  Will only sync <org>/<repo> instead of every repo
"""
import os
import sys
import git
import json
import docopt
import github


def setup_config_file():
    with file('.githubmirror', 'w') as f:
        prompt = ("Please give me a Github API token "
                  "(create on https://github.com/settings/applications): ")
        auth_token = raw_input(prompt)
        c = dict(auth_token=auth_token)
        json.dump(c, f)


def get_config_file():
    if not os.path.isfile('.githubmirror'):
        setup_config_file()

    with file('.githubmirror') as f:
        c = json.load(f)
        return c


def get_auth_token():
    config = get_config_file()
    return config.get('auth_token')


def get_github_client():
    token = get_auth_token()
    return github.Github(token)


def get_organization(organization_name):
    gh = get_github_client()
    org = None
    while not org:
        try:
            org = gh.get_organization(organization_name)
        except github.GithubException:
            print >>sys.stderr, "Github did not accept this API token!"
            setup_config_file()
    return org


class FetchProgress(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        # Ignore the details, just give an indication that we haven't hung:
        sys.stdout.write(".")
        sys.stdout.flush()


def get_repo_path(repo_name, dir):
    return os.path.join(os.getcwd(), "%s.git" % repo_name)


def init_repos(repos, dir):
    for repo in repos:
        url = repo.ssh_url
        gitdir = git.Repo.init(get_repo_path(repo.name, dir), bare=True)
        try:
            gitdir.create_remote('origin', url)
        except git.exc.GitCommandError:
            pass


def fetch(repos, dest):
    for repo in repos:
        gitdir = git.Repo.init(get_repo_path(repo.name, dir), bare=True)
        remote = gitdir.remote(name='origin')
        print ("Fetching %s..." % repo.name),
        remote.fetch(progress=FetchProgress())
        print ""


if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    dir = args['--workdir']
    if not dir:
        dir = os.getcwd()

    org = get_organization(args['<organization>'])
    if args['--only-repo']:
        repos = [org.get_repo(args['--only-repo'])]
    else:
        repos = org.get_repos()

    if args['init']:
        init_repos(repos, dir)

    fetch(repos, dir)
