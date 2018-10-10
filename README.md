# Program Temporary Fix (PTF) download helper
This script is intended to simplify the download of PTF packages.  
For more information on using PTFs, please visit the following support articles:

* Best practice for applying Program Temporary Fixes (PTFs)  
  https://www.suse.com/support/kb/doc/?id=7016640
  
* SLES 12: How to import suse_key for signed PTF packages  
  https://www.suse.com/support/kb/doc/?id=7016511

## Command-line interface
```
$ ./suse_ptfdownload.py -h
usage: suse_ptfdownload.py [-d <outputdir>] [-p <url>] [-u <username>] [-i]

    Recommended:
        -d: use specified download directory

    Optional:
        -p: PTF URL to use
        -u: SCC username
        -i: ignore optional packages (src, debuginfo, debugsource)
        -h: print this help
```

## Module
(see [test.py](https://github.com/cupracer/suse-ptf-utils/blob/master/test.py))

```
#!/usr/bin/python

from suse_ptfdownload import do_ptf_download

outputdir = './'
url = ''
username = ''
password = ''
ignoreOptional = False

do_ptf_download(outputdir, url, username, password, ignoreOptional)
```

## Example CLI session
```
$ mkdir /tmp/my-ptf

$ ./suse_ptfdownload.py -d my-ptf
######################################################
Welcome to the Program Temporary Fix download helper!
######################################################

This script is intended to simplify the download of PTF packages.
For more information on using PTFs, please visit the following support articles:

* Best practice for applying Program Temporary Fixes (PTFs)
  https://www.suse.com/support/kb/doc/?id=7016640

* SLES 12: How to import suse_key for signed PTF packages
  https://www.suse.com/support/kb/doc/?id=7016511


Please provide necessary information:

Output dir   : /tmp/my-ptf/
PTF URL      : [*REMOVED*]
SCC username : [*REMOVED*]
SCC password :

Retrieving PTF information...
Downloading to "/tmp/my-ptf/":

* [SOME_RPM_1].rpm
    127291  [100.00%]
* [SOME_RPM_2].rpm
    310716  [100.00%]
* [SOME_RPM_3].rpm
    284098  [100.00%]
* readme.txt
       298  [100.00%]

Downloads finished.
Output directory contains at least one .txt file. Please read!
To install the downloaded packages please run as root:

$ rpm -Fvh /tmp/my-ptf/*.rpm

```

