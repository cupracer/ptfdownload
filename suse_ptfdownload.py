#!/usr/bin/python

import sys
import os
import subprocess
import getpass
import urllib2
import re
import base64
import getopt


def warn_root_uid():
    if os.getuid() == 0:
        print "WARNING! You're running this script with root permissions, which is not recommended."


def print_welcome():
    print ("############################################################\n"
           "Welcome to the Program Temporary Fix (PTF) download helper!\n"
           "############################################################\n\n"
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
    except:
        return False


def download_item(name, url, base64auth, outputdir):
    r = urllib2.Request(url)
    r.add_header("Authorization", "Basic %s" % base64auth)
    u = urllib2.urlopen(r)
    f = open(outputdir + name, 'wb')
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


def do_ptf_download_cli(outputdir, url, username, password, ignore_optional):
    outputdir = add_slash(outputdir)

    print ("\nPlease provide necessary information:\n\n"
           "Output dir   : " + outputdir)

    if url == '':
        url = raw_input("PTF URL      : ")
    else:
        print "PTF URL      : " + url

    if not url:
        print "No URL given."
        return False

    if username == '':
        username = raw_input("SCC username : ")
    else:
        print "SCC username : " + username

    if not username:
        print "No username given."
        return False

    if password == '':
        password = getpass.getpass("SCC password : ")

    if not password:
        print "No password given."
        return False

    if do_ptf_download(outputdir, url, username, password, ignore_optional):
        print ("To install the downloaded packages please run as root:\n\n"
               "$ rpm -Fvh " + outputdir + "*.rpm\n")
        return True


def do_ptf_download(outputdir, url, username, password, ignore_optional):
    has_readme = False
    base64auth = base64.b64encode('%s:%s' % (username, password))

    try:
        print "\nRetrieving PTF information..."
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64auth)
        index_page = urllib2.urlopen(request)
        index_html = index_page.read()
        links = re.findall(' href="(.*rpm|.*readme.txt)"', index_html)
    except:
        print "Error while accessing given URL."
        return False

    if not len(links) > 0:
        print "Given URL does not seem to contain links to any downloadable files."
        return False

    outputdir = add_slash(outputdir)

    if not os.path.isdir(outputdir):
        print 'Directory "' + outputdir + '" does not seem to exist.'
        return False

    print 'Downloading to "' + outputdir + '":\n'

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
            if ignore_optional is True and (
                    item_url.endswith('.src.rpm') or 'debuginfo' in link or 'debugsource' in link):
                print "* " + item_name + " (SKIPPED: optional)"
                continue
            else:
                print "* " + item_name
                download_item(item_name, item_url, base64auth, outputdir)
        except:
            print "\nSomething went wrong while downloading."
            return False

        try:
            if item_name.endswith('.rpm'):
                check_downloaded_package(outputdir + item_name)
            if item_name.endswith('.txt'):
                has_readme = True
        except Exception as error:
            print "\nError: " + repr(error)
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
    print ("""usage: %s [-d <outputdir>] [-p <url>] [-u <username>] [-i]

    Recommended:
        -d: use specified download directory

    Optional:
        -p: PTF URL to use
        -u: SCC username
        -i: ignore optional packages (src, debuginfo, debugsource)
        -h: print this help""" % os.path.basename(__file__))


#####################################

def main():
    outputdir = './'
    url = ''
    username = ''
    password = ''
    ignore_optional = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:d:p:u:i")

        for opt, arg in opts:
            if opt == '-h':
                print_cmd_info()
                exit()
            elif opt == '-d':
                outputdir = arg
            elif opt == '-p':
                url = arg
            elif opt == '-u':
                username = arg
            elif opt == '-i':
                ignore_optional = True

    except getopt.GetoptError:
        print_cmd_info()
        exit(2)

    print_welcome()

    warn_root_uid()

    if not check_build_key():
        print ("Notice:\n"
               "Something seems to be wrong with the \"suse-build-key\" RPM package.\n"
               "It may be required to (re)install it before you'll be able to install any PTF packages on this system.")

    if not do_ptf_download_cli(outputdir, url, username, password, ignore_optional):
        print "\nAborting."


if __name__ == '__main__':
    main()
