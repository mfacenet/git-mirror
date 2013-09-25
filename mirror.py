#!/usr/bin/env python

import sys, os, argparse, configparser, shutil
from github import Github
from git import *
from urlparse import urlparse

def main(argv):
    config = parse_config()
    args = parse_arguments(argv)
    if (args.verbose):
      print "Mirroring {} organization to {} organization using User {}".format(args.src, args.target, config['Github']['User'])
   
    g = Github(config['Github']['User'], config['Github']['Key'])
    repo_list = get_repo_list(g, args.src, args.target)
    process_repos(config, args.dir, repo_list, args.verbose, args.prefix)


def parse_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'Github' not in config:
      print >> sys.stderr, 'Please setup config.ini to have a github user/apikey section'
      exit(1)
    return config


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Mirror one Github organization to another')
    parser.add_argument('src', help='Source organization')
    parser.add_argument('target', help='Target Organization')
    parser.add_argument('--verbose', '-v', help='Increase Verbosity', action="store_true")
    parser.add_argument('--dir', '-d', help='Target directory where the local copies will be stored', default="/tmp/")
    parser.add_argument('--prefix', help="Optional repo name prefix", default=None)
    return parser.parse_args()

  

def get_repo_list(g, src, target, prefix=None):
    src_org = g.get_organization(src)
    mirror_repos = src_org.get_repos()
    target_org = g.get_organization(target)
    target_repos = target_org.get_repos()
    repo_dict = {}
    for repo in mirror_repos:
      exists = False
      if prefix is None:
        name = repo.name
      else:
        name = args.prefix + '-' + repo.name
      for exist_repo in target_repos:
        if name == exist_repo.name:
	  exists = exist_repo
      if not exists:
        # Create Fork
	exist_repo = target_org.create_repo(name, description=repo.description, private=repo.private, auto_init=False)
      repo_dict[repo.name] = {'src': repo.ssh_url, 'target': exist_repo.ssh_url}
    return repo_dict
      
def process_repo(path, name, src, target, verbose=False):
  # Check if local repo clone  exists, if not clone with --mirror

  #Push up clone to github url
  if verbose:
    print "Processing source {} to target {} in {}".format(src, target, path)
  clone_dir = os.path.join(path, name)
  if os.path.exists(clone_dir) and os.path.isdir(clone_dir):
    shutil.rmtree(clone_dir)
  repo = Repo.clone_from(src, path + name, mirror=True)
  repo.git.push(target, mirror=True)

def process_repos( path, repo_list, verbose=False, prefix=None):
    for target, data in repo_list.items():
      process_repo(path, target, data['src'], data['target'], verbose)

if __name__ == '__main__':
   main(sys.argv[1:])
