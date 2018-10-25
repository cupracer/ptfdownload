#!/usr/bin/python

# Copyright (c) 2018 Thomas Schulte.  All rights reserved.
#
# This file is part of ptfdownload.
#
# ptfdownload is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ptfdownload is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ptfdownload. If not, see <http://www.gnu.org/licenses/>

import sys
import os
import subprocess
import getpass
import urllib2
import re
import base64
import getopt


def get_program_title(banner=False):
    title = 'Program Temporary Fix (PTF) download helper'

    if banner:
        border = '############################################\n'
        return border + title + "\n" + border

    return title


def warn_root_uid():
    if os.getuid() == 0:
        print "WARNING! You're running this script with root permissions, which is not recommended."


def print_welcome():
    print (get_program_title(True) + "\n"
           "This script is intended to simplify the download of PTF packages.\n"
           "For more information on using PTFs, please visit the following support articles:\n\n"
           "* Best practice for applying Program Temporary Fixes (PTFs)\n"
           "  https://www.suse.com/support/kb/doc/?id=7016640\n\n"
           "* SLES 12: How to import suse_key for signed PTF packages\n"
           "  https://www.suse.com/support/kb/doc/?id=7016511\n")


def check_build_key():
    try:
        devnull = open(os.devnull, 'w')
        subprocess.check_call(['rpm', '-V', 'suse-build-key'], stdout=devnull, stderr=subprocess.STDOUT)
        return True
    except OSError:
        print "Verification of RPM packages is not available on this system."
        return False
    except Exception as e:
        print ("Notice:\n"
               "Something seems to be wrong with the \"suse-build-key\" RPM package.\n"
               "It may be required to (re)install it before being able to install any PTF packages on this system.\n"
               "Raw error message: " + str(e))
        return False


def download_item(name, url, base64auth, output_directory):
    r = urllib2.Request(url)

    if base64auth:
        r.add_header("Authorization", "Basic %s" % base64auth)

    u = urllib2.urlopen(r)
    f = open(output_directory + name, 'wb')
    m = u.info()
    target_file_size = int(m.getheaders("Content-Length")[0])
    progress_file_size = 0
    block_sz = 8192

    while True:
        read_buffer = u.read(block_sz)
        if not read_buffer:
            break

        progress_file_size += len(read_buffer)
        f.write(read_buffer)
        status = r"%10d  [%3.2f%%]" % (progress_file_size, progress_file_size * 100. / target_file_size)
        status = status + chr(8) * (len(status) + 1)
        print status

    print ""
    f.close()


def add_slash(str_to_edit):
    if not str_to_edit.endswith('/'):
        str_to_edit += '/'
    return str_to_edit


def do_download_cli(output_directory, url, username, password, ignore_optional, ignore_signature):
    print ("\nPlease provide necessary information:\n\n")

    if output_directory == '':
        output_directory = raw_input("Output dir   : ")
    else:
        print "Output dir   : " + output_directory

    if not output_directory:
        print "No output directory given."
        return False

    output_directory = add_slash(output_directory)

    if url == '':
        url = raw_input("URL          : ")
    else:
        print "URL          : " + url

    if not url:
        print "No URL given."
        return False

    if username == '':
        username = raw_input("Username     : ")
    else:
        print "Username     : " + username

    # if not username:
    #     print "No username given."
    #     return False

    if password == '':
        password = getpass.getpass("Password     : ")

    # if not password:
    #     print "No password given."
    #     return False

    if do_download(output_directory, url, username, password, ignore_optional, ignore_signature):
        print ("To install the downloaded packages please run (as root):\n\n"
               "$ rpm -Fvh " + output_directory + "*.rpm\n")
        return True


def do_download(output_directory, url, username, password, ignore_optional, ignore_signature):
    has_readme = False
    base64auth = ''

    if username and password:
        base64auth = base64.b64encode('%s:%s' % (username, password))

    is_single_download = False

    if url.endswith('.rpm'):
        # force-fake final paths for single rpm download:
        is_single_download = True
        base_url, filename = os.path.split(url)
        url = base_url
        links = [filename]
    else:
        try:
            print "\nRetrieving information..."
            request = urllib2.Request(url)

            if base64auth:
                request.add_header("Authorization", "Basic %s" % base64auth)

            index_page = urllib2.urlopen(request)
            index_html = index_page.read()
            links = re.findall(' href="(.*rpm|.*readme.txt)"', index_html)
        except Exception as e:
            print ("Error while accessing given URL.\n"
                   "Raw error message: " + str(e))
            return False

    if not len(links) > 0:
        print "Given URL does not seem to contain links to any downloadable files."
        return False

    output_directory = add_slash(output_directory)

    if not os.path.isdir(output_directory):
        print 'Directory "' + output_directory + '" does not seem to exist.'
        return False

    print 'Downloading to "' + output_directory + '":\n'

    for link in links:
        if '/' in link:
            item_name = link.rsplit('/', 1)[-1]
        else:
            item_name = link

        item_url = url
        if not link.startswith('/'):
            item_url = add_slash(item_url)
        item_url += link

        try:
            if ignore_optional is True and is_single_download is False and (
                    item_url.endswith('.src.rpm') or 'debuginfo' in link or 'debugsource' in link):
                print "* " + item_name + " (SKIPPED: optional)"
                continue
            else:
                print "* " + item_name
                download_item(item_name, item_url, base64auth, output_directory)
        except Exception as e:
            print ("\nSomething went wrong while downloading.\n"
                   "Raw error message: " + str(e))
            return False

        try:
            if ignore_signature and item_name.endswith('.rpm'):
                check_downloaded_package(output_directory + item_name)
            if item_name.endswith('.txt'):
                has_readme = True
        except Exception as e:
            print "\nError: " + repr(e)
            return False

    print "\nDownloads finished."
    if has_readme:
        print "Output directory contains at least one .txt file. Please read!"
    return True


def check_downloaded_package(package_path):
    devnull = open(os.devnull, 'w')
    process = subprocess.call(['rpm', '-K', package_path], stdout=devnull, stderr=subprocess.STDOUT)

    if process != 0:
        raise Exception('Signature NOT OK!')


def print_cmd_info():
    print get_program_title() + "\n"
    print ("""usage: %s [-d <output_directory>] [-p <url>] [-u <username>] [-i] [-s]

    General:
        -h,   --help              print this help
        
    Recommended:
        -d,   --directory=DIR     use specified download directory

    Optional:
        -p,   --ptf-url=URL       URL to use
        -u,   --username=USER     username for authentication
        -i,   --ignore-optional   ignore optional packages (src, debuginfo, debugsource)
        -s,   --ignore-signature  ignore signature errors"""
           % os.path.basename(__file__))


#####################################

def main():
    output_directory = ''
    url = ''
    username = ''
    password = ''
    ignore_optional = False
    ignore_signature = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hd:p:u:is", ["help", "directory=", "ptf-url=", "username=",
                                                 "ignore-optional", "ignore-signature"])

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print_cmd_info()
                exit()
            elif opt in ('-d', '--directory'):
                output_directory = arg
            elif opt in ('-p', '--ptf-url'):
                url = arg
            elif opt in ('-u', '--username'):
                username = arg
            elif opt in ('-i', '--ignore-optional'):
                ignore_optional = True
            elif opt in ('-s', '--ignore-signature'):
                ignore_signature = True

    except getopt.GetoptError:
        print_cmd_info()
        exit(2)

    print_welcome()

    warn_root_uid()

    check_build_key()

    if not do_download_cli(output_directory, url, username, password, ignore_optional, ignore_signature):
        print "\nAborting."


if __name__ == '__main__':
    main()
