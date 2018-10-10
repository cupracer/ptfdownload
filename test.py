#!/usr/bin/python

from suse_ptfdownload import do_ptf_download

outputdir = './'
url = ''
username = ''
password = ''
includeOptional = False
verbose = True

do_ptf_download(outputdir, url, username, password, includeOptional, verbose)

