#!/usr/bin/env python
#coding: utf-8

from os import sys
from os import path
from os import environ

parent_dir, bin_dir = path.split(path.dirname(path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from optparse import OptionParser
from nouka.command import Main

if __name__ == '__main__':
    p = OptionParser()
    p.add_option('-c','--config',dest="config",help="configuration file. default is <nouka_HOME>/conf/nouka.cfg")
    p.set_defaults(
	config=parent_dir+'/conf/nouka.conf',
	)
    opts,args = p.parse_args()
    host_name=environ['HOSTNAME']
    sys.exit(Main(opts.config,host_name=host_name).run())

# :vim: filetype=python :
