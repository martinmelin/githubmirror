# -*- encoding: utf-8 -*-

import os
import sys
import git
import json
import github


def setup_config_file(dir):
    config = dict()
    with open(get_workdir_path('.githubmirror', dir), 'w') as config_file:
        prompt = ("Please give me a Github API token "
                  "(create on https://github.com/settings/applications): ")
        auth_token = raw_input(prompt)
        config = dict(auth_token=auth_token)
        json.dump(config, config_file)
    return config


def get_config_file(dir):
    if not os.path.isfile(get_workdir_path('.githubmirror', dir)):
        setup_config_file()

    with file('.githubmirror') as f:
        try:
            config = json.load(f)
        except ValueError:
            return setup_config_file(dir)
        return config


def get_auth_token(dir):
    config = get_config_file(dir)
    return config.get('auth_token')


def get_github_client(dir):
    token = get_auth_token(dir)
    return github.Github(token)


def get_organization(organization_name, dir):
    gh = get_github_client(dir)
    org = None
    while not org:
        try:
            org = gh.get_organization(organization_name)
        except github.GithubException as e:
            print >>sys.stderr, "Github error: %s" % e
            setup_config_file(dir)
    return org


class FetchProgress(git.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        # Ignore the details, just give an indication that we haven't hung:
        sys.stdout.write(".")
        sys.stdout.flush()


def get_workdir_path(filename, dir):
    return os.path.join(os.getcwd(), filename)


def get_repo_path(repo_name, dir):
    return get_workdir_path("%s.git" % repo_name, dir)


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
        path = get_repo_path(repo.name, dir)
        gitdir = git.Repo.init(path, bare=True)
        remote = gitdir.remote(name='origin')
        print ("Fetching %s in %s..." % (repo.name, path)),  # to avoid newline
        remote.fetch(progress=FetchProgress())
        print ""
