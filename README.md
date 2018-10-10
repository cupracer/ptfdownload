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
usage: suse_ptfdownload.py [-d <outputdir>] [-p <url>] [-u <username>] [-i] [-v]

    Optional:
        -d: use specified download directory
        -p: PTF URL to use
        -u: SCC username
        -i: include optional packages (src, debuginfo, debugsource)
        -v: verbose output
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
includeOptional = False
verbose = True

do_ptf_download(outputdir, url, username, password, includeOptional, verbose)
```

## Example CLI session
```
# ./suse_ptfdownload.py -d my-ptf
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

Output dir   : my-ptf/
PTF URL      : [*REMOVED*]
SCC username : [*REMOVED*]
SCC password :

Retrieving PTF information...
Downloading to "my-ptf/":

* [SOME_RPM_1].rpm
    127291  [100.00%]
* [SOME_RPM_2].rpm
    310716  [100.00%]
* [SOME_RPM_3].rpm
    284098  [100.00%]

Downloads finished.
To install the downloaded packages please run as root:

$ rpm -Fvh my-ptf/*.rpm

```

