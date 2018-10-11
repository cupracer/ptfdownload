#!/usr/bin/python

from suse_ptfdownload import do_ptf_download

output_directory = './'
url = ''
username = ''
password = ''
ignore_optional = False

do_ptf_download(output_directory, url, username, password, ignore_optional)
