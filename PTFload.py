#!/usr/bin/python

import sys
import os
import subprocess
import getpass
import urllib2
import re
import base64
import getopt

def printWelcome():
		print ( "###########################################################\n"
				"Welcome to the SUSE Program Temporary Fix download helper!\n"
				"###########################################################\n\n"
				"This script is intended to simplify the download of PTF packages.\n"
				"For more information on using PTFs, please visit the following support articles:\n\n"
				"* Best practice for applying Program Temporary Fixes (PTFs)\n"
				"  https://www.suse.com/support/kb/doc/?id=7016640\n\n"
				"* SLES 12: How to import suse_key for signed PTF packages\n"
				"  https://www.suse.com/support/kb/doc/?id=7016511\n")


def checkBuildKey():
		try:
				devnull = open(os.devnull, 'w')
				subprocess.check_call(['rpm', '-V', 'suse-build-key'], stdout=devnull, stderr=subprocess.STDOUT)
				return True
		except:
				return False


def downloadPackage(name, url, base64auth, outputdir):
		r = urllib2.Request(url)
		r.add_header("Authorization", "Basic %s" % base64auth)
		u = urllib2.urlopen(r)
		f = open(outputdir + name, 'wb')
		m = u.info()
		targetFileSize = int(m.getheaders("Content-Length")[0])
		progressFileSize = 0
		block_sz = 8192

		while True:
				buffer = u.read(block_sz)
				if not buffer:
						break

				progressFileSize += len(buffer)
				f.write(buffer)
				status = r"%10d  [%3.2f%%]" % (progressFileSize, progressFileSize * 100. / targetFileSize)
				status = status + chr(8)*(len(status)+1)
				print status

		print ""
		f.close()


def doPtfDownloadCli(outputdir, url, username, password, includeOptional, verbose):
		print ( "\nPlease provide necessary information:\n\n"
				"Output	   : " + outputdir)

		if url == '':
				url = raw_input("PTF URL	  : ")
		else:
				print "PTF URL	  : " + url

		if not url:
				print "No URL given."
				return False

		if username == '':
			username = raw_input("SCC username : ")

		if not username:
				print "No username given."
				return False

		if password == '':
			password = getpass.getpass("SCC password : ")

		if not password:
				print "No password given."
				return False

		if doPtfDownload(outputdir, url, username, password, includeOptional, verbose):
			print ("To install the downloaded packages please run as root:\n\n"
				"$ rpm -Fvh " + outputdir + "*.rpm\n")
			return True


def doPtfDownload(outputdir, url, username, password, includeOptional, verbose):
		base64auth = base64.b64encode('%s:%s' % (username, password))

		try:
				print "\nRetrieving PTF information..."
				request = urllib2.Request(url)
				request.add_header("Authorization", "Basic %s" % base64auth)
				indexPage = urllib2.urlopen(request)
				indexHtml = indexPage.read()
				rpmLinks = re.findall(' href="(.*rpm)"', indexHtml)
		except:
				print "Error while accessing given URL."
				return False

		if not len(rpmLinks) > 0:
				print "Given URL does not seem to contain links to any RPM packages."
				return False

		if not outputdir.endswith('/'):
				outputdir+= '/'

		if not os.path.isdir(outputdir):
				print 'Directory "' + outputdir + '" does not seem to exist.'
				return False

		print 'Downloading to "' + outputdir + '":\n'

		for link in rpmLinks:
				if '/' in link:
						packageName = link.rsplit('/', 1)[-1]
				else:
						packageName = link

				packageUrl = url
				if not url.endswith('/') and not link.startswith('/'):
						packageUrl+= '/'
				packageUrl+= link

				try:
						if includeOptional == False and (link.endswith('src.rpm') or 'debuginfo' in link or 'debugsource' in link):
								if verbose == True:
										print "* " + packageName + " (SKIPPED: optional, see help)"
								continue
						else:
								print "* " + packageName
								downloadPackage(packageName, packageUrl, base64auth, outputdir)
				except:
						print "\nSomething went wrong while downloading."
						return False

				try:
						checkDownloadedPackage(outputdir + packageName)
				except Exception as error:
						print "\nError: " + repr(error)
						return False

		print "\nDownloads finished."
		return True


def checkDownloadedPackage(packagePath):
		devnull = open(os.devnull, 'w')
		process = subprocess.call(['rpm', '-K', packagePath], stdout=devnull, stderr=subprocess.STDOUT)

		if process != 0:
				raise Exception('Signature NOT OK!')


def printCmdInfo():
		print ("""usage: %s [-d <outputdir>] [-u <url>] [-i] [-v]\n
		-d: use specified download directory
		-u: PTF base URL to use
		-i: include  optional packages (src, debuginfo, debugsource)
		-v: verbose output"""%os.path.basename(__file__))

#####################################

def main():
	outputdir = './'
	url = ''
	username = ''
	password = ''
	includeOptional = False
	verbose = False

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hd:u:i:v")
	except getopt.GetoptError:
		printCmdInfo()
		exit(2)

	for opt, arg in opts:
		if opt == '-h':
			printCmdInfo()
			exit()
		elif opt == '-d':
			outputdir = arg
		elif opt == '-u':
			url = arg
		elif opt == '-i':
			includeOptional = True
		elif opt == '-v':
			verbose = True

	printWelcome()

	if not checkBuildKey():
		print ( "Notice:\n"
			"Something seems to be wrong with the \"suse-build-key\" RPM package.\n"
			"It may be required to (re)install it before you'll be able to install any PTF packages on this system.")

	if not doPtfDownloadCli(outputdir, url, username, password, includeOptional, verbose):
		print "\nAborting."


if __name__ == '__main__':
	main()

