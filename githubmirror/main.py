# -*- encoding: utf-8 -*-

import os
import sys
import git
import github
import keyring  # https://pypi.python.org/pypi/keyring

REMOTE_NAME = 'origin'


def store_auth_token(organization_name):
    prompt = ("Please give me a Github API token, "
              "create on https://github.com/settings/applications : ")
    auth_token = raw_input(prompt)
    keyring.set_password('githubmirror', organization_name, auth_token)


def get_auth_token(organization_name):
    return keyring.get_password('githubmirror', organization_name)


def get_github_client(organization_name):
    token = get_auth_token(organization_name)
    return github.Github(token)


def get_organization(organization_name):
    gh = get_github_client(organization_name)
    org = None
    while not org:
        try:
            org = gh.get_organization(organization_name)
        except github.GithubException as e:
            print >>sys.stderr, "Github error: %s" % e
            store_auth_token(organization_name)
    return org


def expand_workdir(workdir):
    return os.path.expanduser(os.path.expandvars(workdir))


def get_workdir_path(filename, workdir):
    return os.path.join(expand_workdir(workdir), filename)


def get_repo_path(repo_name, workdir):
    return get_workdir_path("%s.git" % repo_name, workdir)


def init_repos(repos, workdir):
    for repo in repos:
        url = repo.ssh_url
        gitdir = git.Repo.init(get_repo_path(repo.name, workdir), bare=True)
        # Cleanup existing origin, if any
        try:
            remote = gitdir.remote(REMOTE_NAME)
            gitdir.delete_remote(remote)
        except (ValueError, git.exc.GitCommandError):
            pass

        gitdir.git.remote("add", "--mirror", REMOTE_NAME, url)


def fetch(repos, workdir):
    for repo in repos:
        path = get_repo_path(repo.name, workdir)
        gitdir = git.Repo.init(path, bare=True)
        print ("Fetching %s in %s..." % (repo.ssh_url, path))
        gitdir.git.fetch(REMOTE_NAME)