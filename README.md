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
