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
import docopt

import main


def cmd():
    args = docopt.docopt(__doc__)

    workdir = args['--workdir']
    if workdir:
        if not os.path.isdir(main.expand_workdir(workdir)):
            print >>sys.stderr, "Won't create the workdir for you!"
            raise SystemExit
    else:
        workdir = os.getcwd()

    org = main.get_organization(args['<organization>'], workdir)
    if args['--only-repo']:
        repos = [org.get_repo(args['--only-repo'])]
    else:
        repos = org.get_repos()

    if args['init']:
        main.init_repos(repos, workdir)

    if args['sync']:
        main.fetch(repos, workdir)

if __name__ == '__main__':
    cmd()
