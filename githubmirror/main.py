# -*- encoding: utf-8 -*-

import os
import sys
import git
import json
import github

REMOTE_NAME = 'origin'


def setup_config_file(workdir):
    config = dict()
    with open(get_workdir_path('.githubmirror', workdir), 'w') as config_file:
        prompt = ("Please give me a Github API token, "
                  "create on https://github.com/settings/applications : ")
        auth_token = raw_input(prompt)
        config = dict(auth_token=auth_token)
        json.dump(config, config_file)
    return config


def get_config_file(workdir):
    if not os.path.isfile(get_workdir_path('.githubmirror', workdir)):
        setup_config_file(workdir)

    with file(get_workdir_path('.githubmirror', workdir)) as f:
        try:
            config = json.load(f)
        except ValueError:
            return setup_config_file(workdir)
        return config


def get_auth_token(workdir):
    config = get_config_file(workdir)
    return config.get('auth_token')


def get_github_client(workdir):
    token = get_auth_token(workdir)
    return github.Github(token)


def get_organization(organization_name, workdir):
    gh = get_github_client(workdir)
    org = None
    while not org:
        try:
            org = gh.get_organization(organization_name)
        except github.GithubException as e:
            print >>sys.stderr, "Github error: %s" % e
            setup_config_file(workdir)
    return org


def expand_workdir(workdir):
    return os.path.expanduser(os.path.expandvars(workdir))


def get_workdir_path(filename, workdir):
    return os.path.join(expand_workdir(workdir), filename)


def get_repo_path(repo_name, workdir):
    return get_workdir_path("%s.git" % repo_name, workdir)

def print_failed(failed):
    print "Failures encountered while processing:"
    for repo in failed:
        print ("    %s" % repo.name)

def init_repo(repo, workdir):
    path = get_repo_path(repo.name, workdir)
    # Create accessor
    gitdir = git.Repo.init(path, bare=True)
    # Log about it
    print ("Initializing %s..." % (repo.name))
    # Cleanup existing origin, if any
    try:
        remote = gitdir.remote(REMOTE_NAME)
        gitdir.delete_remote(remote)
    except (ValueError, git.exc.GitCommandError) as e:
        pass # can be ignored
    # Add the remote
    gitdir.git.remote("add", "--mirror", REMOTE_NAME, repo.ssh_url)

def init_repos(repos, workdir):
    failed = []
    for repo in repos:
        try:
            init_repo(repo, workdir)
        except git.exc.GitCommandError as e:
            print str(e)
            failed.append(repo)
    if failed:
        print_failed(failed)

def fetch_repo(repo, workdir):
    path = get_repo_path(repo.name, workdir)
    # Initialize if it doesn't exist
    if not os.path.exists(path):
        init_repo(repo, workdir)
    # Create accessor
    gitdir = git.Repo.init(path, bare=True)
    # Log about it
    print ("Fetching %s..." % (repo.name))
    # Perform the fetch
    gitdir.git.fetch(REMOTE_NAME)

def fetch(repos, workdir):
    failed = []
    for repo in repos:
        try:
            fetch_repo(repo, workdir)
        except git.exc.GitCommandError as e:
            print str(e)
            failed.append(repo)
    if failed:
        print_failed(failed)
