#!/usr/bin/python

# Copyright (c) 2018 Thomas Schulte.  All rights reserved.
#
# This file is part of suse_ptfdownload.
#
# suse_ptfdownload is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# suse_ptfdownload is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with suse_ptfdownload. If not, see <http://www.gnu.org/licenses/>

from suse_ptfdownload import do_ptf_download

output_directory = './'
url = ''
username = ''
password = ''
ignore_optional = False

do_ptf_download(output_directory, url, username, password, ignore_optional)
