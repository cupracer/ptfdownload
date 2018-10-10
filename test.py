#!/usr/bin/python

from suse_ptfdownload import do_ptf_download

outputdir = './'
url = ''
username = ''
password = ''
ignoreOptional = False

do_ptf_download(outputdir, url, username, password, ignoreOptional)
