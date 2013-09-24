#!/usr/bin/env python

import sys, argparse, configparser
from github import Github

def main(argv):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'Github' not in config:
      print 'Please setup config.ini to have a github user/apikey section'
      exit()

    parser = argparse.ArgumentParser(description='Mirror one Github organization to another')
    parser.add_argument('src', help='Source organization')
    parser.add_argument('target', help='Target Organization')
    parser.add_argument('--verbose', '-v', help='Increase Verbosity', action="store_true")
    args = parser.parse_args()

    if (args.verbose):
      print "Mirroring {} organization to {} organization using User {}".format(args.src, args.target, config['Github']['User'])
   
    g = Github(config['Github']['User'], config['Github']['Key'])



if __name__ == '__main__':
   main(sys.argv[1:])
